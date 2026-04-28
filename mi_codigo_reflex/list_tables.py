import psycopg2
import os

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "db_personalidad_proyecto"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "Prefor2026!"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    cur = conn.cursor()
    cur.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog')")
    tables = cur.fetchall()
    print("Tables found:")
    for schema, name in tables:
        print(f" - {schema}.{name}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
