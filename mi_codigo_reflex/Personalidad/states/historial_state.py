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
        from Personalidad.db.crud import consultar_historial_usuario
        registros = consultar_historial_usuario(user_id)
        
        self.historial = []
        for r in registros:
            # Si r.fecha ya es un string (por el importador), lo usamos tal cual
            if isinstance(r.fecha, str):
                fecha_str = r.fecha[:10] # Solo pillamos YYYY-MM-DD
            else:
                fecha_str = r.fecha.strftime("%d/%m/%Y")
            color = "#787C4D" if r.resultado == "APTO" else "#4A4D4E"
            
            porcentaje_str = r.porcentaje if r.porcentaje else ""
            
            # Color para el componente Badge de Radix/Reflex
            color_name = "green" if r.resultado == "APTO" else "gray"
            
            self.historial.append({
                "fecha": fecha_str,
                "test": r.simulacro_code,
                "resultado": f"{r.resultado} ({porcentaje_str}%)" if porcentaje_str else r.resultado,
                "color": color,           # Hexadecimal para componentes personalizados
                "color_name": color_name, # Para color_scheme de Reflex
                "gender": r.gender if r.gender else "-",
                "flexiones": r.flexiones if r.flexiones else "-",
                "plancha": r.plancha_seg if r.plancha_seg else "-",
                "km2000": r.km2000 if r.km2000 else "-",
                "agilidad": r.agilidad_seg if r.agilidad_seg else "-",
                "porcentaje": porcentaje_str if porcentaje_str else "-",
                "user_id": r.user_id if r.user_id else "anónimo"
            })
