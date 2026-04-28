import psycopg2
from psycopg2.extras import RealDictCursor
from Personalidad.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

class PostgresClient:
    def __init__(self, default_schema="public"):
        self.default_schema = default_schema

    def _get_connection(self):
        """Crea y devuelve una nueva conexión a PostgreSQL."""
        try:
            return psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
        except Exception as e:
            # Fallback para desarrollo local fuera de Docker
            if DB_HOST != "localhost":
                try:
                    return psycopg2.connect(
                        dbname=DB_NAME,
                        user=DB_USER,
                        password=DB_PASSWORD,
                        host="localhost",
                        port=DB_PORT
                    )
                except Exception as inner_e:
                    print(f"Error fatal conectando a PostgreSQL: {inner_e}")
                    raise
            raise e

    def _get_full_table_name(self, table):
        """Asegura que el nombre de la tabla incluya el esquema."""
        if "." in table:
            return table
        return f"{self.default_schema}.{table}"

    def find_one(self, table, query_field, query_value):
        """Busca un único registro que coincida con el campo y valor dado."""
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
        """Actualiza un registro existente."""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                table_name = self._get_full_table_name(table)
                fields = list(update_dict.keys())
                values = [update_dict[f] for f in fields]
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

    def delete_one(self, table, query_field, query_value):
        """Elimina un registro de la tabla."""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                table_name = self._get_full_table_name(table)
                sql = f'DELETE FROM {table_name} WHERE "{query_field}" = %s'
                cur.execute(sql, (str(query_value),))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error en delete_one ({table}): {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def find_all(self, table):
        """Devuelve todos los registros de una tabla."""
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

# Instancia global para la aplicación
# Usamos el esquema 'usuarios_metodos' como base para evitar confusiones
db_client = PostgresClient("usuarios_metodos")