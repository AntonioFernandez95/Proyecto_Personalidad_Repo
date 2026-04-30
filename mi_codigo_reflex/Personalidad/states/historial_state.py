import reflex as rx
from Personalidad.states.base_state import State

class HistorialSimplificado_State(State):
    """
    Capa de Historial.
    Se encarga de cargar y refrescar la tabla de simulacros combinada (Físicas + Personalidad).
    """
    historial: list[dict] = []

    def cargar_historial(self):
        """
        Carga el historial real del usuario (Físicas + Personalidad) desde la base de datos.
        """
        user_id = self.user if self.user else "anónimo"
        print(f"DEBUG: Cargando historial completo para {user_id}")
        
        try:
            from Personalidad.db.crud import consultar_historial_completo
            self.historial = consultar_historial_completo(user_id)
            
            # Añadimos metadatos visuales adicionales si faltasen
            for item in self.historial:
                # Color para el componente Badge (por si se usa fuera de personalidad)
                if "color" not in item:
                    item["color"] = "#e53e3e" if item["resultado"] == "NO APTO" else "#28a745"
                    
        except Exception as e:
            print(f"Error cargando historial: {e}")
            self.historial = []
