import bcrypt
import random
import string
from datetime import datetime
from Personalidad.db.client import db_client
from Personalidad.db.schemas.user_schema import user_schema
from Personalidad.db.models.user_model import UserModel, UserDBModel


def _sync_expiration(email: str, user_data: dict):
    """
    Comprueba si los planes han caducado y actualiza los flags en PostgreSQL.
    Solo escribe en la BD si hay un cambio de estado (evita escrituras innecesarias).
    Los admins están siempre exentos de caducidad.
    """
    if user_data.get("rol") == "admin":
        return  # Los admins nunca caducan

    updates = {}
    now = datetime.now()

    # Función auxiliar para parsear fechas de forma segura
    def parse_fecha(v):
        if not v or v == "N/A": return None
        if isinstance(v, datetime): return v
        try:
            from dateutil import parser as dateutil_parser
            return dateutil_parser.parse(str(v))
        except: return None
        
    def to_bool(val):
        if isinstance(val, bool): return val
        if isinstance(val, str): return val.lower() in ("true", "1", "yes", "t")
        return bool(val)

    # Evaluación de FÍSICAS
    hasta_fisicas = parse_fecha(user_data.get("hasta_fisicas")) or parse_fecha(user_data.get("hasta"))
    is_fisicas_expired = (hasta_fisicas is None) or (hasta_fisicas < now)
    current_disabled_fisicas = to_bool(user_data.get("disabled_fisicas")) or to_bool(user_data.get("disabled", False))

    if is_fisicas_expired and not current_disabled_fisicas:
        updates["disabled_fisicas"] = True
        updates["disabled"] = True

    # Evaluación de PERSONALIDAD
    hasta_personalidad = parse_fecha(user_data.get("hasta_personalidad")) or parse_fecha(user_data.get("hasta"))
    is_perso_expired = (hasta_personalidad is None) or (hasta_personalidad < now)
    current_disabled_perso = to_bool(user_data.get("disabled_personalidad")) or to_bool(user_data.get("disabled", False))

    if is_perso_expired and not current_disabled_perso:
        updates["disabled_personalidad"] = True
        updates["disabled"] = True

    if updates:
        db_client.update_one("usuarios_plataformas", "email", email, updates)


def search_user(field: str, key) -> UserModel:
    """Busca un usuario en la BD, sincroniza su caducidad y devuelve su modelo."""
    try:
        user_data = db_client.find_one("usuarios_plataformas", field, key)
        if not user_data:
            return None

        # Sincronización automática de caducidad (solo cuando buscamos por email)
        if field == "email":
            _sync_expiration(key, user_data)
            # Releemos los datos frescos para que el modelo refleje el estado actualizado
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
    if db_password.startswith("$2") and len(db_password) >= 50:
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
    success = db_client.update_one("usuarios_metodos.usuarios_plataformas", "email", email, {"password": new_password})
    return new_password if success else None


def generate_random_password(length=7):
    """Genera una contraseña segura de longitud fija."""
    chars = string.ascii_letters + string.digits + '*@?¿¡!$#'
    return ''.join(random.choices(chars, k=length))



def increment_login_count(email: str):
    """Incrementa el contador de inicios de sesión de un usuario."""
    try:
        user_data = db_client.find_one("usuarios_plataformas", "email", email)
        if user_data:
            current_count = int(user_data.get("count_login", 0))
            db_client.update_one("usuarios_plataformas", "email", email, {"count_login": current_count + 1})
    except Exception as e:
        print(f"Error incrementando login para {email}: {e}")
