from typing import Optional
import reflex as rx

class State(rx.State):
    """The base state for the app."""

    user: str = None
    user_role: str = "estudiante" # Rol por defecto
    user_plan: str = "sin_plan"
    disabled_personalidad: bool = False
    disabled_fisicas: bool = False

    def logout(self):
        """Log out a user."""
        self.reset()
        return rx.redirect("/")

    def refresh_user_data(self):
        """Refresca los datos del usuario desde la base de datos sin bloquear."""
        if not self.user:
            return
        
        try:
            from Personalidad.services.auth_service import search_user
            user_data = search_user("email", self.user)
            if user_data:
                self.user_role = user_data.rol
                self.disabled_personalidad = user_data.disabled_personalidad
                self.disabled_fisicas = user_data.disabled_fisicas
        except Exception as e:
            print(f"Error refrescando datos: {e}")

    def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect("/")

    def check_fisicas_access(self):
        """Verifica acceso al plan de físicas."""
        if not self.logged_in:
            return rx.redirect("/")
        
        self.refresh_user_data()
        if not self.has_fisicas_access:
            return rx.redirect("/academia")

    def check_personalidad_access(self):
        """Verifica acceso al plan de personalidad."""
        if not self.logged_in:
            return rx.redirect("/")
            
        self.refresh_user_data()
        if not self.has_personalidad_access:
            return rx.redirect("/academia")

    def check_admin(self):
        """Verifica si el usuario es administrador. Si no, lo manda a la zona de estudiantes."""
        if not self.logged_in:
            return rx.redirect("/")
        
        # Refrescamos datos para asegurar que sigue siendo admin o no ha sido desactivado
        self.refresh_user_data()
        
        if self.user_role != "admin":
            return rx.redirect("/academia")

    @rx.var
    def logged_in(self):
        """Check if a user is logged in."""
        return self.user is not None

    @rx.var
    def is_admin(self) -> bool:
        """Helper para ocultar/mostrar elementos en el frontend."""
        return self.user_role == "admin"

    @rx.var
    def has_fisicas_access(self) -> bool:
        """Control de acceso para el plan de físicas."""
        if self.is_admin:
            return True
        return not self.disabled_fisicas

    @rx.var
    def has_personalidad_access(self) -> bool:
        """Control de acceso para el plan de personalidad."""
        if self.is_admin:
            return True
        return not self.disabled_personalidad