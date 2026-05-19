"""
Lector de pedidos de la BD externa MySQL (WooCommerce/gestion).
Extrae compras de hoy y ayer para los 4 productos configurados
y las devuelve sanitizadas al motor de auto-altas.
"""
import os
import datetime
import pymysql
from pymysql.cursors import DictCursor

# IDs de producto que generan altas automáticas
PRODUCT_IDS = ("380893", "396346", "396348", "396350")


class OrdersReader:

    def __init__(self):
        self.host     = os.getenv("ORDERS_DB_HOST",     "82.223.68.173")
        self.port     = int(os.getenv("ORDERS_DB_PORT", "3306"))
        self.db       = os.getenv("ORDERS_DB_NAME",     "gestion")
        self.user     = os.getenv("ORDERS_DB_USER",     "usuOzein")
        self.password = os.getenv("ORDERS_DB_PASSWORD", "Ozy.rul3s.cl0ud")

    def _conn(self):
        return pymysql.connect(
            host=self.host, port=self.port, database=self.db,
            user=self.user, password=self.password,
            cursorclass=DictCursor, connect_timeout=10
        )

    # ------------------------------------------------------------------
    # AUDITORÍA (ejecutar una sola vez para mapear columnas reales)
    # ------------------------------------------------------------------
    def audit_schema(self):
        """Muestra estructura de tablas WooCommerce. Solo lectura."""
        print("\n=== AUDITORÍA DE ESQUEMA BD EXTERNA ===")
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                # Tablas personalizadas (intentar primero)
                for tabla in ["woo_orders_items_todos", "woo_orders_items"]:
                    try:
                        cur.execute(f"DESCRIBE {tabla};")
                        cols = cur.fetchall()
                        print(f"\n--- DESCRIBE {tabla} ---")
                        for c in cols:
                            print(f"  {c.get('Field'):<30} {c.get('Type')}")
                        cur.execute(f"SELECT * FROM {tabla} LIMIT 2;")
                        for r in cur.fetchall():
                            print(f"  Ejemplo: {dict(r)}")
                    except Exception as e:
                        print(f"  [WARN] {tabla}: {e}")

                # Estados reales de WooCommerce
                cur.execute("""
                    SELECT DISTINCT post_status, COUNT(*) AS total
                    FROM mcfi_posts
                    WHERE post_type = 'shop_order'
                    GROUP BY post_status ORDER BY total DESC LIMIT 10;
                """)
                print("\n--- Estados reales de pedidos WooCommerce ---")
                for r in cur.fetchall():
                    print(f"  {r.get('post_status'):<25}  total={r.get('total')}")

                # Metadatos de un pedido para mapear campos
                cur.execute("""
                    SELECT pm.meta_key, pm.meta_value
                    FROM mcfi_postmeta pm
                    JOIN mcfi_posts p ON p.ID = pm.post_id
                    WHERE p.post_type = 'shop_order'
                      AND pm.meta_key IN (
                        '_billing_email','_billing_first_name','_billing_last_name',
                        '_billing_phone','_order_total','_payment_method'
                      )
                    LIMIT 12;
                """)
                print("\n--- Metadatos de pedido (campos de facturación) ---")
                for r in cur.fetchall():
                    print(f"  {r.get('meta_key'):<35} {r.get('meta_value')}")

        except Exception as e:
            print(f"[AUDIT ERROR] {e}")
        finally:
            conn.close()
        print("\n=== FIN AUDITORÍA ===")

    # ------------------------------------------------------------------
    # EXTRACCIÓN — Estrategia A: tabla personalizada woo_orders_items_todos
    # ------------------------------------------------------------------
    def _fetch_custom_table(self, desde: datetime.datetime) -> list:
        """
        Intenta usar woo_orders_items_todos (tabla pre-agregada).
        Los nombres de columna se ajustan TRAS ejecutar audit_schema().
        """
        query = """
            SELECT
                order_id      AS pedido_id,
                item_id       AS linea_id,
                product_id    AS producto_id,
                billing_email AS email,
                first_name    AS nombre,
                last_name     AS apellidos,
                date_created  AS created_at,
                status        AS estado
            FROM woo_orders_items_todos
            WHERE date_created >= %s
              AND status IN ('wc-completed','wc-processing','completed','processing','paid')
              AND product_id IN %s;
        """
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, (desde, PRODUCT_IDS))
                rows = cur.fetchall()
                print(f"[ORDERS] {len(rows)} registros desde woo_orders_items_todos.")
                return list(rows)
        except Exception as e:
            print(f"[ORDERS] woo_orders_items_todos no disponible: {e}")
            return []
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # EXTRACCIÓN — Estrategia B: tablas nativas WooCommerce (mcfi_*)
    # ------------------------------------------------------------------
    def _fetch_woocommerce_native(self, desde: datetime.datetime) -> list:
        """
        Query nativa sobre mcfi_posts + mcfi_postmeta + mcfi_woocommerce_order_items.
        Fallback automático si woo_orders_items_todos no tiene los campos necesarios.
        """
        query = """
            SELECT
                p.ID AS pedido_id,
                oi.order_item_id AS linea_id,
                MAX(CASE WHEN im.meta_key = '_product_id'         THEN im.meta_value END) AS producto_id,
                MAX(CASE WHEN pm.meta_key = '_billing_email'      THEN pm.meta_value END) AS email,
                MAX(CASE WHEN pm.meta_key = '_billing_first_name' THEN pm.meta_value END) AS nombre,
                MAX(CASE WHEN pm.meta_key = '_billing_last_name'  THEN pm.meta_value END) AS apellidos,
                p.post_date   AS created_at,
                p.post_status AS estado
            FROM mcfi_posts p
            INNER JOIN mcfi_woocommerce_order_items oi
                ON oi.order_id = p.ID AND oi.order_item_type = 'line_item'
            INNER JOIN mcfi_woocommerce_order_itemmeta im
                ON im.order_item_id = oi.order_item_id
            INNER JOIN mcfi_postmeta pm
                ON pm.post_id = p.ID
            WHERE p.post_type   = 'shop_order'
              AND p.post_status IN ('wc-completed', 'wc-processing')
              AND p.post_date  >= %s
              AND pm.meta_key  IN ('_billing_email','_billing_first_name','_billing_last_name')
            GROUP BY p.ID, oi.order_item_id
            HAVING producto_id IN ('380893','396346','396348','396350');
        """
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                print(f"[ORDERS] Query WooCommerce nativa desde {desde}...")
                cur.execute(query, (desde,))
                rows = cur.fetchall()
                print(f"[ORDERS] {len(rows)} registros desde tablas mcfi_.")
                return list(rows)
        except Exception as e:
            print(f"[ORDERS ERROR] Query nativa fallida: {e}")
            return []
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # PUNTO DE ENTRADA PRINCIPAL
    # ------------------------------------------------------------------
    def fetch_recent_orders(self) -> list:
        """Extrae pedidos de ayer+hoy. Intenta tabla personalizada, luego nativa."""
        ahora = datetime.datetime.now()
        desde = (ahora - datetime.timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        pedidos = self._fetch_custom_table(desde)
        if not pedidos:
            pedidos = self._fetch_woocommerce_native(desde)
        return pedidos

    # ------------------------------------------------------------------
    # SANITIZACIÓN
    # ------------------------------------------------------------------
    def sanitizar_datos(self, raw: list) -> list:
        limpios = []
        for item in raw:
            email = str(item.get("email") or "").strip().lower()
            if not email or "@" not in email:
                print(f"[SANITY] Pedido {item.get('pedido_id')} sin email válido. Saltando.")
                continue
            limpios.append({
                "pedido_id":   str(item.get("pedido_id") or "").strip(),
                "linea_id":    str(item.get("linea_id")  or "").strip(),
                "producto_id": str(item.get("producto_id") or "").strip(),
                "email":       email,
                "nombre":      str(item.get("nombre")    or "").strip().title(),
                "apellidos":   str(item.get("apellidos") or "").strip().title(),
                "dni":         None,  # WooCommerce no almacena DNI por defecto
            })
        print(f"[SANITY] {len(limpios)}/{len(raw)} registros válidos.")
        return limpios
