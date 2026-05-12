import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "db_personalidad_proyecto")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Prefor2026!")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

def fix_types():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST, 
            port=DB_PORT
        )
        cur = conn.cursor()
        
        print("Actualizando tipos en la tabla de vídeos...")
        cur.execute("UPDATE recursos.videos SET tipo = 'video' WHERE tipo IS NULL OR tipo = '';")
        
        print("Actualizando tipos en la tabla de PDFs...")
        cur.execute("UPDATE recursos.pdfs SET tipo = 'pdf' WHERE tipo IS NULL OR tipo = '';")
        
        conn.commit()
        print(f"Filas actualizadas: {cur.rowcount}")
        cur.close()
        conn.close()
        print("Corrección completada con éxito.")
    except Exception as e:
        print(f"Error al corregir la base de datos: {e}")

if __name__ == "__main__":
    fix_types()
