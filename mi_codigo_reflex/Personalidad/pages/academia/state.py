import reflex as rx
from Personalidad.states.base_state import State

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

    def calcular(self):
        puntos = 0
        total  = 4
        try:
            flex = int(self.flexiones)      if self.flexiones      else 0
            plan = int(self.plancha_seg)    if self.plancha_seg    else 0
            agil = float(self.agilidad_seg) if self.agilidad_seg   else 99.0

            if self.gender == "male":
                if flex >= 17: puntos += 1
                if plan >= 60: puntos += 1
                if agil <= 25: puntos += 1
            else:
                if flex >= 12: puntos += 1
                if plan >= 40: puntos += 1
                if agil <= 27: puntos += 1

            if self.km2000:
                parts = self.km2000.split(":")
                if len(parts) == 2:
                    secs = int(parts[0]) * 60 + int(parts[1])
                    limit = 660 if self.gender == "male" else 780
                    if secs <= limit:
                        puntos += 1

            self.porcentaje = int((puntos / total) * 100)
            self.resultado = "APTO" if puntos >= 3 else "NO APTO"
        except Exception:
            self.resultado  = "ERROR"
            self.porcentaje = 0
