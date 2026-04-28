import os
import json
import psycopg2
from psycopg2 import sql
import bcrypt

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
    "usuarios_metodos.usuarios_plataformas.json": ("usuarios_metodos", "usuarios_plataformas")
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
                "are_terms_accepted", "is_optional_checked", "disabled", "rol"
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
                else:
                    val = item.get(col)

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
    """Ejecuta la importación completa de todos los archivos configurados."""
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                for archivo, (esquema, tabla) in ARCHIVOS_A_IMPORTAR.items():
                    importar_archivo(cur, archivo, esquema, tabla)
                conn.commit()
                print("\n--- IMPORTACIÓN FINALIZADA CON ÉXITO ---")
    except Exception as e:
        print(f"\nERROR CRÍTICO EN LA IMPORTACIÓN: {e}")

if __name__ == "__main__":
    importar_todo()
