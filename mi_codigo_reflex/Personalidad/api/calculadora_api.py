import reflex as rx
from datetime import datetime
import uuid
from Personalidad.states.base_state import State
# Importamos el Motor (1B) y el CRUD (2C)
from Personalidad.db.crud import guardar_historial_ligero
from Personalidad.db.schemas.historial_schema import HistorialSimplificadoCreate

class CalculadoraState(State):
    """
    Punto 3: Capa de Conexión.
    Es el puente entre el cálculo (motor.py) y la base de datos (crud.py).
    """
    genero: str = "male"
    flexiones: str = ""
    plancha_seg: str = ""
    km2000: str = ""
    agilidad_seg: str = ""
    
    resultado_final: str = ""
    porcentaje: int = 0

    def calcular_y_guardar(self):
        """Función que se dispara al darle al botón 'Calcular'"""
        
        # 1. Recibe el clic y ejecuta el Motor de Cálculo (Punto 1B)
        res_motor = calcular_resultado_test(
            self.genero, 
            self.flexiones, 
            self.plancha_seg, 
            self.km2000, 
            self.agilidad_seg
        ) [cite: 75]

        if res_motor["success"]:
            # 2. Cogemos el resultado ("APTO"/"NO APTO") y el user_id de la sesión
            self.resultado_final = res_motor["resultado"] 
            self.porcentaje = res_motor["porcentaje"] 
            usuario_id = self.user if self.user else "anonimo@test.com" 

            # 3. Llama al ejecutor de crud.py (Punto 2C) para guardar el "ticket"
            try:
                nuevo_ticket = HistorialSimplificadoCreate(
                    id=str(uuid.uuid4()), 
                    user_id=usuario_id, 
                    simulacro_code="FISICAS-CALC", 
                    resultado=self.resultado_final 
                )
                
                # Ejecución real del guardado
                guardar_historial_ligero(nuevo_ticket) [cite: 91, 178]
                return rx.window_alert(f"¡Cálculo guardado con éxito! Resultado: {self.resultado_final}")
            
            except Exception as e:
                return rx.window_alert(f"Error al guardar en el historial: {str(e)}")
        else:
            return rx.window_alert(f"Error en los datos: {res_motor.get('error')}")