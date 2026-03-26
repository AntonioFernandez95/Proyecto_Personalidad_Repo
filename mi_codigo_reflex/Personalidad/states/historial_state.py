import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.db.crud import consultar_historial_usuario

class HistorialSimplificado_State(State):
    """
    Capa de Historial.
    Se encarga de cargar y refrescar la tabla de simulacros.
    """
    historial: list[dict] = []

    def cargar_historial(self):
        """
        Carga el historial real del usuario desde la base de datos.
        """
        user_id = self.user if self.user else "anónimo"
        print(f"DEBUG: Cargando historial para {user_id}")
        
        # Importamos aquí para evitar circulares si fuera necesario, 
        # aunque en este caso consultar_historial_usuario está en crud.py
        registros = consultar_historial_usuario(user_id)
        
        self.historial = []
        for r in registros:
            fecha_str = r.fecha.strftime("%d/%m/%Y")
            color = "#787C4D" if r.resultado == "APTO" else "#4A4D4E"
            
            porcentaje_str = r.porcentaje if r.porcentaje else ""
            
            self.historial.append({
                "fecha": fecha_str,
                "test": r.simulacro_code,
                "resultado": f"{r.resultado} ({porcentaje_str})" if porcentaje_str else r.resultado,
                "color": color
            })
