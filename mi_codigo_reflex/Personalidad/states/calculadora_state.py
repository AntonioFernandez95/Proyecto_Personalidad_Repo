import reflex as rx
from datetime import datetime
from Personalidad.states.base_state import State
from Personalidad.db.crud import guardar_historial_ligero

class CalculadoraState(State):
    """Estado de la Calculadora: Hace las matemáticas y le pasa el dato al CRUD"""
   
    # Variables del formulario conectadas al frontend
    genero: str = "Hombre"
    carrera_minutos: int = 0
    carrera_segundos: int = 0
    flexiones: int = 0
    plancha_seg: int = 0
    agilidad_seg: float = 0.0
   
    # Variable de respuesta
    resultado_final: str = ""
   
    def calcular_resultado(self):
        """Aplica las matemáticas del baremo oficial y prepara el guardado."""
        tiempo_carrera_total = (int(self.carrera_minutos) * 60) + int(self.carrera_segundos)
        agilidad = float(self.agilidad_seg)
       
        es_apto = False
       
        # Lógica para HOMBRES
        if self.genero == "Hombre":
            if tiempo_carrera_total < 714 and agilidad < 15.4:
                es_apto = True
               
        # Lógica para MUJERES
        elif self.genero == "Mujer":
            if tiempo_carrera_total < 778 and agilidad < 17.1:
                es_apto = True

        # Asignamos el resultado
        if es_apto:
            self.resultado_final = "APTO"
        else:
            self.resultado_final = "NO APTO"
           
        # Llamamos a la función que le pasa los datos al código de tu amigo
        self._enviar_datos_al_crud()

    def _enviar_datos_al_crud(self):
        """Prepara el paquete de datos y llama a la función de base de datos de tu compañero"""
        usuario_identificador = self.user if self.user else "anonimo@test.com"
       
        # 1. Empaquetamos los datos exactamente como los va a pedir el Schema de tu amigo
        datos_para_guardar = {
            "user_id": usuario_identificador,
            "simulacro_code": "FISICAS-CALC",
            "resultado": self.resultado_final,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
       
        # 2. Se lo enviamos a su función
        try:
            # 👇 Cuando tu amigo termine, descomenta esta línea para que se guarde de verdad
            # guardar_historial_ligero(datos_para_guardar)
           
            # Mientras tu amigo termina, dejamos este print para que veas que tu parte funciona
            print(f"✅ ¡Cálculo terminado! Esperando al CRUD de tu amigo para guardar esto: {datos_para_guardar}")
           
        except Exception as e:
            print(f"❌ Error al conectar con el CRUD: {e}")

    def motor_de_calculo(self, genero: str, flexiones: str, plancha: str, km2000: str, agilidad: str) -> str:
        """
        Motor de Cálculo (Punto 1B).
        Recibe los datos y devuelve "APTO" o "NO APTO".
        """
        try:
            # Reutilizamos la lógica de Personalidad.api.motor o implementamos una similar.
            # Para cumplir la regla de "Pásale los datos", procesamos aquí.
            
            # Objetivos simplificados para el ejemplo (basados en Baremo)
            if genero == "male":
                t_flex, t_plan, t_agil, t_carr = 17, 60, 25.0, 660
            else:
                t_flex, t_plan, t_agil, t_carr = 12, 40, 27.0, 780

            val_flex = int(flexiones) if flexiones else 0
            val_plan = int(plancha) if plancha else 0
            val_agil = float(agilidad) if agilidad else 999.0
            
            # Procesar carrera 2000m (mm:ss)
            val_carr = 9999
            if km2000 and ":" in km2000:
                parts = km2000.split(":")
                if len(parts) == 2:
                    val_carr = int(parts[0]) * 60 + int(parts[1])

            # El APTO se rige por cumplir los mínimos en al menos 3 pruebas
            puntos_apto = 0
            if val_flex >= t_flex: puntos_apto += 1
            if val_plan >= t_plan: puntos_apto += 1
            if val_agil <= t_agil: puntos_apto += 1
            if val_carr <= t_carr: puntos_apto += 1
            
            return "APTO" if puntos_apto >= 3 else "NO APTO"
        except Exception as e:
            print(f"Error en motor de cálculo: {e}")
            return "ERROR"
