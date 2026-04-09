import os
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Configuración centralizada
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "db_personalidad_proyecto"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "Prefor2026!"),
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_db_connection():
    """Retorna una conexión directa a PostgreSQL usando psycopg2."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        # Intento fallback a localhost si falla 'db' (útil en desarrollo local)
        try:
            temp_config = DB_CONFIG.copy()
            temp_config["host"] = "localhost"
            return psycopg2.connect(**temp_config)
        except:
            print(f"ERROR DE CONEXIÓN DB: {e}")
            return None

def guardar_resultado_fisicas(data: dict):
    """Guarda un registro de pruebas físicas en historial_simplificado.fisicas"""
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        columnas = list(data.keys())
        valores = [data[col] for col in columnas]
        
        query = sql.SQL("INSERT INTO historial_simplificado.fisicas ({}) VALUES ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, columnas)),
            sql.SQL(', ').join(sql.Placeholder() * len(columnas))
        )
        cur.execute(query, valores)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error guardando físicas: {e}")
        return False
    finally:
        conn.close()

def guardar_resultado_personalidad(data: dict):
    """Guarda un resultado de personalidad en historial_simplificado.personalidad"""
    conn = get_db_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        # Aseguramos la fecha si no viene
        if "fecha" not in data:
            data["fecha"] = datetime.now()
            
        columnas = list(data.keys())
        valores = [data[col] for col in columnas]
        
        query = sql.SQL("INSERT INTO historial_simplificado.personalidad ({}) VALUES ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, columnas)),
            sql.SQL(', ').join(sql.Placeholder() * len(columnas))
        )
        cur.execute(query, valores)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error guardando personalidad en DB: {e}")
        # Intentamos imprimir más detalles si es un error de psycopg2
        if hasattr(e, 'pgerror'):
            print(f"DETALLE PG: {e.pgerror}")
        return False
    finally:
        conn.close()
