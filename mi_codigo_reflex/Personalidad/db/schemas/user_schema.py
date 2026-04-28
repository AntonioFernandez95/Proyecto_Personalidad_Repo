

#*Devuelve un usuario*#
def user_schema(user):
    if not user: return {}
    
    # Formateo seguro de fechas
    h_perso = user.get("hasta_personalidad")
    h_fisicas = user.get("hasta_fisicas")
    
    return {
        "id": str(user.get("id", user.get("_id", ""))),        
        "disabled": bool(user.get("disabled", False)),
        "email": user.get("email", ""),
        "full_name": f"{user.get('nombre', '')} {user.get('apellidos', '')}".strip() or user.get("full_name", "Sin nombre"),
        "password": user.get("password"),
        "username": user.get("email", ""),
        "count_login": int(user.get("count_login", 0)),
        "are_terms_accepted": bool(user.get("are_terms_accepted", False)),
        "is_optional_checked": bool(user.get("is_optional_checked", False)),
        "rol": user.get("rol", "estudiante"),
        "hasta_personalidad": h_perso.strftime("%Y-%m-%d") if hasattr(h_perso, "strftime") else "N/A",
        "hasta_fisicas": h_fisicas.strftime("%Y-%m-%d") if hasattr(h_fisicas, "strftime") else "N/A",
        "disabled_personalidad": bool(user.get("disabled_personalidad", False)),
        "disabled_fisicas": bool(user.get("disabled_fisicas", False)),
    }

#*Devuelve un listado de usuarios*#
def users_schema(users) -> list:
    return [user_schema(user) for user in users]