import reflex as rx
from typing import List, Dict, Any
from Personalidad.states.base_state import State
from Personalidad.db.crud import (
    obtener_simulacros, guardar_simulacro, actualizar_simulacro, 
    eliminar_simulacro, obtener_simulacro_por_id, upsert_simulacro
)

class SimulacroState(State):
    """Estado para la gestión de simulacros presenciales."""
    
    simulacros: List[Dict[str, Any]] = []
    
    # Índice para el carrusel "uno a uno"
    current_index: int = 0
    
    # Campos para el formulario (crear/editar)
    edit_id: int = -1
    titulo: str = "PRÓXIMA CONVOCATORIA"
    fecha: str = ""
    ubicacion: str = ""
    descripcion: str = ""
    url_reserva: str = ""
    
    def next_simulacro(self):
        """Avanza al siguiente simulacro."""
        if self.current_index < len(self.simulacros) - 1:
            self.current_index += 1

    def prev_simulacro(self):
        """Vuelve al simulacro anterior."""
        if self.current_index > 0:
            self.current_index -= 1

    def fetch_simulacros(self):
        """Carga todos los simulacros de la base de datos."""
        raw = obtener_simulacros()
        self.simulacros = [
            {
                "id": s.id,
                "titulo": s.titulo,
                "fecha": s.fecha,
                "ubicacion": s.ubicacion,
                "descripcion": s.descripcion,
                "url_reserva": s.url_reserva
            } for s in raw
        ]

    def set_edit_simulacro(self, simulacro: Dict[str, Any]):
        """Prepara el formulario para editar un simulacro existente."""
        self.edit_id = simulacro["id"]
        self.titulo = simulacro["titulo"]
        self.fecha = simulacro["fecha"]
        self.ubicacion = simulacro["ubicacion"]
        self.descripcion = simulacro["descripcion"]
        self.url_reserva = simulacro.get("url_reserva", "")

    def clear_form(self):
        """Limpia el formulario."""
        self.edit_id = -1
        self.titulo = "PRÓXIMA CONVOCATORIA"
        self.fecha = ""
        self.ubicacion = ""
        self.descripcion = ""
        self.url_reserva = ""

    def _guardar_json_respaldo(self):
        """Guarda la lista actual de simulacros en un archivo JSON como respaldo."""
        import json
        import os
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
            with open("data/simulacros.json", "w", encoding="utf-8") as f:
                json.dump(self.simulacros, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando respaldo JSON: {e}")


    def save_simulacro(self):
        """Guarda o actualiza un simulacro en la BD y en el JSON local."""
        from Personalidad.db.crud import upsert_simulacro
        
        if not self.titulo or not self.fecha:
            return rx.window_alert("Título y Fecha son obligatorios.")
            
        try:
            simulacro_id = self.edit_id if self.edit_id != -1 else None
            upsert_simulacro(
                id=simulacro_id,
                titulo=self.titulo,
                fecha=self.fecha,
                ubicacion=self.ubicacion,
                descripcion=self.descripcion,
                url_reserva=self.url_reserva
            )
            
            # --- ACTIVAR NOTIFICACIÓN PARA ALUMNOS ---
            import os
            import json
            notify_path = os.path.join("data", "novedades.json")
            with open(notify_path, "w") as f:
                json.dump({"nuevo_simulacro": True}, f)
            
            self.fetch_simulacros()
            self._guardar_json_respaldo()
            self.clear_form()
            return rx.toast("Simulacro guardado y notificación enviada.")
        except Exception as e:
            return rx.window_alert(f"Error al guardar: {e}")

    def guardar_simulacro_action(self):
        """Crea o actualiza un simulacro delegando en save_simulacro para activar la notificación."""
        return self.save_simulacro()

    def eliminar_simulacro_action(self, id: int):
        """Elimina un simulacro."""
        if eliminar_simulacro(id):
            self.fetch_simulacros()
            self._guardar_json_respaldo()
            return rx.toast("Simulacro eliminado.")
        return rx.window_alert("No se pudo eliminar el simulacro.")
