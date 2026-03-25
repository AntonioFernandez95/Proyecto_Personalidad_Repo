import psycopg2
from psycopg2.extras import RealDictCursor
import os

class PostgresClient:
    def __init__(self, schema):
        self.schema = schema

    def _get_connection(self):
        # Usamos las credenciales de variables de entorno o defaults
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME", "db_personalidad_proyecto"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "Prefor2026!"),
            host=os.getenv("DB_HOST", "db"),
            port=os.getenv("DB_PORT", "5432")
        )

    def _get_full_table_name(self, table):
        if "." in table:
            return table
        return f"{self.schema}.{table}"

    def find_one(self, table, query_field, query_value):
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                table_name = self._get_full_table_name(table)
                sql = f'SELECT * FROM {table_name} WHERE "{query_field}" = %s LIMIT 1'
                cur.execute(sql, (str(query_value),))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"Error en find_one ({table}): {e}")
            return None
        finally:
            conn.close()

    def update_one(self, table, query_field, query_value, update_dict):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                table_name = self._get_full_table_name(table)
                fields = list(update_dict.keys())
                values = [str(update_dict[f]) for f in fields]
                set_query = ", ".join([f'"{f}" = %s' for f in fields])
                
                sql = f'UPDATE {table_name} SET {set_query} WHERE "{query_field}" = %s'
                cur.execute(sql, values + [str(query_value)])
                conn.commit()
                return True
        except Exception as e:
            print(f"Error en update_one ({table}): {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def find_all(self, table):
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                table_name = self._get_full_table_name(table)
                sql = f'SELECT * FROM {table_name}'
                cur.execute(sql)
                resultados = cur.fetchall()
                return [dict(r) for r in resultados]
        except Exception as e:
            print(f"Error en find_all ({table}): {e}")
            return []
        finally:
            conn.close()

# Instancias
db_client = PostgresClient("public")
personalidad_db_client = PostgresClient("public")
python_db_client = PostgresClient("public")