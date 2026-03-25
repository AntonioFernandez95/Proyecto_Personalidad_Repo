import os
import json
import pandas as pd
from sqlalchemy import create_engine, text

# La URL se toma del entorno definido en docker-compose
DB_URL = os.getenv("DATABASE_URL")
DATA_DIR = "./data"

def cargar():
    if not DB_URL:
        print("DATABASE_URL no definida. Saltando migración.")
        return

    engine = create_engine(DB_URL)
    if not os.path.exists(DATA_DIR):
        print(f"Carpeta {DATA_DIR} no encontrada.")
        return

    with engine.connect() as conn:
        for archivo in os.listdir(DATA_DIR):
            if archivo.endswith(".json"):
                tabla = archivo.replace(".json", "").lower()
                print(f"Migrando {archivo} a Postgres (JSONB)...")
                
                with open(os.path.join(DATA_DIR, archivo), 'r', encoding='utf-8') as f:
                    documentos = json.load(f)
                
                conn.execute(text(f"DROP TABLE IF EXISTS {tabla};"))
                conn.execute(text(f"CREATE TABLE {tabla} (id SERIAL PRIMARY KEY, data JSONB);"))
                
                for doc in documentos:
                    conn.execute(
                        text(f"INSERT INTO {tabla} (data) VALUES (:d)"),
                        {"d": json.dumps(doc)}
                    )
                conn.commit()
    print("✅ Migración jerárquica completada.")

if __name__ == "__main__":
    cargar()