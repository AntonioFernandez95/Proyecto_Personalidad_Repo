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