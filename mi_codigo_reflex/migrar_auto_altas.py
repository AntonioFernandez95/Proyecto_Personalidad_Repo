"""
Script de migración: crea la tabla auto_altas_procesadas en usuarios_metodos.
Ejecutar UNA SOLA VEZ en el servidor para preparar la BD.

Uso local:
    python migrar_auto_altas.py

Uso en producción (dentro del contenedor):
    docker compose -p tropa-fase2 exec -T backend python migrar_auto_altas.py
"""
import os
import psycopg2

# Configuración — lee del entorno o usa los valores por defecto del proyecto
DB_CONFIG = {
    "dbname":   os.getenv("DB_NAME",     "db_personalidad_proyecto"),
    "user":     os.getenv("DB_USER",     "postgres"),
    "password": os.getenv("DB_PASSWORD", "Prefor2026!"),
    "host":     os.getenv("DB_HOST",     "db"),      # 'db' dentro de Docker, 'localhost' fuera
    "port":     os.getenv("DB_PORT",     "5432"),
}

SQL_MIGRACION = """
-- 1. Esquema
CREATE SCHEMA IF NOT EXISTS usuarios_metodos;

-- 2. Tabla de control de altas
CREATE TABLE IF NOT EXISTS usuarios_metodos.auto_altas_procesadas (
    id                BIGSERIAL    PRIMARY KEY,
    pedido_id         VARCHAR(100) NOT NULL,
    linea_id          VARCHAR(100) NOT NULL,
    producto_id       VARCHAR(50)  NOT NULL,
    email             VARCHAR(255) NOT NULL,
    estado            VARCHAR(20)  NOT NULL DEFAULT 'processing'
                          CHECK (estado IN ('processing', 'processed', 'failed')),
    intentos          INT          NOT NULL DEFAULT 0,
    error             TEXT         NULL,
    usuario_id        VARCHAR(255) NULL,
    fecha_inicio      TIMESTAMP    NULL,
    fecha_vencimiento TIMESTAMP    NULL,
    created_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_pedido_linea_producto UNIQUE (pedido_id, linea_id, producto_id)
);

-- 3. Índices
CREATE INDEX IF NOT EXISTS idx_auto_altas_estado
    ON usuarios_metodos.auto_altas_procesadas (estado);

CREATE INDEX IF NOT EXISTS idx_auto_altas_email
    ON usuarios_metodos.auto_altas_procesadas (email);
"""

SQL_COLUMNAS_USUARIOS = [
    ("hasta_personalidad",    "TIMESTAMP"),
    ("hasta_fisicas",         "TIMESTAMP"),
    ("disabled_personalidad", "BOOLEAN DEFAULT TRUE"),
    ("disabled_fisicas",      "BOOLEAN DEFAULT TRUE"),
]


def migrar():
    print("=" * 60)
    print(" MIGRACIÓN: Sistema de Auto-Altas")
    print("=" * 60)

    # Intentar conexión — primero con el host del .env, luego localhost como fallback
    conn = None
    for host in [DB_CONFIG["host"], "localhost"]:
        try:
            conn = psycopg2.connect(
                dbname=DB_CONFIG["dbname"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                host=host,
                port=DB_CONFIG["port"],
            )
            print(f"[OK] Conectado a PostgreSQL en {host}:{DB_CONFIG['port']}")
            break
        except Exception as e:
            print(f"[WARN] No se pudo conectar a {host}: {e}")

    if conn is None:
        print("[ERROR] No se pudo establecer conexión. Abortando.")
        return False

    try:
        cur = conn.cursor()

        # Crear tabla de control
        print("\n[1/3] Creando tabla auto_altas_procesadas...")
        cur.execute(SQL_MIGRACION)
        print("      ✓ Tabla creada (o ya existía).")

        # Asegurar columnas de vencimiento en usuarios_plataformas
        print("\n[2/3] Verificando columnas en usuarios_plataformas...")
        for columna, tipo in SQL_COLUMNAS_USUARIOS:
            cur.execute("""
                SELECT 1 FROM information_schema.columns
                WHERE table_schema = 'usuarios_metodos'
                  AND table_name   = 'usuarios_plataformas'
                  AND column_name  = %s
            """, (columna,))
            if cur.fetchone():
                print(f"      ✓ Columna '{columna}' ya existe.")
            else:
                cur.execute(
                    f"ALTER TABLE usuarios_metodos.usuarios_plataformas "
                    f"ADD COLUMN IF NOT EXISTS {columna} {tipo};"
                )
                print(f"      + Columna '{columna}' creada.")

        conn.commit()

        # Verificación final
        print("\n[3/3] Verificando resultado en la BD...")
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'usuarios_metodos'
              AND table_name   = 'auto_altas_procesadas'
            ORDER BY ordinal_position;
        """)
        columnas = cur.fetchall()
        print(f"\n      Tabla 'usuarios_metodos.auto_altas_procesadas' — {len(columnas)} columnas:")
        for col_name, col_type in columnas:
            print(f"        • {col_name:<22} {col_type}")

        cur.close()
        print("\n[✓] MIGRACIÓN COMPLETADA CON ÉXITO.")
        return True

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Fallo durante la migración: {e}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    migrar()
