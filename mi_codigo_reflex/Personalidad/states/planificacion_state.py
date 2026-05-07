import reflex as rx
from Personalidad.states.base_state import State

class PlanificacionState(State):
    """Estado para gestionar los recursos dinámicos en la página de planificación."""
    recursos: list[dict] = []
    selected_recurso_id: str = ""

    def on_load(self):
        """Carga los recursos de la categoría 'planificacion'."""
        if not self.logged_in:
            return rx.redirect("/")
        if not self.has_fisicas_access:
            return rx.redirect("/academia")
            
        self.refresh_user_data()

        # Cargamos los recursos (Vídeos + PDFs)
        from Personalidad.db.crud import obtener_recursos_por_categoria_y_tipo
        try:
            videos_raw = obtener_recursos_por_categoria_y_tipo("planificacion", "video")
            pdfs_raw = obtener_recursos_por_categoria_y_tipo("planificacion", "pdf")
            
            self.recursos = []
            for v in videos_raw:
                # Omitimos el vídeo principal para que no salga duplicado en el desplegable
                if "PLAN DE ENTRENAMIENTO" in v.nombre.upper():
                    continue
                self.recursos.append({
                    "id": v.id, 
                    "full_id": f"video_{v.id}",
                    "nombre": f"{v.nombre} [Vídeo]", 
                    "url": v.url, 
                    "tipo": "video"
                })
            for p in pdfs_raw:
                self.recursos.append({
                    "id": p.id, 
                    "full_id": f"pdf_{p.id}",
                    "nombre": f"{p.nombre} [PDF]", 
                    "url": p.url, 
                    "tipo": "pdf"
                })
            
            # Seleccionamos el primero por defecto usando el full_id
            if self.recursos and not self.selected_recurso_id:
                self.selected_recurso_id = self.recursos[0]["full_id"]
        except Exception as e:
            print(f"Error cargando recursos de planificación: {e}")
            self.recursos = []

    @rx.var
    def selected_recurso(self) -> dict:
        """Devuelve el recurso seleccionado actualmente."""
        for r in self.recursos:
            if r["full_id"] == self.selected_recurso_id:
                return r
        return {}

    def set_selected_recurso_id(self, val: str):
        self.selected_recurso_id = val
