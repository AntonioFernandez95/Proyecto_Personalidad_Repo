import os
from sqlalchemy import create_engine, text

# URL de la base de datos (ajustada para Docker localhost o service name si fuera necesario)
DATABASE_URL = "postgresql://postgres:Prefor2026!@localhost:5432/db_personalidad_proyecto"

def check_resources():
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM tecnicas.recursos"))
            rows = result.fetchall()
            print(f"\n--- RECURSOS ENCONTRADOS EN LA BD ({len(rows)}) ---")
            for row in rows:
                print(f"ID: {row[0]} | Nombre: {row[1]} | Tipo: {row[2]} | URL: {row[3]} | Categoría: {row[4]}")
            print("--------------------------------------------\n")
    except Exception as e:
        print(f"Error consultando la base de datos: {e}")

if __name__ == "__main__":
    check_resources()
