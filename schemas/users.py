def user_schema(user):
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "password": user["password"]}

def users_schema(productos):
    return [user_schema(producto) for producto in productos]