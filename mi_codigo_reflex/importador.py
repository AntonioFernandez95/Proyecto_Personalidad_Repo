import os
import json
import psycopg2
from psycopg2 import sql
import bcrypt
from datetime import datetime, timedelta

# Importamos la configuración centralizada
try:
    from Personalidad.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
except ImportError:
    # Fallback por si se ejecuta desde un entorno donde el paquete no está accesible
    DB_NAME = os.getenv("DB_NAME", "db_personalidad_proyecto")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Prefor2026!")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

RUTA_DATOS = os.path.join(os.path.dirname(__file__), "data")

ARCHIVOS_A_IMPORTAR = {
    "Personalidad.users.json": ("personalidad", "users"),
    "Personalidad.db_personalidad.json": ("personalidad", "db_personalidad"),
    "usuarios_metodos.plataformas_metodos.json": ("usuarios_metodos", "plataformas_metodos"),
    "usuarios_metodos.usuarios_plataformas.json": ("usuarios_metodos", "usuarios_plataformas"),
    "recursos_videos.json": ("recursos", "videos"),
    "recursos_pdfs.json": ("recursos", "pdfs"),
    "tecnicas_data.json": ("tecnicas", "tecnicas_data")
}

def obtener_conexion():
    """Establece conexión con PostgreSQL usando la config centralizada."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def importar_archivo(cursor, nombre_archivo, esquema, tabla):
    """Procesa e importa un archivo JSON individual a una tabla específica."""
    ruta_completa = os.path.join(RUTA_DATOS, nombre_archivo)
    if not os.path.exists(ruta_completa):
        print(f"Saltando {nombre_archivo}: No existe.")
        return

    print(f"Importando {nombre_archivo} -> {esquema}.{tabla}...")
    with open(ruta_completa, 'r', encoding='utf-8') as f:
        datos = json.load(f)
        lista_datos = datos if isinstance(datos, list) else [datos]

        if not lista_datos:
            return

        # Definición de columnas
        columnas_originales = list(lista_datos[0].keys())
        es_tabla_usuarios = (esquema == "usuarios_metodos" and tabla == "usuarios_plataformas")
        
        if es_tabla_usuarios:
            columnas = [
                "nombre", "apellidos", "dni", "email", "password", 
                "pedido", "desde", "hasta", "count_login", 
                "are_terms_accepted", "is_optional_checked", "disabled", "rol",
                "disabled_personalidad", "disabled_fisicas"
            ]
        else:
            columnas = columnas_originales

        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {esquema};")
        cursor.execute(f"DROP TABLE IF EXISTS {esquema}.{tabla} CASCADE;")
        
        columnas_def = []
        for col in columnas:
            if col in ["fecha", "desde", "hasta"]:
                columnas_def.append(f'"{col}" TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            elif col in ["count_login", "pedido"]:
                columnas_def.append(f'"{col}" INTEGER DEFAULT 0')
            elif col in ["are_terms_accepted", "disabled", "is_optional_checked"]:
                columnas_def.append(f'"{col}" BOOLEAN DEFAULT TRUE')
            elif col == "rol":
                columnas_def.append(f'"{col}" TEXT DEFAULT \'estudiante\'')
            else:
                columnas_def.append(f'"{col}" TEXT')
        
        cursor.execute(f"CREATE TABLE {esquema}.{tabla} ({', '.join(columnas_def)});")
        
        for item in lista_datos:
            # Filtro de seguridad (solo academia para la tabla principal)
            if es_tabla_usuarios:
                email = str(item.get("email", "")).lower()
                if not email.endswith("@academiametodos.com"):
                    continue

            valores = []
            for col in columnas:
                if col == "password" and es_tabla_usuarios:
                    raw_pass = str(item.get("password", ""))
                    if raw_pass.startswith("$2") and len(raw_pass) >= 59:
                        val = raw_pass
                    else:
                        val = bcrypt.hashpw(raw_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                elif col == "rol" and es_tabla_usuarios:
                    email_item = str(item.get("email", "")).lower()
                    val = "admin" if email_item.endswith("@academiametodos.com") else "estudiante"
                elif col == "apellidos" and es_tabla_usuarios:
                    # Combinamos apellido1 y apellido2 si existen
                    ap1 = item.get("apellido1", "")
                    ap2 = item.get("apellido2", "")
                    val = f"{ap1} {ap2}".strip()
                else:
                    val = item.get(col)
                    # Fallback para campos con nombres alternativos en el JSON
                    if val is None:
                        if col == "count_login": val = item.get("count_login", 0)
                        elif col == "are_terms_accepted": val = item.get("are_terms_accepted", False)
                        elif col == "is_optional_checked": val = item.get("is_optional_checked", True)

                if isinstance(val, (dict, list)):
                    valores.append(json.dumps(val))
                else:
                    valores.append(str(val) if val is not None else None)
           
            query = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
                sql.Identifier(esquema), sql.Identifier(tabla),
                sql.SQL(', ').join(map(sql.Identifier, columnas)),
                sql.SQL(', ').join(sql.Placeholder() * len(columnas))
            )
            cursor.execute(query, valores)

def importar_todo():
    """Ejecuta la importación completa con fusión de datos de usuarios."""
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                # 0. Asegurar esquema y tablas de recursos REALES (recursos.videos y recursos.pdfs)
                print("Verificando esquema 'recursos' y tablas 'videos'/'pdfs'...")
                cur.execute("CREATE SCHEMA IF NOT EXISTS recursos;")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS recursos.videos (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        url TEXT NOT NULL,
                        categoria TEXT NOT NULL,
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS recursos.pdfs (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        url TEXT NOT NULL,
                        categoria TEXT NOT NULL,
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
                print("Tablas de recursos listas.")

                # 1. PRE-PROCESAMIENTO: Fusión de datos de usuarios
                usuarios_maestros = {}
                
                archivos_usuarios = [
                    "Personalidad.users.json",
                    "usuarios_metodos.usuarios_plataformas.json"
                ]
                
                for nombre_archivo in archivos_usuarios:
                    ruta = os.path.join(RUTA_DATOS, nombre_archivo)
                    if os.path.exists(ruta):
                        with open(ruta, 'r', encoding='utf-8') as f:
                            datos = json.load(f)
                            for item in (datos if isinstance(datos, list) else [datos]):
                                email = str(item.get("email", "")).lower()
                                if not email or not email.endswith("@academiametodos.com"):
                                    continue
                                
                                if email not in usuarios_maestros:
                                    usuarios_maestros[email] = {}
                                
                                # Fusionar campos (priorizando valores no nulos)
                                for k, v in item.items():
                                    if v is not None and v != "":
                                        usuarios_maestros[email][k] = v
                                        
                # 2. IMPORTACIÓN DE TABLAS NORMALES
                for archivo, (esquema, tabla) in ARCHIVOS_A_IMPORTAR.items():
                    if tabla == "usuarios_plataformas":
                        continue # La procesamos luego con la fusión
                    importar_archivo(cur, archivo, esquema, tabla)
                
                # 3. IMPORTACIÓN DE LA TABLA DE USUARIOS FUSIONADA
                print("Importando tabla de usuarios fusionada...")
                esquema, tabla = "usuarios_metodos", "usuarios_plataformas"
                columnas = [
                    "nombre", "apellidos", "dni", "email", "password", 
                    "pedido", "desde", "hasta", "count_login", 
                    "are_terms_accepted", "is_optional_checked", "disabled", "rol",
                    "disabled_personalidad", "disabled_fisicas"
                ]
                
                cur.execute(f"CREATE SCHEMA IF NOT EXISTS {esquema};")
                cur.execute(f"DROP TABLE IF EXISTS {esquema}.{tabla} CASCADE;")
                
                # Definición de tabla (simplificada para brevedad, igual que antes)
                columnas_def = []
                for col in columnas:
                    if col in ["desde", "hasta"]: columnas_def.append(f'"{col}" TIMESTAMP')
                    elif col in ["count_login", "pedido"]: columnas_def.append(f'"{col}" INTEGER DEFAULT 0')
                    elif col in ["are_terms_accepted", "disabled", "is_optional_checked"]: columnas_def.append(f'"{col}" BOOLEAN DEFAULT TRUE')
                    elif col == "rol": columnas_def.append(f'"{col}" TEXT DEFAULT \'estudiante\'')
                    else: columnas_def.append(f'"{col}" TEXT')
                
                cur.execute(f"CREATE TABLE {esquema}.{tabla} ({', '.join(columnas_def)});")
                
                for email, info in usuarios_maestros.items():
                    # Preparar valores con lógica de mapeo
                    nombre = info.get("nombre", info.get("full_name", email.split("@")[0]))
                    ap1 = info.get("apellido1", "")
                    ap2 = info.get("apellido2", "")
                    apellidos = info.get("apellidos", f"{ap1} {ap2}".strip())
                    
                    pw = str(info.get("password", "123456"))
                    # Detectar si ya es un hash de bcrypt ($2a$, $2b$, $2y$)
                    is_already_hashed = pw.startswith("$2") and len(pw) >= 50
                    if not is_already_hashed:
                        pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                    desde = info.get("desde") or datetime.now()
                    hasta = info.get("hasta") or (datetime.now() + timedelta(days=30))

                    valores = [
                        nombre, apellidos, info.get("dni"), email, pw,
                        info.get("pedido", 0), desde, hasta,
                        info.get("count_login", 0), 
                        info.get("are_terms_accepted", False),
                        info.get("is_optional_checked", True),
                        info.get("disabled", False),
                        "admin" if email.endswith("@academiametodos.com") else "estudiante",
                        info.get("disabled_personalidad", False),
                        info.get("disabled_fisicas", False)
                    ]
                    
                    query = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
                        sql.Identifier(esquema), sql.Identifier(tabla),
                        sql.SQL(', ').join(map(sql.Identifier, columnas)),
                        sql.SQL(', ').join(sql.Placeholder() * len(columnas))
                    )
                    cur.execute(query, valores)

                conn.commit()
                print("\n--- IMPORTACIÓN MAESTRA FINALIZADA CON ÉXITO ---")
    except Exception as e:
        print(f"\nERROR CRÍTICO: {e}")

if __name__ == "__main__":
    importar_todo()
