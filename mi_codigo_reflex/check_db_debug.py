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

        # 2. Verificar si existe la tabla
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'historial_simplificado' AND table_name = 'registrosCalculadoraFisicas'")
        if not cur.fetchone():
            print("ERROR: La tabla 'registrosCalculadoraFisicas' NO EXISTE en el esquema.")
            print("SOLUCIÓN: Ejecuta 'python importador.py'")
            return

        # 3. Contar registros
        cur.execute('SELECT COUNT(*) FROM historial_simplificado."registrosCalculadoraFisicas"')
        count = cur.fetchone()[0]
        print(f"Número de registros encontrados: {count}")
        
        if count > 0:
            print("\nÚltimos 3 registros:")
            cur.execute('SELECT fecha, user_id, resultado FROM historial_simplificado."registrosCalculadoraFisicas" ORDER BY fecha DESC LIMIT 3')
            for r in cur.fetchall():
                print(f" - {r[0]} | Usuario: {r[1]} | Resultado: {r[2]}")
        else:
            print("\nAVISO: La tabla está vacía. Intenta usar la calculadora ahora.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    check()
