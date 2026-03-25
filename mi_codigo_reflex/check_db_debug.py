import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "db_personalidad_proyecto",
    "user": "postgres",
    "password": "Prefor2026!",
    "host": "localhost",
    "port": "5432"
}

def check_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Ver esquemas
            cur.execute("SELECT schema_name FROM information_schema.schemata")
            schemas = cur.fetchall()
            print("Esquemas disponibles:", [s['schema_name'] for s in schemas])

            # Ver tablas en el esquema personalidad
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'personalidad'")
            tables = cur.fetchall()
            print("Tablas en 'personalidad':", [t['table_name'] for t in tables])

            # Ver los últimos usuarios insertados con detalle
            cur.execute("SELECT id, data FROM personalidad.users ORDER BY id DESC LIMIT 2")
            users = cur.fetchall()
            print("\nDetalle de los últimos 2 registros:")
            for u in users:
                data = u.get('data')
                print(f"\nID: {u.get('id')}")
                print(f"Campos presentes: {list(data.keys()) if data else 'None'}")
                print(f"Email: {data.get('email')}")
                print(f"Full JSON: {data}")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
