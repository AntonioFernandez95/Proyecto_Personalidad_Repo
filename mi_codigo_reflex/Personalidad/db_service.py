import os
import psycopg2
from psycopg2 import sql

# Configuración centralizada
# Nota: "db" es el nombre del servicio en Docker. 
# Si lo ejecutas localmente fuera de Docker, podrías necesitar "localhost"
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
        print(f"ERROR DE CONEXIÓN DB: {e}")
        return None
