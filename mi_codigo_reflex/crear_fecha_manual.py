import os
import psycopg2
from Personalidad.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def crear_fecha_manual():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        
        print("Añadiendo columna 'fecha' a recursos.videos...")
        cur.execute("ALTER TABLE recursos.videos ADD COLUMN IF NOT EXISTS fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
        
        print("Añadiendo columna 'fecha' a recursos.pdfs...")
        cur.execute("ALTER TABLE recursos.pdfs ADD COLUMN IF NOT EXISTS fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
        
        conn.commit()
        cur.close()
        conn.close()
        print("Columnas 'fecha' creadas correctamente.")
    except Exception as e:
        print(f"Error al crear las columnas: {e}")

if __name__ == "__main__":
    crear_fecha_manual()
