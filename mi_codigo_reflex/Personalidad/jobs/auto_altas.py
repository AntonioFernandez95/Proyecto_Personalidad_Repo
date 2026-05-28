import sys
import argparse

# Aseguramos que la ruta del proyecto esté mapeada
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Personalidad.services.orders_reader import OrdersReader
from Personalidad.services.auto_altas_service import AutoAltasService, FileLock

def procesar_flujo(dry_run=False, forzar_pedido_id=None):
    print(f"\n--- INICIANDO PROCESADOR AUTO-ALTAS (Dry-Run: {dry_run}) ---")
    
    # 1. Instanciar lector de pedidos y motor lógico del backend
    reader = OrdersReader()
    backend = AutoAltasService()
    backend.init_db()  # Crea la tabla si no existe (idempotente)
    
    # 2. Extraer pedidos
    pedidos_bruto = reader.fetch_recent_orders()
    pedidos = reader.sanitizar_datos(pedidos_bruto)
    
    if forzar_pedido_id:
        print(f"[*] Filtrando ejecución única para el pedido ID: {forzar_pedido_id}")
        pedidos = [p for p in pedidos if p["pedido_id"] == str(forzar_pedido_id)]
        if not pedidos:
            print(f"[WARN] No se encontró el pedido ID {forzar_pedido_id} en los registros recientes.")
            return

    # 3. Procesamiento en bucle de cada línea
    altas_simuladas = 0
    altas_reales = 0
    
    for p in pedidos:
        if dry_run:
            # === MODO DRY-RUN ===
            altas_simuladas += 1
            print(f"[DRY-RUN] Simulación de alta:")
            print(f"    - Pedido/Línea: {p['pedido_id']} / {p['linea_id']}")
            print(f"    - Producto: {p['producto_id']}")
            print(f"    - Alumno: {p['nombre']} {p['apellidos']} ({p['email']})")
            print(f"    - Método Pago: {p.get('metodo_pago')}")
        else:
            # === MODO REAL (PRODUCCIÓN) ===
            success = backend.procesar_linea(
                pedido_id=p["pedido_id"],
                linea_id=p["linea_id"],
                producto_id=p["producto_id"],
                email=p["email"],
                nombre=p["nombre"],
                apellidos=p["apellidos"],
                dni=p["dni"],
                metodo_pago=p.get("metodo_pago", "")
            )
            if success:
                altas_reales += 1

    print(f"\n--- FIN DEL PROCESAMIENTO ---")
    if dry_run:
        print(f"Altas simuladas con éxito: {altas_simuladas}")
    else:
        print(f"Altas reales procesadas con éxito: {altas_reales}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job de automatización de altas en Academia Métodos.")
    parser.add_argument("--dry-run", action="store_true", help="Lee pedidos y simula altas sin modificar la BD de Reflex ni enviar correos.")
    parser.add_argument("--pedido-id", type=str, default=None, help="Fuerza el procesamiento de un único ID de pedido.")
    parser.add_argument("--audit", action="store_true", help="Audita el esquema de la base de datos externa de WooCommerce.")
    
    args = parser.parse_args()

    if args.audit:
        reader = OrdersReader()
        reader.audit_schema()
        sys.exit(0)

    # Adquirir FileLock antes de la ejecución real (evita concurrencias indeseadas)
    # Si ya se está ejecutando, saldrá limpiamente con código 0
    with FileLock():
        procesar_flujo(dry_run=args.dry_run, forzar_pedido_id=args.pedido_id)
