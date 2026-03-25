import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.api.motor import calcular_resultado_test
from Personalidad.db.crud import guardar_historial_ligero, consultar_historial_usuario
from Personalidad.db.schemas.historial_schema import HistorialSimplificadoCreate
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

    # Historial
    historial: list[dict] = []

    def set_gender(self, val: str):    self.gender = val
    def set_flexiones(self, val: str): self.flexiones = val
    def set_plancha(self, val: str):   self.plancha_seg = val
    def set_km2000(self, val: str):    self.km2000 = val
    def set_agilidad(self, val: str):  self.agilidad_seg = val

    def calcular(self):
        """
        3. CAPA DE CONEXIÓN
        Es el puente entre el cálculo y la base de datos.
        """
        # 1. Recibe el clic (este método se dispara al darle al botón)
        
        # 2. Ejecuta el Motor de Cálculo (Punto 1B)
        resultado_motor = calcular_resultado_test(
            self.gender,
            self.flexiones,
            self.plancha_seg,
            self.km2000,
            self.agilidad_seg
        )
        
        if resultado_motor["success"]:
            # 3. Coge ese resultado ("APTO") y el user_id de la sesión
            self.resultado = resultado_motor["resultado"]
            self.porcentaje = resultado_motor["porcentaje"]
            user_id = self.user if self.user else "anónimo"
            
            # 4. Llama al ejecutor de crud.py (Punto 2C) para guardar el "ticket"
            try:
                datos_historial = HistorialSimplificadoCreate(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    simulacro_code="FISC-01",
                    resultado=self.resultado,
                    porcentaje=f"{self.porcentaje}%"
                )
                guardar_historial_ligero(datos_historial)
            except Exception as e:
                print(f"Error al guardar historial: {e}")
        else:
            self.resultado = "ERROR"
            self.porcentaje = 0

    def cargar_historial(self):
        """
        Capa de Datos.
        Carga el historial real del usuario desde la base de datos.
        """
        user_id = self.user if self.user else "anónimo"
        print(f"DEBUG: Cargando historial para {user_id}")
        registros = consultar_historial_usuario(user_id)
        
        self.historial = []
        for r in registros:
            # Formateamos para la UI
            fecha_str = r.fecha.strftime("%d/%m/%Y")
            color = "#787C4D" if r.resultado == "APTO" else "#4A4D4E"
            
            # Mostramos el porcentaje guardado (ej: 53%)
            porcentaje_str = r.porcentaje if r.porcentaje else ""
            
            self.historial.append({
                "fecha": fecha_str,
                "test": r.simulacro_code,
                "resultado": f"{r.resultado} ({porcentaje_str})" if porcentaje_str else r.resultado,
                "color": color
            })
