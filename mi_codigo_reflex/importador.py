import os
import json
import psycopg2
from psycopg2 import sql
from datetime import datetime

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "db_personalidad_proyecto"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "Prefor2026!"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

RUTA_DATOS = os.path.join(os.path.dirname(__file__), "data")

# Mapeo de archivos JSON a tablas
ARCHIVOS_A_IMPORTAR = {
    "Personalidad.users.json": ("personalidad", "users"),
    "Personalidad.db_personalidad.json": ("personalidad", "db_personalidad"),
    "usuarios_metodos.plataformas_metodos.json": ("usuarios_metodos", "plataformas_metodos"),
    "usuarios_metodos.usuarios_plataformas.json": ("usuarios_metodos", "usuarios_plataformas"),
    "psico_gc.enunciados_multiples.json": ("psico_gc", "enunciados_multiples"),
    "psico_gc.preguntas_normales.json": ("psico_gc", "preguntas_normales"),
    "python.users.json": ("python", "users"),
}

# Estructuras de tablas vacías (Historial)
TABLAS_VACIAS = {
    "fisicas": ("historial_simplificado", ["id", "user_id", "simulacro_code", "resultado", "gender", "flexiones", "plancha_seg", "km2000", "agilidad_seg", "porcentaje", "fecha"]),
    "personalidad": ("historial_simplificado", ["id", "user_id", "sinceridad", "extraversion", "neuroticismo", "psicoticismo", "es_apto", "fecha"])
}

def importar_todo():
    conexion = None
    try:
        print("--- INICIANDO IMPORTACIÓN TOTAL ---")
        conexion = psycopg2.connect(**DB_CONFIG)
        cursor = conexion.cursor()

        # 1. CREAR TABLAS DE ESTRUCTURA (Prioridad)
        print("\n--- 1. CREANDO TABLAS DE HISTORIAL ---")
        for tabla, (esquema, columnas) in TABLAS_VACIAS.items():
            print(f"Preparando: {esquema}.{tabla}...")
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {esquema};")
            cursor.execute(f"DROP TABLE IF EXISTS {esquema}.{tabla} CASCADE;")
            columnas_def = [f'"{col}" TEXT' for col in columnas if col != "fecha"]
            columnas_def.append('"fecha" TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            cursor.execute(f'CREATE TABLE {esquema}.{tabla} ({", ".join(columnas_def)});')
            print(f"¡{esquema}.{tabla} lista (vacía)!")

        # 2. IMPORTAR DATOS JSON
        print("\n--- 2. IMPORTANDO DATOS DESDE JSON ---")
        for archivo, (esquema, tabla) in ARCHIVOS_A_IMPORTAR.items():
            try:
                ruta_completa = os.path.join(RUTA_DATOS, archivo)
                if not os.path.exists(ruta_completa):
                    print(f"Saltando: {archivo} (No existe)")
                    continue

                print(f"Importando: {esquema}.{tabla}...")
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                if not datos: continue
                lista_datos = datos if isinstance(datos, list) else [datos]
                ejemplo = lista_datos[0]
                columnas = [k for k in ejemplo.keys() if k != '_id']

                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {esquema};")
                cursor.execute(f"DROP TABLE IF EXISTS {esquema}.{tabla} CASCADE;")
                
                cols_sql = []
                for col in columnas:
                    if col == "fecha": cols_sql.append(f'"{col}" TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                    else: cols_sql.append(f'"{col}" TEXT')
                
                cursor.execute(f'CREATE TABLE {esquema}.{tabla} ({", ".join(cols_sql)});')

                for item in lista_datos:
                    valores = []
                    for col in columnas:
                        val = item.get(col)
                        if isinstance(val, (dict, list)): valores.append(json.dumps(val))
                        else: valores.append(str(val) if val is not None else None)
                    
                    query = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
                        sql.Identifier(esquema), sql.Identifier(tabla),
                        sql.SQL(', ').join(map(sql.Identifier, columnas)),
                        sql.SQL(', ').join(sql.Placeholder() * len(columnas))
                    )
                    cursor.execute(query, valores)
                print(f"¡{esquema}.{tabla} completada!")

            except Exception as e:
                print(f"Error procesando {archivo}: {e} (saltando...)")
                conexion.rollback()

        conexion.commit()
        print("\n--- PROCESO FINALIZADO CON ÉXITO ---")

    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    importar_todo()
