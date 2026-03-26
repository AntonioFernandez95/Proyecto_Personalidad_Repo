import reflex as rx
from Personalidad.states.base_state import State
import uuid

class AcademiaState(State):
    """Shared state for Academia Online pages."""
    
    # Calculadora
    gender: str = "male"
    flexiones: str = ""
    plancha_seg: str = ""
    km2000: str = ""
    agilidad_seg: str = ""
    resultado: str = ""
    porcentaje: int = 0

    def set_gender(self, val: str):    self.gender = val
    def set_flexiones(self, val: str): self.flexiones = val
    def set_plancha(self, val: str):   self.plancha_seg = val
    def set_km2000(self, val: str):    self.km2000 = val
    def set_agilidad(self, val: str):  self.agilidad_seg = val

    async def procesar_calculo(self):
        """
        CAPA DE CONEXIÓN (HANDLER)
        Delega toda la orquestación a CalculadoraAPI.
        """
        try:
            from Personalidad.api.calculadora_api import CalculadoraAPI
            await CalculadoraAPI.ejecutar_flujo_calculo(self)
        except Exception as e:
            return rx.window_alert(f"Error en el servidor: {str(e)}")
