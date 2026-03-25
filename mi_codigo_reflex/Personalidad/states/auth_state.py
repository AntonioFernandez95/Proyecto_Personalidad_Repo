import reflex as rx

from Personalidad.states.base_state import State
from Personalidad.db.client import db_client
from Personalidad.db.schemas.user_schema import user_schema
from Personalidad.db.models.user_model import UserModel


class AuthState(State):
    """The authentication state for sign up and login page."""

    email: str
    password: str
    confirm_password: str

    def signup(self):
        """Sign up a user."""
        if self.password != self.confirm_password:
            return rx.window_alert("Passwords do not match.")
        
        # Validación con PostgresClient
        existing_user = db_client.find_one("personalidad.users", "email", self.email)
        if existing_user:
            return rx.window_alert("Username already exists.")
            
        # TODO: Implementar función de inserción (insert_one) en db_client si se requiere registro desde la web
        return rx.window_alert("El registro desde la web está deshabilitado temporalmente.")

    def login(self):
        """Log in a user."""
        user = db_client.find_one("personalidad.users", "email", self.email)
        
        if user and user.get("password") == self.password:
            self.user = user.get("email")
            return rx.redirect("/")
        else:
            return rx.window_alert("Invalid username or password.")


def search_user(field: str, key):
    try:
        # CAMBIO: Usamos el esquema de PostgreSQL
        user = db_client.find_one("personalidad.users", field, key)
        if user:
            return UserModel(**user_schema(user))
        else:
            raise ValueError("Usuario o contraseña incorrectos")
    except Exception as e:
        print(f"Error during user search: {e}")
        return {"error": "No se ha encontrado el usuario"}