from typing import Optional
import reflex as rx

class State(rx.State):
    """The base state for the app."""

    user: str = None
    user_role: str = "estudiante" # Rol por defecto
    user_plan: str = "sin_plan"

    def logout(self):
        """Log out a user."""
        self.reset()
        return rx.redirect("/")

    def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect("/")

    def check_admin(self):
        """Verifica si el usuario es administrador. Si no, lo manda a la zona de estudiantes."""
        if not self.logged_in:
            return rx.redirect("/")
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
        """Control de acceso centralizado."""
        if self.is_admin:
            return True
        return self.user_plan.lower() == "plan fisico"