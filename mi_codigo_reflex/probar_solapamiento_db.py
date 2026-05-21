# -*- coding: utf-8 -*-
"""
Script de Prueba y Monitoreo Activo de Solapamientos en la Base de Datos.
Usa un bucle 'for' para realizar consultas en tiempo real al contenedor de PostgreSQL
y demostrar visualmente el solapamiento concurrente.
"""

import time
import os
import psycopg2
import threading

# Configuración de conexión dinámica (funciona en Local y en Servidor/Docker)
DB_NAME = os.getenv("DB_NAME", "db_personalidad_proyecto")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Prefor2026!")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

DB_CONFIG = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT
}

def obtener_conexion():
    return psycopg2.connect(**DB_CONFIG)

def tarea_importador_sin_lock(id_proceso):
    """
    Simula una importación pesada en la BD ejecutando un comando sleep directo en PostgreSQL.
    Esto consume recursos y bloquea la BD por 3 segundos.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        # Establecemos el nombre de aplicación para rastrearla fácilmente en la BD
        cur.execute("SET application_name = 'importador_test_concurrente';")
        
        # Simula una importación que dura 3 segundos en el motor
        cur.execute("SELECT pg_sleep(3);")
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f" -> Proceso {id_proceso} finalizado con error (BD no disponible).")

def tarea_importador_con_lock(id_proceso):
    """
    Simula una importación protegida con Advisory Locks en la BD.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SET application_name = 'importador_test_concurrente';")
        
        # Intentamos obtener el bloqueo consultivo (advisory lock) en Postgres
        LOCK_KEY = 876543
        cur.execute("SELECT pg_try_advisory_lock(%s);", (LOCK_KEY,))
        lock_adquirido = cur.fetchone()[0]
        
        if not lock_adquirido:
            # Si no se pudo adquirir, se cancela la ejecución
            cur.close()
            conn.close()
            return
            
        try:
            # Ejecuta la importación simulada si obtuvo el bloqueo
            cur.execute("SELECT pg_sleep(3);")
            conn.commit()
        finally:
            # Liberamos el lock
            cur.execute("SELECT pg_advisory_unlock(%s);", (LOCK_KEY,))
            conn.commit()
            cur.close()
            conn.close()
    except Exception:
        pass

def contar_procesos_activos_en_db():
    """
    Realiza una consulta directa a la base de datos (contenedor) para contar
    cuántas consultas 'importador_test_concurrente' están ejecutándose actualmente.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        # Consultamos las estadísticas de actividad del contenedor
        cur.execute("""
            SELECT COUNT(*) 
            FROM pg_stat_activity 
            WHERE application_name = 'importador_test_concurrente' 
              AND state = 'active';
        """)
        cuenta = cur.fetchone()[0]
        cur.close()
        conn.close()
        return cuenta
    except Exception:
        # Retorna -1 si no se puede conectar a la BD
        return -1

def ejecutar_test_concurrente(usar_bloqueo=False):
    if usar_bloqueo:
        print("\n" + "="*80)
        print("PRUEBA B: EJECUCION CON BLOQUEOS CONSULTIVOS (ADVISORY LOCKS) EN LA BD")
        print("Esperado: Maximo 1 proceso activo a la vez. No hay solapamiento.")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("PRUEBA A: EJECUCION CON CONCURRENCIA DE CRON SIN BLOQUEOS (SOLAPAMIENTO)")
        print("Esperado: Varios procesos corriendo a la vez en la BD. ¡SOLAPAMIENTO!")
        print("="*80)

    # 1. Lanzamos 3 hilos concurrentes simulando el cron disparándose 3 veces
    hilos = []
    for i in range(1, 4):
        target_fn = tarea_importador_con_lock if usar_bloqueo else tarea_importador_sin_lock
        t = threading.Thread(target=target_fn, args=(i,))
        hilos.append(t)
        t.start()
        time.sleep(0.1) # Breve pausa para simular desfase corto

    # 2. Bucle FOR en el hilo principal para comprobar activamente el estado en la BD cada 0.5 seg
    print("Iniciando bucle 'for' de monitoreo en tiempo real de la base de datos...")
    
    # 10 iteraciones de 0.5 segundos (5 segundos en total)
    for iteracion in range(1, 11):
        tiempo = iteracion * 0.5
        activos = contar_procesos_activos_en_db()
        
        if activos == -1:
            print(f" -> [T + {tiempo:.1f}s] Error de conexion: ¿Esta el contenedor de la BD corriendo?")
            break
            
        # Comprobar si hay solapamiento
        estado = "OK (Limpio)"
        if activos > 1:
            estado = "⚠️ SOLAPAMIENTO DETECTADO (Multiples procesos activos)"
        elif activos == 1:
            estado = "OK (1 proceso activo)"
            
        print(f" -> [T + {tiempo:.1f}s] Procesos concurrentes en el contenedor de BD: {activos} | Estado: {estado}")
        time.sleep(0.5)

    # Esperamos a que los hilos terminen
    for t in hilos:
        t.join()

if __name__ == "__main__":
    print("Comprobador de Solapamiento Directo en el Servidor de Base de Datos")
    
    # Intentamos verificar si la base de datos está activa
    test_conn = None
    try:
        test_conn = obtener_conexion()
        print("Conectado con éxito a PostgreSQL (localhost:5432). Iniciando pruebas...")
        test_conn.close()
        
        # Lanzamos la prueba SIN bloqueo (provoca solapamiento en la BD)
        ejecutar_test_concurrente(usar_bloqueo=False)
        
        time.sleep(1)
        
        # Lanzamos la prueba CON bloqueo (evita solapamiento en la BD)
        ejecutar_test_concurrente(usar_bloqueo=True)
        
    except Exception as e:
        print("\n[!] ERROR DE CONEXION A LA BASE DE DATOS:")
        print(f"No se pudo conectar a PostgreSQL en localhost:5432: {e}")
        print("\nPara correr este script:")
        print("1. El contenedor de la base de datos ('db') debe estar encendido y expuesto en el puerto 5432.")
        print("2. Puedes iniciar tu Docker Compose con: docker-compose up -d db")
