import os
import pymysql

host = os.getenv('ORDERS_DB_HOST')
port = int(os.getenv('ORDERS_DB_PORT', '3306'))
user = os.getenv('ORDERS_DB_USER')
password = os.getenv('ORDERS_DB_PASSWORD')
dbname = os.getenv('ORDERS_DB_NAME')

try:
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=dbname, connect_timeout=5)
    print('✅ Conexión a MySQL exitosa')
    conn.close()
except Exception as e:
    print('❌ Error de conexión a MySQL:', e)
