import reflex as rx
import re

# Importamos nuestros nuevos servicios refactorizados
from Personalidad.services.auth_service import (
    login, search_user, change_password, increment_login_count
)
from Personalidad.services.email_service import (
    send_credentials_email, send_recovery_email, is_authorized_email
)
from Personalidad.states.base_state import State

class LoginState(State):
    """Estado base para la gestión de login."""
    email: str = ""
    password: str = ""
    isWaiting: bool = False 
    isEmailValid: bool = False
    display: str = "none"
    description: str = "Introduce tus credenciales para acceder al test"
    isEmailRegistered: bool = False
    isChecked: bool = False
    isOptionalChecked: bool = False
    isClick1Done: bool = False
    showPasswordAlert: str = "none" 
    showEmailNotFoundAlert: bool = False 
    
    def update_email(self, email: str):
        self.email = email.strip()
        self.validate_email()
        
    def update_password(self, password: str):
        self.password = password
        self.showPasswordAlert = "none"
        
    def validate_email(self):
        """Valida el formato del email mediante regex."""
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.isEmailValid = bool(re.match(regex, self.email))
    
    def toggleCheck(self, checked: bool):
        self.isChecked = checked
        
    def toggleOptionalCheck(self, checked: bool):
        self.isOptionalChecked = checked
    
    @rx.var
    def checkStatusButton(self) -> bool:
        """Determina si el botón de login debe estar activado."""
        return not (self.isChecked and self.isEmailValid and self.password != "")
    
    @rx.var
    def show_email_alert(self) -> str:
        return "none" if self.isEmailValid or self.email == "" else "block"
        
    @rx.var
    def show_terms_alert(self) -> str:
        return "none" if self.isChecked else "block"

class ButtonClick(LoginState):
    """Maneja las acciones de los botones (Login y Recuperación)."""
    
    @rx.background
    async def click_event(self):
        self.isWaiting = True
        self.showEmailNotFoundAlert = False 
        self.showPasswordAlert = "none"
        yield

        # 1. Filtro de dominio (Solo academia o correos de prueba)
        if not is_authorized_email(self.email):
            self.isWaiting = False
            self.showEmailNotFoundAlert = True 
            yield
            return

        # 2. Búsqueda del usuario
        user_data = search_user("email", self.email)
        if not user_data:
            self.isWaiting = False
            self.showEmailNotFoundAlert = True
            yield
            return
        
        # 3. Validación de credenciales
        login_success = await login(self.email, self.password)
        if not login_success:
            self.isWaiting = False
            self.showPasswordAlert = "block"
            yield
            return

        # 4. Éxito: Registro de login y redirección
        increment_login_count(self.email)
        self.user = self.email
        self.isWaiting = False
        yield rx.redirect("/academia")

    @rx.background
    async def recover_password(self):
        """Lógica para la recuperación de contraseña por email."""
        if not self.isEmailValid or self.email == "":
            self.showEmailNotFoundAlert = True
            yield
            return

        self.isWaiting = True
        yield
        
        # 1. Filtro de dominio
        if not is_authorized_email(self.email):
            self.isWaiting = False
            self.showEmailNotFoundAlert = True
            yield
            return

        # 2. Búsqueda y envío
        user_exists = search_user("email", self.email)
        if user_exists:
            # Generamos nueva contraseña y la enviamos
            new_pass = await change_password(self.email)
            if new_pass:
                send_recovery_email(self.email, new_pass)
                self.isWaiting = False
                yield rx.toast.success(
                    f"Nueva contraseña enviada a {self.email}", 
                    position="bottom-right"
                )
                return

        # Si llegamos aquí, el usuario no existe o falló el proceso
        self.isWaiting = False
        self.showEmailNotFoundAlert = True
        yield

    def check_authenticated(self):
        """Verifica si ya hay una sesión activa."""
        if self.logged_in:
            return rx.redirect("/academia")
        self.reset_page()

    def reset_page(self):
        """Limpia los campos del formulario."""
        self.email = ""
        self.password = ""
        self.isEmailValid = False
        self.isChecked = False
        self.isOptionalChecked = False
        self.showPasswordAlert = "none"
        self.showEmailNotFoundAlert = False
