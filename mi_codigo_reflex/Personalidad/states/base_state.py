<<<<<<< Updated upstream
from typing import Optional
import reflex as rx

class State(rx.State):
    """The base state for the app."""

    user: str = None
    user_plan: str = "sin_plan"

    def logout(self):
        """Log out a user."""
        self.reset()
        return rx.redirect("/")

    def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect("/")

    @rx.var
    def logged_in(self):
        """Check if a user is logged in."""
        return self.user is not None

    @rx.var
    def has_fisicas_access(self) -> bool:
        """Control de acceso centralizado."""
        if self.user == "claudia@academiametodos.com":
            return True
        return self.user_plan.lower() == "plan fisico"
=======
from typing import Optional
from datetime import datetime
import reflex as rx
from Personalidad.db.models.user_model import UsuariosMetodos

class State(rx.State):
    """The base state for the app."""

    usuario_actual: Optional[UsuariosMetodos] = None
    user: str = None # Mantenemos por retrocompatibilidad temporal
    user_plan: str = "sin_plan"

    def logout(self):
        """Log out a user."""
        self.reset()
        return rx.redirect("/")

    def check_login(self):
        """Check if a user is logged in and subscription is active."""
        if not self.logged_in:
            return rx.redirect("/")
        if self.is_subscription_expired:
            return rx.redirect("/")

    def check_access_personalidad(self):
        """Redirige si no tiene acceso a personalidad."""
        if not self.has_personalidad_access:
            return rx.redirect("/academia")

    def check_access_fisicas(self):
        """Redirige si no tiene acceso a físicas."""
        if not self.has_fisicas_access:
            return rx.redirect("/academia")

    @rx.var
    def logged_in(self) -> bool:
        """Check if a user is logged in."""
        return self.usuario_actual is not None

    @rx.var
    def has_fisicas_access(self) -> bool:
        """Control de acceso centralizado para físicas."""
        if not self.usuario_actual:
            return False
        if self.usuario_actual.email == "claudia@academiametodos.com":
            return True
        return self.usuario_actual.fisicas

    @rx.var
    def has_personalidad_access(self) -> bool:
        """Control de acceso centralizado para personalidad."""
        if not self.usuario_actual:
            return False
        if self.usuario_actual.email == "claudia@academiametodos.com":
            return True
        return self.usuario_actual.personalidad

    @rx.var
    def current_user_email(self) -> str:
        return self.usuario_actual.email if self.usuario_actual else ""

    @rx.var
    def is_subscription_expired(self) -> bool:
        """Verifica si la suscripción del usuario ha caducado."""
        if not self.usuario_actual or not self.usuario_actual.hasta:
            return False
            
        try:
            today = datetime.now().date()
            # Limpiamos posibles espacios o partes de tiempo si vienen en el string
            hasta_str = str(self.usuario_actual.hasta).strip().split(" ")[0]
            
            # Soportamos varios formatos comunes
            formats = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"]
            hasta_date = None
            
            for fmt in formats:
                try:
                    hasta_date = datetime.strptime(hasta_str, fmt).date()
                    break
                except ValueError:
                    continue
            
            if hasta_date:
                # Si 'hoy' es posterior a la fecha 'hasta', ha expirado
                return today > hasta_date
        except Exception as e:
            print(f"Error parseando fecha 'hasta' para {self.usuario_actual.email}: {e}")
            
        return False
>>>>>>> Stashed changes
