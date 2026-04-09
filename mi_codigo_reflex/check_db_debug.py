import psycopg2
import os

DB_CONFIG = {
    "dbname": "db_personalidad_proyecto",
    "user": "postgres",
    "password": "Prefor2026!",
    "host": "localhost",
    "port": "5432"
}

def check():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("--- ESTADO DE LA BASE DE DATOS ---")
        
        # 1. Verificar si existe el esquema
        cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'historial_simplificado'")
        if not cur.fetchone():
            print("ERROR: El esquema 'historial_simplificado' NO EXISTE.")
            print("SOLUCIÓN: Ejecuta 'python importador.py'")
            return

        # 2. Verificar si existe la tabla fisica (ya estaba)
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'historial_simplificado' AND table_name = 'fisicas'")
        if cur.fetchone():
            cur.execute('SELECT COUNT(*) FROM historial_simplificado.fisicas')
            count = cur.fetchone()[0]
            print(f"Registros en FISICAS: {count}")
            if count > 0:
                cur.execute('SELECT fecha, user_id, resultado FROM historial_simplificado.fisicas ORDER BY fecha DESC LIMIT 2')
                for r in cur.fetchall():
                    print(f" - {r[0]} | Usuario: {r[1]} | Res: {r[2]}")
        else:
            print("AVISO: Tabla 'fisicas' NO existe.")

        print("-" * 30)

        # 3. Verificar si existe la tabla personalidad
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'historial_simplificado' AND table_name = 'personalidad'")
        if cur.fetchone():
            cur.execute('SELECT COUNT(*) FROM historial_simplificado.personalidad')
            count = cur.fetchone()[0]
            print(f"Registros en PERSONALIDAD: {count}")
            if count > 0:
                cur.execute('SELECT fecha, user_id, es_apto FROM historial_simplificado.personalidad ORDER BY fecha DESC LIMIT 3')
                for r in cur.fetchall():
                    print(f" - {r[0]} | Usuario: {r[1]} | Res: {r[2]}")
        else:
            print("ERROR: La tabla 'personalidad' NO EXISTE.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    check()
