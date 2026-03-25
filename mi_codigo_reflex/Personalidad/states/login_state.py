import reflex as rx
import re

# Importamos la nueva función de envío de recuperación
from Personalidad.api.login_api import login, checkEmailProvided, changePassword, sendEmail, sendRecoveryEmail, optionalCheck
from Personalidad.db.client import db_client
from Personalidad.db.schemas.user_schema import user_schema
from Personalidad.db.models.user_model import UserModel
from Personalidad.states.base_state import State


# --- BASE LOGIN STATE ---
class LoginState(State):
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
    showPasswordAlert: str = "none" # Controla el aviso de contraseña mal
    showEmailNotFoundAlert: bool = False # Controla el aviso de email no existe
    
    def update_email(self, email):
        self.email = email.strip() # Limpiamos espacios
        self.validate_email()
        
    def update_password(self, password):
        self.password = password
        self.showPasswordAlert = "none" # Si empieza a escribir, quitamos la alerta
        
    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.isEmailValid = False
        else:
            self.isEmailValid = True
    
    def toggleCheck(self, checked):
        self.isChecked = checked
        
    def toggleOptionalCheck(self, checked):
        self.isOptionalChecked = checked
    
    @rx.var
    def checkStatusButton(self) -> bool:
        # Botón desactivado si no cumple condiciones
        return not (self.isChecked and self.isEmailValid and self.password != "")
    
    @rx.var
    def show_email_alert(self) -> str:
        return "none" if self.isEmailValid or self.email == "" else "block"
        
    @rx.var
    def show_terms_alert(self) -> str:
        return "none" if self.isChecked else "block"

# --- LÓGICA DEL BOTÓN Y RESET ---
class ButtonClick(LoginState):
    
    @rx.background
    async def click_event(self):
        self.isWaiting = True
        self.showEmailNotFoundAlert = False 
        self.showPasswordAlert = "none"
        yield

        # 1. Buscamos al usuario en la tabla de personalidad
        user_data = search_user("email", self.email)
        
        # 2. Filtro de existencia en BD
        if not user_data:
            self.isWaiting = False
            self.showEmailNotFoundAlert = True
            yield
            return

        # 3. FILTRO DE DOMINIO (Academia O tu correo de prueba)
        is_academia = self.email.lower().endswith("@academiametodos.com")
        is_prueba = self.email.lower() == "alejandragarzon.24@campuscamara.es"

        if not (is_academia or is_prueba):
            self.isWaiting = False
            self.showEmailNotFoundAlert = True 
            yield
            return
        
        # 4. VALIDAR CONTRASEÑA
        login_success = await login(self.email, self.password)
        
        if not login_success:
            self.isWaiting = False
            self.showPasswordAlert = "block"
            yield
            return

        # 5. ÉXITO
        increment_login_count(self.email)
        self.user = self.email
        self.isWaiting = False
        yield rx.redirect("/academia")

    @rx.background
    async def recover_password(self):
        """Lógica para recuperar contraseña"""
        # Validar que el email sea correcto antes de nada
        if not self.isEmailValid or self.email == "":
            self.showEmailNotFoundAlert = True
            yield
            return

        self.isWaiting = True
        yield
        
        # Comprobar dominio (Academia o Prueba)
        is_academia = self.email.lower().endswith("@academiametodos.com")
        is_prueba = self.email.lower() == "alejandragarzon.24@campuscamara.es"
        
        if not (is_academia or is_prueba):
            self.isWaiting = False
            self.showEmailNotFoundAlert = True
            yield
            return

        # Buscar si el usuario existe en la base de datos
        user_exists = search_user("email", self.email)
        if user_exists:
            # 1. Generamos contraseña nueva en la BD
            await changePassword(self.email)
            # 2. Enviamos el correo de recuperación
            sendRecoveryEmail(self.email)
            
            self.isWaiting = False
            yield rx.toast.success(f"Se ha enviado una nueva contraseña a {self.email}", position="bottom-right")
        else:
            self.isWaiting = False
            self.showEmailNotFoundAlert = True
            yield

    def check_authenticated(self):
        """Redirect to academia if already logged in, otherwise reset fields."""
        if self.logged_in:
            return rx.redirect("/academia")
        self.reset_page()

    def reset_page(self):
        self.email = ""
        self.password = ""
        self.isEmailValid = False
        self.display = "none"
        self.isEmailRegistered = False
        self.isChecked = False
        self.isOptionalChecked = False
        self.showPasswordAlert = "none"
        self.showEmailNotFoundAlert = False

class Authentication(LoginState):
    async def user_login(self):
        await user(self.email)

# --- UTILS / FUNCIONES EXTERNAS ---

def search_user(field: str, key):
    try:
        user = db_client.find_one("personalidad.users", field, key)
        if user:
            return UserModel(**user_schema(user))
    except Exception as e:
        print(f"Error during user search: {e}")
    return None

async def user(email: str):
    return search_user("email", email)

def increment_login_count(email: str):
    try:
        user = db_client.find_one("personalidad.users", "email", email)
        if user:
            current_count = user.get("count_login", 0)
            try:
                new_count = int(current_count) + 1
            except:
                new_count = 1
                
            db_client.update_one(
                "personalidad.users", 
                "email",
                email,
                {"count_login": new_count}
            )
    except Exception as e:
        print(f"Error increment login: {e}")