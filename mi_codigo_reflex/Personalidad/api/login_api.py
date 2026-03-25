import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from Personalidad.db.client import db_client
from Personalidad.db.schemas.user_schema import user_schema
from Personalidad.db.models.user_model import UserModel, UserDBModel

async def checkEmailProvided(email: str):
    """
    Verifica si el correo electrónico existe en la tabla de personalidad.
    """
    try:
        user_check = search_user("email", email)
        if user_check is None:
            return False
        return True
    except Exception as e:
        print(f"Error en checkEmailProvided: {e}")
        return False

async def login(email: str, password: str):
    """
    Valida email y password contra la base de datos.
    """
    user_db = search_password_from_user("email", email)
    
    if not user_db:
        print("Usuario no encontrado")
        return False
        
    # Comprobación de contraseña directa
    if not password == user_db.password:
        print("Contraseña incorrecta")
        return False
        
    return True

#*Cambio de contraseña*#
async def changePassword(email: str):
    newPassword = genRandomPassword()
    try:
        # Actualizamos la contraseña en la base de datos
        db_client.update_one("personalidad.users", "email", email, {"password": newPassword})
    except Exception as e:
        print(f"Error al cambiar password: {e}")
        return {"error": "No se ha actualizado el usuario"}

    return search_user("email", email)

#*Check opcional para términos*#
async def optionalCheck(email: str, isOptionalChecked: bool):
    if isOptionalChecked:
        try:
            db_client.update_one("personalidad.users", "email", email, {"is_optional_checked": isOptionalChecked})
        except Exception as e:
            print(f"Error en optionalCheck: {e}")
            return {"error": "No se ha actualizado el usuario"}

#*Busca al usuario (Modelo sin password)*#
def search_user(field: str, key):
    try:
        user = db_client.find_one("personalidad.users", field, key)
        if user: 
            return UserModel(**user_schema(user))
        return None
    except Exception as e:
        print(f"Error searching user: {e}")
        return None

#*Busca al usuario con password para validar el login*#
def search_password_from_user(field: str, key):
    try:
        user = db_client.find_one("personalidad.users", field, key)
        if user:
            return UserDBModel(**user_schema(user))
        return None
    except Exception as e:
        print(f"Error searching password: {e}")
        return None

def genRandomPassword():
    all_chars = string.ascii_letters + string.digits + '*@?¿¡!$#'
    return ''.join(random.choices(all_chars, k=7))

#*//////////////////////////////////////////////////////////////////*#

def sendEmail(email: str):
    sender = 'metodos@academiametodos.com'
    password_smtp = '*Agentes_010?'
    server = 'smtp.office365.com'
    port = 587
    
    # Filtro: Academia o tu correo de prueba
    is_authorized = email.lower().endswith("@academiametodos.com") or email.lower() == "alejandragarzon.24@campuscamara.es"
    
    if not is_authorized:
        print(f"Email bloqueado: {email} no autorizado.")
        return

    user_db = search_password_from_user("email", email)
    if not user_db:
        return

    user_password = user_db.password
    
    message = MIMEMultipart("alternative")
    message["Subject"] = 'Acceso Test de Personalidad - Academia Métodos'
    message["From"] = sender
    message["To"] = email

    body = f"Tu usuario: {email}\nTu contraseña: {user_password}"
    html = f"<html><body><p>Usuario: <b>{email}</b></p><p>Contraseña: <b>{user_password}</b></p></body></html>"
    
    message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(html, "html"))

    try:
        smtp_server = smtplib.SMTP(server, port)
        smtp_server.starttls()
        smtp_server.login(sender, password_smtp)
        smtp_server.sendmail(sender, email, message.as_string())
        smtp_server.close()
        print("¡Email enviado!")
    except Exception as ex:
        print("Error enviando email:", ex)

# NUEVA FUNCIÓN: Envío de correo específico para recuperación
def sendRecoveryEmail(email: str):
    sender = 'metodos@academiametodos.com'
    password_smtp = '*Agentes_010?'
    server = 'smtp.office365.com'
    port = 587
    
    # Filtro: Academia o tu correo de prueba
    is_authorized = email.lower().endswith("@academiametodos.com") or email.lower() == "alejandragarzon.24@campuscamara.es"
    
    if not is_authorized:
        print(f"Email de recuperación bloqueado para: {email}")
        return

    user_db = search_password_from_user("email", email)
    if not user_db:
        return

    user_password = user_db.password
    
    message = MIMEMultipart("alternative")
    message["Subject"] = 'Recuperación de Contraseña - Academia Métodos'
    message["From"] = sender
    message["To"] = email

    body = f"Hola,\n\nHas solicitado una nueva contraseña.\nTu contraseña actual es: {user_password}"
    html = f"""
    <html>
        <body>
            <h3>Recuperación de acceso</h3>
            <p>Has solicitado recuperar tu contraseña para el Test de Personalidad.</p>
            <p>Tu nueva contraseña es: <b>{user_password}</b></p>
            <p>Ya puedes volver a la web e iniciar sesión.</p>
        </body>
    </html>
    """
    
    message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(html, "html"))

    try:
        smtp_server = smtplib.SMTP(server, port)
        smtp_server.starttls()
        smtp_server.login(sender, password_smtp)
        smtp_server.sendmail(sender, email, message.as_string())
        smtp_server.close()
        print(f"¡Email de recuperación enviado a {email}!")
    except Exception as ex:
        print("Error enviando email de recuperación:", ex)