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
