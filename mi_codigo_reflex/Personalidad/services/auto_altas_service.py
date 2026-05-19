"""
Motor lógico de auto-altas: gestiona la idempotencia, el lock de concurrencia,
el cálculo de vencimientos y la creación/actualización de alumnos en la BD
PostgreSQL de la plataforma Reflex (schema: usuarios_metodos).
"""
import os
import sys
import time
import random
import string
import datetime
import bcrypt
import psycopg2

from Personalidad.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from Personalidad.services.email_service import send_credentials_email, send_access_extended_email

# ---------------------------------------------------------------------------
# MAPEADO DE PRODUCTOS → días de acceso y módulos habilitados
# ---------------------------------------------------------------------------
PRODUCT_ACCESS = {
    "380893": {"days": 5,  "modules": ["personalidad"]},
    "396346": {"days": 7,  "modules": ["personalidad"]},
    "396348": {"days": 30, "modules": ["pruebas_fisicas"]},
    "396350": {"days": 30, "modules": ["personalidad", "pruebas_fisicas"]},
}

# ---------------------------------------------------------------------------
# CONTROL DE CONCURRENCIA — FileLock basado en fichero
# ---------------------------------------------------------------------------
LOCK_TIMEOUT = int(os.getenv("AUTO_ALTA_LOCK_TIMEOUT_SECONDS", "600"))


class FileLockException(Exception):
    pass


class FileLock:
    """
    Gestor de bloqueo por fichero. Evita ejecuciones concurrentes del cron.
    - Si ya hay una ejecución activa (<10 min), sale con sys.exit(0).
    - Si lleva colgada >10 min, rompe el lock y continúa.
    """
    def __init__(self, lock_path=None):
        self.lock_file = lock_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "auto_altas.lock"
        )

    def __enter__(self):
        now = time.time()
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file) as f:
                    parts = f.read().strip().split(":")
                pid, created_at = int(parts[0]), float(parts[1])
            except Exception:
                pid, created_at = 0, 0.0

            elapsed = now - created_at
            if elapsed < LOCK_TIMEOUT:
                print(f"[LOCK] Ejecución activa (PID {pid}, {int(elapsed)}s). Saliendo.")
                sys.exit(0)
            else:
                print(f"[LOCK] Lock huérfano ({int(elapsed)}s > {LOCK_TIMEOUT}s). Rompiendo.")
                self._release()

        with open(self.lock_file, "w") as f:
            f.write(f"{os.getpid()}:{now}")
        print(f"[LOCK] Adquirido (PID {os.getpid()}).")
        return self

    def __exit__(self, *_):
        self._release()

    def _release(self):
        if os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
                print("[LOCK] Liberado.")
            except Exception as e:
                print(f"[LOCK] Error liberando: {e}")


# ---------------------------------------------------------------------------
# MOTOR PRINCIPAL
# ---------------------------------------------------------------------------
class AutoAltasService:

    def _conn(self):
        """Conexión a la BD PostgreSQL interna de Reflex."""
        for host in [DB_HOST, "localhost"]:
            try:
                return psycopg2.connect(
                    dbname=DB_NAME, user=DB_USER,
                    password=DB_PASSWORD, host=host, port=DB_PORT
                )
            except Exception:
                continue
        raise RuntimeError("No se pudo conectar a PostgreSQL.")

    def init_db(self):
        """Crea la tabla de control si no existe. Se llama al instanciar."""
        sql = """
        CREATE SCHEMA IF NOT EXISTS usuarios_metodos;

        CREATE TABLE IF NOT EXISTS usuarios_metodos.auto_altas_procesadas (
            id                BIGSERIAL    PRIMARY KEY,
            pedido_id         VARCHAR(100) NOT NULL,
            linea_id          VARCHAR(100) NOT NULL,
            producto_id       VARCHAR(50)  NOT NULL,
            email             VARCHAR(255) NOT NULL,
            estado            VARCHAR(20)  NOT NULL DEFAULT 'processing'
                                  CHECK (estado IN ('processing','processed','failed')),
            intentos          INT          NOT NULL DEFAULT 0,
            error             TEXT         NULL,
            usuario_id        VARCHAR(255) NULL,
            fecha_inicio      TIMESTAMP    NULL,
            fecha_vencimiento TIMESTAMP    NULL,
            created_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT uq_pedido_linea_producto UNIQUE (pedido_id, linea_id, producto_id)
        );
        CREATE INDEX IF NOT EXISTS idx_auto_altas_estado
            ON usuarios_metodos.auto_altas_procesadas (estado);
        CREATE INDEX IF NOT EXISTS idx_auto_altas_email
            ON usuarios_metodos.auto_altas_procesadas (email);
        """
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
            print("[DB] Tabla auto_altas_procesadas verificada.")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _gen_password(length=16) -> str:
        chars = string.ascii_letters + string.digits + "*@?¿¡!$#"
        pwd = (
            [random.choice(string.ascii_lowercase),
             random.choice(string.ascii_uppercase),
             random.choice(string.digits),
             random.choice("*@?¿¡!$#")]
            + random.choices(chars, k=length - 4)
        )
        random.shuffle(pwd)
        return "".join(pwd)

    @staticmethod
    def _parse_dt(val):
        if not val or val == "N/A":
            return None
        if isinstance(val, datetime.datetime):
            return val
        try:
            from dateutil import parser as dp
            return dp.parse(str(val))
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Procesamiento de una línea de pedido
    # ------------------------------------------------------------------
    def procesar_linea(
        self,
        pedido_id: str,
        linea_id: str,
        producto_id: str,
        email: str,
        nombre: str = "",
        apellidos: str = "",
        dni: str = None,
    ) -> bool:
        email       = email.strip().lower()
        pedido_id   = str(pedido_id).strip()
        linea_id    = str(linea_id).strip()
        producto_id = str(producto_id).strip()

        if producto_id not in PRODUCT_ACCESS:
            print(f"[WARN] Producto {producto_id} no mapeado. Saltando.")
            return False

        conn = self._conn()
        try:
            now = datetime.datetime.now()

            # ── 1. IDEMPOTENCIA: consultar registro existente ─────────────
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, estado, intentos, updated_at "
                    "FROM usuarios_metodos.auto_altas_procesadas "
                    "WHERE pedido_id=%s AND linea_id=%s AND producto_id=%s",
                    (pedido_id, linea_id, producto_id)
                )
                row = cur.fetchone()

            registro = {"id": row[0], "estado": row[1], "intentos": row[2], "updated_at": row[3]} if row else None

            if registro:
                estado, intentos, updated_at = registro["estado"], registro["intentos"], registro["updated_at"]

                if estado == "processed":
                    print(f"[IDEM] Ya procesado. Saltando ({pedido_id}/{linea_id}).")
                    return True

                if estado == "processing" and (now - updated_at).total_seconds() < LOCK_TIMEOUT:
                    print(f"[IDEM] En proceso reciente. Saltando.")
                    return False

                if estado == "failed" and intentos >= 3:
                    print(f"[IDEM] Máximo de intentos alcanzado. Saltando.")
                    return False

                # Reintentar
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE usuarios_metodos.auto_altas_procesadas "
                        "SET estado='processing', intentos=%s, updated_at=NOW(), error=NULL "
                        "WHERE id=%s",
                        (intentos + 1, registro["id"])
                    )
                conn.commit()
            else:
                # ── Insertar en 'processing' ───────────────────────────────
                try:
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO usuarios_metodos.auto_altas_procesadas "
                            "(pedido_id,linea_id,producto_id,email,estado,intentos,created_at,updated_at) "
                            "VALUES (%s,%s,%s,%s,'processing',1,NOW(),NOW())",
                            (pedido_id, linea_id, producto_id, email)
                        )
                    conn.commit()
                except psycopg2.IntegrityError:
                    conn.rollback()
                    print("[IDEM] Colisión de clave única. Saltando.")
                    return False

            # ── 2. DATOS DEL PRODUCTO ─────────────────────────────────────
            info     = PRODUCT_ACCESS[producto_id]
            days     = info["days"]
            modules  = info["modules"]
            ahora    = datetime.datetime.now()
            f_inicio = ahora

            # ── 3. ¿EXISTE EL ALUMNO? ────────────────────────────────────
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT email, nombre, apellidos, "
                    "hasta_personalidad, hasta_fisicas, "
                    "disabled_personalidad, disabled_fisicas "
                    "FROM usuarios_metodos.usuarios_plataformas WHERE email=%s",
                    (email,)
                )
                u = cur.fetchone()
            usuario = (
                {"email": u[0], "nombre": u[1], "apellidos": u[2],
                 "hasta_personalidad": u[3], "hasta_fisicas": u[4],
                 "disabled_personalidad": u[5], "disabled_fisicas": u[6]}
                if u else None
            )

            # ── 4. CÁLCULO DE VENCIMIENTOS ───────────────────────────────
            venc_perso   = self._parse_dt(usuario["hasta_personalidad"]) if usuario else None
            venc_fisicas = self._parse_dt(usuario["hasta_fisicas"])      if usuario else None

            hasta_perso_new   = venc_perso
            hasta_fisicas_new = venc_fisicas
            dis_perso_new     = True
            dis_fisicas_new   = True
            f_vencimiento     = ahora + datetime.timedelta(days=days)

            for mod in modules:
                if mod == "personalidad":
                    base = max(venc_perso, ahora) if venc_perso else ahora
                    hasta_perso_new   = base + datetime.timedelta(days=days)
                    dis_perso_new     = False
                    f_vencimiento     = hasta_perso_new
                elif mod == "pruebas_fisicas":
                    base = max(venc_fisicas, ahora) if venc_fisicas else ahora
                    hasta_fisicas_new = base + datetime.timedelta(days=days)
                    dis_fisicas_new   = False
                    f_vencimiento     = hasta_fisicas_new

            # hasta global = el más largo de los dos módulos activos
            activos = [d for d in [hasta_perso_new, hasta_fisicas_new] if d and d > ahora]
            hasta_global = max(activos) if activos else f_vencimiento

            # ── 5. CREAR O ACTUALIZAR ALUMNO ─────────────────────────────
            try:
                pedido_num = int(pedido_id)
            except ValueError:
                pedido_num = 0

            if usuario:
                # — Actualizar accesos —
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE usuarios_metodos.usuarios_plataformas "
                        "SET hasta_personalidad=%s, hasta_fisicas=%s, "
                        "    disabled_personalidad=%s, disabled_fisicas=%s, "
                        "    disabled=false, hasta=%s, pedido=%s "
                        "WHERE email=%s",
                        (hasta_perso_new, hasta_fisicas_new,
                         dis_perso_new, dis_fisicas_new,
                         hasta_global, pedido_num, email)
                    )
                conn.commit()
                full_name = f"{usuario['nombre']} {usuario['apellidos']}".strip() or email.split("@")[0]
                print(f"[ALUMNO] {email} actualizado. Vence: {hasta_global:%Y-%m-%d}")
                send_access_extended_email(email, full_name, modules, f_vencimiento)

            else:
                # — Crear nuevo alumno —
                if not nombre:
                    nombre = email.split("@")[0].capitalize()
                temp_pwd    = self._gen_password(16)
                hashed_pwd  = bcrypt.hashpw(temp_pwd.encode(), bcrypt.gensalt()).decode()

                hasta_p = hasta_perso_new   if "personalidad"   in modules else None
                hasta_f = hasta_fisicas_new if "pruebas_fisicas" in modules else None
                dis_p   = False if "personalidad"   in modules else True
                dis_f   = False if "pruebas_fisicas" in modules else True

                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO usuarios_metodos.usuarios_plataformas "
                        "(nombre,apellidos,dni,email,password,pedido,desde,hasta,"
                        " count_login,disabled,rol,hasta_personalidad,hasta_fisicas,"
                        " disabled_personalidad,disabled_fisicas) "
                        "VALUES (%s,%s,%s,%s,%s,%s,NOW(),%s,"
                        "        0,false,'estudiante',%s,%s,%s,%s)",
                        (nombre, apellidos, dni, email, hashed_pwd,
                         pedido_num, hasta_global,
                         hasta_p, hasta_f, dis_p, dis_f)
                    )
                conn.commit()
                full_name = f"{nombre} {apellidos}".strip()
                print(f"[ALUMNO] {email} creado. Vence: {hasta_global:%Y-%m-%d}")
                send_credentials_email(email, temp_pwd, full_name)

            # ── 6. MARCAR COMO PROCESSED ─────────────────────────────────
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE usuarios_metodos.auto_altas_procesadas "
                    "SET estado='processed', usuario_id=%s, "
                    "    fecha_inicio=%s, fecha_vencimiento=%s, "
                    "    updated_at=NOW(), error=NULL "
                    "WHERE pedido_id=%s AND linea_id=%s AND producto_id=%s",
                    (email, f_inicio, f_vencimiento, pedido_id, linea_id, producto_id)
                )
            conn.commit()
            print(f"[OK] Línea ({pedido_id}/{linea_id}) marcada como 'processed'.")
            return True

        except Exception as e:
            conn.rollback()
            print(f"[ERROR] {e}")
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE usuarios_metodos.auto_altas_procesadas "
                        "SET estado='failed', error=%s, updated_at=NOW() "
                        "WHERE pedido_id=%s AND linea_id=%s AND producto_id=%s",
                        (str(e), pedido_id, linea_id, producto_id)
                    )
                conn.commit()
            except Exception:
                pass
            return False
        finally:
            conn.close()
