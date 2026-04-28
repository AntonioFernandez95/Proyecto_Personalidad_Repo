import bcrypt
import random
import string
from Personalidad.db.client import db_client
from Personalidad.db.schemas.user_schema import user_schema
from Personalidad.db.models.user_model import UserModel, UserDBModel

def search_user(field: str, key) -> UserModel:
    """Busca un usuario en la BD y devuelve su modelo (sin password)."""
    try:
        user_data = db_client.find_one("usuarios_plataformas", field, key)
        return UserModel(**user_schema(user_data)) if user_data else None
    except Exception as e:
        print(f"Error buscando usuario ({field}={key}): {e}")
        return None

def search_password_from_user(field: str, key) -> UserDBModel:
    """Busca un usuario y devuelve el modelo con password para validación."""
    try:
        user_data = db_client.find_one("usuarios_plataformas", field, key)
        return UserDBModel(**user_schema(user_data)) if user_data else None
    except Exception as e:
        print(f"Error buscando password ({field}={key}): {e}")
        return None

async def login(email: str, password: str) -> bool:
    """
    Valida las credenciales de un usuario.
    Soporta migración automática de texto plano a bcrypt.
    """
    user_db = search_password_from_user("email", email)
    if not user_db:
        return False

    password_bytes = password.encode('utf-8')
    db_password = user_db.password

    # 1. Comprobación Estándar (Bcrypt)
    if db_password.startswith("$2") and len(db_password) >= 59:
        try:
            return bcrypt.checkpw(password_bytes, db_password.encode('utf-8'))
        except Exception:
            return False
    
    # 2. Comprobación Híbrida (Texto Plano + Migración)
    if password == db_password:
        # Migramos a bcrypt automáticamente en el primer login exitoso
        new_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        db_client.update_one("usuarios_plataformas", "email", email, {"password": new_hash})
        print(f"Usuario {email} migrado a bcrypt con éxito.")
        return True

    return False

async def change_password(email: str) -> str:
    """Genera una nueva contraseña aleatoria y la actualiza en la BD."""
    new_password = generate_random_password()
    # Nota: Aquí la guardamos en texto plano para que el usuario pueda verla en el correo,
    # y se migrará a bcrypt en su próximo login exitoso.
    success = db_client.update_one("usuarios_metodos.usuarios_plataformas", "email", email, {"password": new_password})
    return new_password if success else None

def generate_random_password(length=7):
    """Genera una contraseña segura de longitud fija."""
    chars = string.ascii_letters + string.digits + '*@?¿¡!$#'
    return ''.join(random.choices(chars, k=length))

async def update_optional_terms(email: str, checked: bool):
    """Actualiza el estado de aceptación de términos opcionales."""
    return db_client.update_one("usuarios_plataformas", "email", email, {"is_optional_checked": checked})

def increment_login_count(email: str):
    """Incrementa el contador de inicios de sesión de un usuario."""
    try:
        user_data = db_client.find_one("usuarios_plataformas", "email", email)
        if user_data:
            current_count = int(user_data.get("count_login", 0))
            db_client.update_one("usuarios_plataformas", "email", email, {"count_login": current_count + 1})
    except Exception as e:
        print(f"Error incrementando login para {email}: {e}")
