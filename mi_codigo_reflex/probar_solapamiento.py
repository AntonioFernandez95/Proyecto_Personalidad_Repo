# -*- coding: utf-8 -*-
"""
Script de Prueba y Simulación para el Cron de Actualizaciones (cada 5 minutos)
Este script permite comprobar el comportamiento cuando el cron se ejecuta cada 5 minutos
y simular/verificar cómo evitar el solapamiento (overlapping) de múltiples procesos.
"""

import time
import os
import sys
import threading

# Variable global para simular el estado de una base de datos o recurso compartido
recurso_bd_ocupado = False
lock_simulado = threading.Lock()

class LockfileManager:
    """Clase para gestionar el solapamiento usando un archivo de bloqueo físico (Lockfile)"""
    def __init__(self, filename="importador.lock"):
        self.filename = filename

    def adquirir(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    pid = int(f.read().strip())
                if self._pid_exists(pid):
                    return False
            except:
                pass
        
        # Crear lockfile escribiendo el PID actual
        try:
            with open(self.filename, 'w') as f:
                f.write(str(os.getpid()))
            return True
        except Exception as e:
            print(f"Error escribiendo el lockfile: {e}")
            return False

    def liberar(self):
        if os.path.exists(self.filename):
            try:
                os.remove(self.filename)
            except:
                pass

    def _pid_exists(self, pid):
        if pid < 0: return False
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            process = kernel32.OpenProcess(1, False, pid)
            if process:
                kernel32.CloseHandle(process)
                return True
            return False
        else:
            try:
                os.kill(pid, 0)
            except OSError:
                return False
            else:
                return True


def simulacion_actualizacion_sin_bloqueo(id_proceso, delay=3):
    """
    Simula la ejecución de una actualización sin ninguna protección contra solapamientos.
    """
    global recurso_bd_ocupado
    print(f"[{id_proceso}] Cron iniciado...")
    
    if recurso_bd_ocupado:
        print(f"[{id_proceso}] WARNING: ALERTA DE SOLAPAMIENTO! Este proceso se esta ejecutando al mismo tiempo que otro! Puede haber corrupcion o errores en la BD.")
    
    # Marcamos como ocupado
    recurso_bd_ocupado = True
    
    print(f"[{id_proceso}] Importando JSONs, vaciando tablas, encriptando contraseñas con bcrypt...")
    time.sleep(delay)
    
    # Liberamos el recurso
    recurso_bd_ocupado = False
    print(f"[{id_proceso}] SUCCESS: Actualizacion finalizada.")


def simulacion_actualizacion_con_bloqueo(id_proceso, delay=3):
    """
    Simula la ejecución de una actualización protegiendo el recurso de solapamientos.
    """
    global recurso_bd_ocupado
    print(f"[{id_proceso}] Cron iniciado...")
    
    # Intentamos obtener el lock global
    lock_global = LockfileManager("importador_produccion.lock")
    
    if not lock_global.adquirir():
        print(f"[{id_proceso}] EXCLUDED: EVITADO SOLAPAMIENTO. Otra instancia ya esta ejecutandose. Este proceso se cancela pacificamente.")
        return
        
    try:
        # Iniciamos el trabajo seguro
        print(f"[{id_proceso}] SAFE_RUN: Lock adquirido de forma segura. Iniciando importacion...")
        
        if recurso_bd_ocupado:
            print(f"[{id_proceso}] ERROR: ALERTA DE SOLAPAMIENTO! Esto nunca deberia ocurrir con lock activo!")
            
        recurso_bd_ocupado = True
        time.sleep(delay)
        recurso_bd_ocupado = False
        print(f"[{id_proceso}] SUCCESS: Actualizacion finalizada con exito y sin solapamiento.")
    finally:
        # Liberamos el lock siempre
        lock_global.liberar()


def ejecutar_prueba_concurrente(con_bloqueo=False):
    """
    Usa un bucle 'for' para lanzar varios procesos en paralelo simulando múltiples
    ejecuciones del cron cada 5 minutos que se solapan (ejemplo: ejecuciones muy seguidas
    o procesos lentos que no han terminado).
    """
    print("\n" + "="*70)
    if con_bloqueo:
        print("SIMULACION 2: Ejecucion del Cron CON CONTROL DE SOLAPAMIENTO")
        print("Esperado: Solo un proceso se ejecuta; los demas se auto-cancelan elegantemente.")
    else:
        print("SIMULACION 1: Ejecucion del Cron SIN CONTROL DE SOLAPAMIENTO (Riesgo de caidas)")
        print("Esperado: Los procesos se solapan en paralelo y causan alertas en la consola.")
    print("="*70 + "\n")
    
    # Limpiamos lockfiles residuales
    if os.path.exists("importador_produccion.lock"):
        os.remove("importador_produccion.lock")

    hilos = []
    # Usamos un bucle FOR para simular 3 ejecuciones concurrentes del cron
    for i in range(1, 4):
        if con_bloqueo:
            t = threading.Thread(target=simulacion_actualizacion_con_bloqueo, args=(i, 2))
        else:
            t = threading.Thread(target=simulacion_actualizacion_sin_bloqueo, args=(i, 2))
        hilos.append(t)
        t.start()
        time.sleep(0.2) # Forzar concurrencia cercana
        
    for t in hilos:
        t.join()


def simular_for_5_minutos():
    """
    Simula una ejecución secuencial a lo largo de un bucle que representa el paso del tiempo.
    Representa 3 intervalos del cron de 5 minutos (total de 15 minutos ficticios).
    Muestra que si las ejecuciones son menores de 5 minutos, todo fluye bien de forma normal.
    """
    print("\n" + "="*70)
    print("SIMULACION 3: Simulacion de Bucle Cron de cada 5 minutos (15 minutos totales)")
    print("="*70)
    
    # Un for que recorre intervalos de 5 minutos
    for intervalo in range(1, 4):
        minutos_simulados = (intervalo - 1) * 5
        print(f"\n[Reloj: T+{minutos_simulados} min] Cron disparado automaticamente...")
        
        lock = LockfileManager("importador_produccion.lock")
        if lock.adquirir():
            print(f" -> Iniciando importador.py (Ejecucion #{intervalo})...")
            time.sleep(1) # Tarda 1 segundo ficticio
            lock.liberar()
            print(f" -> [OK] Ejecucion #{intervalo} finalizada correctamente.")
        else:
            print(" -> [ERROR] Solapamiento detectado.")
            
    print("\nSimulacion de linea temporal finalizada.")


if __name__ == "__main__":
    print("Bienvenido al simulador de pruebas del Cron de Actualizaciones.")
    
    # 1. Ejecutamos la simulación insegura (sin control)
    ejecutar_prueba_concurrente(con_bloqueo=False)
    time.sleep(1)
    
    # 2. Ejecutamos la simulación segura (con control)
    ejecutar_prueba_concurrente(con_bloqueo=True)
    time.sleep(1)
    
    # 3. Ejecutamos la simulación del paso del tiempo de 5 en 5 minutos
    simular_for_5_minutos()
    
    print("\n" + "="*70)
    print("RESUMEN Y CONSEJO:")
    print("1. Para evitar el solapamiento en tu Cron en produccion, la mejor practica es usar")
    print("   un 'lockfile' (archivo de bloqueo) o un 'Advisory Lock' de PostgreSQL.")
    print("2. Con el Advisory Lock, el script de importador.py solicita permiso al motor de la BD.")
    print("   Si otra instancia lo tiene, la nueva se detiene de inmediato.")
    print("="*70)
