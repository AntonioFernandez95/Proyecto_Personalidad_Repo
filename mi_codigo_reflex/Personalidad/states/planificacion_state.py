import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.db.crud import obtener_recursos_por_categoria
from Personalidad.db.schemas.recurso_schema import recurso_schema

class PlanificacionState(State):
    """Estado para gestionar los recursos dinámicos en la página de planificación."""
    recursos: list[dict] = []
    selected_recurso_id: str = ""

    def on_load(self):
        """Carga los recursos de la categoría 'planificacion'."""
        # Verificamos login y acceso
        if not self.logged_in:
            return rx.redirect("/")
        if not self.has_fisicas_access:
            return rx.redirect("/academia")
            
        # Refrescamos datos del usuario (permisos)
        self.refresh_user_data()

        # Cargamos los recursos
        try:
            raw = obtener_recursos_por_categoria("planificacion")
            self.recursos = [recurso_schema(r) for r in raw]
            
            # Seleccionamos el primero por defecto si no hay ninguno seleccionado
            if self.recursos and not self.selected_recurso_id:
                self.selected_recurso_id = str(self.recursos[0]["id"])
        except Exception as e:
            print(f"Error cargando recursos de planificación: {e}")
            self.recursos = []

    @rx.var
    def selected_recurso(self) -> dict:
        """Devuelve el recurso seleccionado actualmente."""
        for r in self.recursos:
            if str(r["id"]) == self.selected_recurso_id:
                return r
        return {}

    def set_selected_recurso_id(self, val: str):
        self.selected_recurso_id = val
