import os
import json
import psycopg2
from psycopg2 import sql
#No se muestran datos de historial en la db porque no se ha implementado la funcion de guardar historial
#No se ha definido un esquema
#
#

import os

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "db_personalidad_proyecto"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "Prefor2026!"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}


# Ruta relativa donde tienes tus archivos .json en la carpeta data
RUTA_DATOS = os.path.join(os.path.dirname(__file__), "data")


# Diccionario completo con todas las tablas del proyecto
ARCHIVOS_A_IMPORTAR = {
    "Personalidad.users.json": ("personalidad", "users"),
    "Personalidad.db_personalidad.json": ("personalidad", "db_personalidad"),
    "usuarios_metodos.plataformas_metodos.json": ("usuarios_metodos", "plataformas_metodos"),
    "usuarios_metodos.usuarios_plataformas.json": ("usuarios_metodos", "usuarios_plataformas"),
    "usuarios_metodos.actualizaciones_plataformas.json": ("usuarios_metodos", "actualizaciones_plataformas"),
    "psico_gc.enunciados_multiples.json": ("psico_gc", "enunciados_multiples"),
    "psico_gc.preguntas_normales.json": ("psico_gc", "preguntas_normales"),
    "psico_gc.preguntas_contestadas.json": ("psico_gc", "preguntas_contestadas"),
    "psico_gc.sesiones_contestadas.json": ("psico_gc", "sesiones_contestadas"),
    "python.users.json": ("python", "users"),
    
    "tecnicas_data.json": ("tecnicas", "tecnicas_data")
}


# Diccionario para tablas que no tienen JSON aún pero queremos crear su estructura
# (Esquema, {Columna: Tipo})
TABLAS_VACIAS = {
    "fisicas": ("historial_simplificado", {
        "token_simulacro": "TEXT PRIMARY KEY",
        "propietario_id": "TEXT",
        "simulacro_code": "TEXT",
        "resultado": "TEXT",
        "gender": "TEXT",
        "flexiones": "INTEGER",
        "plancha_seg": "INTEGER",
        "km2000": "INTEGER",
        "agilidad_seg": "FLOAT",
        "porcentaje": "TEXT",
        "fecha": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }),
    "personalidad": ("historial_simplificado", {
        "id": "TEXT PRIMARY KEY",
        "user_id": "TEXT",
        "sinceridad": "INTEGER",
        "extraversion": "INTEGER",
        "neuroticismo": "INTEGER",
        "psicoticismo": "INTEGER",
        "es_apto": "TEXT",
        "fecha": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    })
}


def importar_todo():
    try:
        print("--- INICIANDO IMPORTACIÓN TOTAL ---")
        conexion = psycopg2.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
        # Set datestyle to MDY to avoid errors with MM/DD/YYYY format dates
        cursor.execute("SET datestyle = 'ISO, MDY';")


        # 1. Procesar archivos JSON existentes
        for archivo, (esquema, tabla) in ARCHIVOS_A_IMPORTAR.items():
            ruta_completa = os.path.join(RUTA_DATOS, archivo)
           
            if not os.path.exists(ruta_completa):
                print(f"Saltando: No se encontró {archivo}")
                continue


            print(f"Procesando: {esquema}.{tabla}...")
           
            with open(ruta_completa, 'r', encoding='utf-8') as f:
                datos = json.load(f)
           
            if not datos:
                print(f"Empty: {archivo} no tiene datos.")
                continue
           
            # Normalizar: asegurar que datos sea una lista
            lista_datos = datos if isinstance(datos, list) else [datos]
           
            # Detectar columnas (excluyendo el _id de MongoDB para evitar conflictos)
            ejemplo = lista_datos[0]
            columnas = [k for k in ejemplo.keys() if k != '_id']

            # Crear Esquema y recrear Tabla con columnas reales
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {esquema};")
            cursor.execute(f"DROP TABLE IF EXISTS {esquema}.{tabla} CASCADE;")
            
            # Creamos las columnas. 'fecha' será TIMESTAMP, el resto TEXT
            columnas_def = []
            for col in columnas:
                if col == "fecha":
                    columnas_def.append(f'"{col}" TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                else:
                    columnas_def.append(f'"{col}" TEXT')
            
            columnas_sql = ", ".join(columnas_def)
            cursor.execute(f'CREATE TABLE {esquema}.{tabla} ({columnas_sql});')


            # Insertar los datos
            for item in lista_datos:
                # Convertir dicts/lists a strings JSON para que quepan en las columnas TEXT
                valores = []
                for col in columnas:
                    val = item.get(col)
                    if isinstance(val, (dict, list)):
                        valores.append(json.dumps(val))
                    else:
                        valores.append(str(val) if val is not None else None)
               
                query = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
                    sql.Identifier(esquema),
                    sql.Identifier(tabla),
                    sql.SQL(', ').join(map(sql.Identifier, columnas)),
                    sql.SQL(', ').join(sql.Placeholder() * len(columnas))
                )
                cursor.execute(query, valores)


            print(f"¡{esquema}.{tabla} lista!")


        # 2. Procesar tablas que solo quieren estructura (sin datos)
        print("\n--- CREANDO TABLAS DE ESTRUCTURA (SIN DATOS) ---")
        for tabla, (esquema, columnas) in TABLAS_VACIAS.items():
            print(f"Creando estructura: {esquema}.{tabla}...")
            
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {esquema};")
            cursor.execute(f"DROP TABLE IF EXISTS {esquema}.{tabla} CASCADE;")
            
            if isinstance(columnas, dict):
                columnas_sql = ", ".join([f'"{col}" {tipo}' for col, tipo in columnas.items()])
            else:
                columnas_sql = ", ".join([f'"{col}" TEXT' for col in columnas])
            
            cursor.execute(f'CREATE TABLE {esquema}.{tabla} ({columnas_sql});')
            
            print(f"¡{esquema}.{tabla} creada (vacía)!")


        conexion.commit()
        print("\n¡BASE DE DATOS COMPLETA! Todas las tablas están normalizadas.")


    except Exception as e:
        print(f"Error crítico: {e}")
    finally:
        if 'conexion' in locals():
            cursor.close()
            conexion.close()


if __name__ == "__main__":
    importar_todo()
