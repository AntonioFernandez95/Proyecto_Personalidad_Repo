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
    host = os.getenv("DB_HOST", "db")
    try:
        # DB_CONFIG ya tiene host="db" pero lo pasaremos explícito para el fallback
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=host,
            port=DB_CONFIG["port"]
        )
        return conn
    except Exception as e:
        if host != "localhost":
            try:
                conn = psycopg2.connect(
                    dbname=DB_CONFIG["dbname"],
                    user=DB_CONFIG["user"],
                    password=DB_CONFIG["password"],
                    host="localhost",
                    port=DB_CONFIG["port"]
                )
                return conn
            except Exception as inner_e:
                print(f"ERROR DE CONEXIÓN DB (LOCAL): {inner_e}")
                return None
        print(f"ERROR DE CONEXIÓN DB: {e}")
        return None

def guardar_resultado_personalidad(data: dict) -> bool:
    """Guarda en BD el resultado final del test."""
    try:
        conn = get_db_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        insert_query = sql.SQL(
            "INSERT INTO historial_simplificado.personalidad (id, user_id, sinceridad, extraversion, neuroticismo, psicoticismo, es_apto) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        
        cursor.execute(insert_query, (
            data.get('id'),
            data.get('user_id'),
            data.get('sinceridad'),
            data.get('extraversion'),
            data.get('neuroticismo'),
            data.get('psicoticismo'),
            data.get('es_apto')
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error guardando en BD (personalidad): {e}")

def obtener_resultados_personalidad(user_id: str) -> list[dict]:
    """Recupera los resultados previos de un usuario de la BD."""
    try:
        conn = get_db_connection()
        if not conn: return []
        cursor = conn.cursor()
        
        # Seleccionamos las columnas principales incluyendo la fecha
        select_query = sql.SQL(
            "SELECT id, sinceridad, extraversion, neuroticismo, psicoticismo, es_apto, fecha "
            "FROM historial_simplificado.personalidad "
            "WHERE user_id = %s "
            "ORDER BY fecha DESC"
        )
        
        cursor.execute(select_query, (user_id,))
        rows = cursor.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append({
                "id": row[0],
                "sinceridad": row[1],
                "extraversion": row[2],
                "neuroticismo": row[3],
                "psicoticismo": row[4],
                "es_apto": row[5],
                "fecha": row[6].strftime("%d/%m/%Y %H:%M") if row[6] else "N/A"
            })
            
        cursor.close()
        conn.close()
        return resultados
    except Exception as e:
        print(f"Error obteniendo historial en BD (personalidad): {e}")
        return []
