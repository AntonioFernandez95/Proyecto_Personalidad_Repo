
import psycopg2
conn = psycopg2.connect(dbname='db_personalidad_proyecto', user='postgres', password='Prefor2026!', host='localhost', port='5432')
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='usuarios_plataformas'")
print([r[0] for r in cur.fetchall()])

