import random
import string
from fastapi import HTTPException, status
from Personalidad.db.client import db_client
from Personalidad.db.schemas.user_schema import user_schema
from Personalidad.db.models.user_model import UserModel, UserDBModel

#* --- CONFIGURACIÓN --- *#
ALGORITHM = "HS256"
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

#* --- FUNCIONES PRINCIPALES --- *#

# Encuentra al usuario por correo
async def user(email: str):
    return search_user("email", email)

# Cambio de contraseña (generación y actualización)
async def changePassword(email: str):
    newPassword = genRandomPassword()
    try:
        # CAMBIO CRÍTICO: Se añade el esquema 'personalidad.'
        db_client.update_one("personalidad.users", "email", email, {"password": newPassword})
    except Exception as e:
        print(f"Error updating password: {e}")
        return {"error": "No se ha actualizado el usuario"}

    return search_user("email", email)

#* --- UTILS / BUSQUEDAS --- *#

def search_user(field: str, key):
    try:
        # CAMBIO CRÍTICO: Se añade el esquema 'personalidad.'
        user = db_client.find_one("personalidad.users", field, key)
        if user:
            return UserModel(**user_schema(user))
        else:
            return None # Devolvemos None si no existe para manejarlo en el State
    except Exception as e:
        print(f"Error during user search: {e}")
        return {"error": "Error en la búsqueda de usuario"}

def search_user_db(field: str, key):
    try:
        # CAMBIO CRÍTICO: Se añade el esquema 'personalidad.'
        user = db_client.find_one("personalidad.users", field, key)
        if user:
            return UserDBModel(**user_schema(user))
        return None
    except Exception as e:
        print(f"Error during database user search: {e}")
        return {"error": "No se ha encontrado el usuario"}
    
def genRandomPassword():
    lowercaseLetters = string.ascii_lowercase
    uppercaseLetters = string.ascii_uppercase
    digits = string.digits
    symbols = '*@?¿¡!$#'
    all_chars = lowercaseLetters + uppercaseLetters + digits + symbols
    return ''.join(random.choices(all_chars, k=7))