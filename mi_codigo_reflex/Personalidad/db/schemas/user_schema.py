

#*Devuelve un usuario*#
def user_schema(user):
    return {
        "id": str(user.get("id", user.get("_id", ""))),        
        "disabled": bool(user.get("disabled", False)),
        "email": user.get("email"),
        "full_name": f"{user.get('nombre', '')} {user.get('apellidos', '')}".strip() or user.get("full_name", ""),
        "password": user.get("password"),
        "username": user.get("email"), # Usamos email como username por defecto
        "count_login": int(user.get("count_login", 0)),
        "are_terms_accepted": bool(user.get("are_terms_accepted", False)),
        "is_optional_checked": bool(user.get("is_optional_checked", False)),
        "rol": user.get("rol", "estudiante"),
        "hasta_personalidad": user.get("hasta_personalidad").strftime("%Y-%m-%d") if user.get("hasta_personalidad") else "N/A",
        "hasta_fisicas": user.get("hasta_fisicas").strftime("%Y-%m-%d") if user.get("hasta_fisicas") else "N/A",
        "disabled_personalidad": bool(user.get("disabled_personalidad", False)),
        "disabled_fisicas": bool(user.get("disabled_fisicas", False)),
    }

#*Devuelve un listado de usuarios*#
def users_schema(users) -> list:
    return [user_schema(user) for user in users]