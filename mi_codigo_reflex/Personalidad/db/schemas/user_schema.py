

#*Devuelve un usuario*#
def user_schema(user):
    if not user: return {}
    
    # Formateo seguro de fechas (usamos 'hasta' unificado si no existen las específicas)
    h_perso = user.get("hasta_personalidad") or user.get("hasta")
    h_fisicas = user.get("hasta_fisicas") or user.get("hasta")
    
    # Estados de baja (usamos 'disabled' unificado si no existen las específicas)
    d_perso = user.get("disabled_personalidad", user.get("disabled", False))
    d_fisicas = user.get("disabled_fisicas", user.get("disabled", False))
    
    # Función para convertir a booleano real (soporta strings "true"/"false")
    def to_bool(val):
        if isinstance(val, bool): return val
        if isinstance(val, str):
            return val.lower() in ("true", "1", "yes", "t")
        return bool(val)

    return {
        "id": str(user.get("id", user.get("_id", ""))),        
        "disabled": to_bool(user.get("disabled", False)),
        "email": user.get("email", ""),
        "full_name": f"{user.get('nombre', '')} {user.get('apellidos', '')}".strip() or user.get("full_name", "Sin nombre"),
        "password": user.get("password") or "",
        "username": user.get("email", ""),
        "count_login": int(user.get("count_login", 0)),
        "rol": user.get("rol", "estudiante"),
        "hasta_personalidad": h_perso.strftime("%Y-%m-%d") if hasattr(h_perso, "strftime") else "N/A",
        "hasta_fisicas": h_fisicas.strftime("%Y-%m-%d") if hasattr(h_fisicas, "strftime") else "N/A",
        "disabled_personalidad": to_bool(d_perso),
        "disabled_fisicas": to_bool(d_fisicas),
    }

#*Devuelve un listado de usuarios*#
def users_schema(users) -> list:
    return [user_schema(user) for user in users]