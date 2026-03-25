

#*Devuelve un usuario*#
def user_schema(user):
    return {
        "id": str(user.get("id", user.get("_id", ""))),        
        "disabled": user.get("disabled", False),
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "password": user.get("password"),
        "username": user.get("username"),
        "count_login": int(user.get("count_login", 0)),
        "are_terms_accepted": user.get("are_terms_accepted", False),

    }

#*Devuelve un listado de usuarios*#
def users_schema(users) -> list:
    return [user_schema(user) for user in users]