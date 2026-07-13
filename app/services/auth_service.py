from datetime import datetime

from app.services.google_auth import verify_google_token
from app.repositories.user_repository import (
    get_user_by_email,
    create_user,
    update_last_login
)


def authenticate_google(token: str):

    # 1. Validar token con Google
    google_user = verify_google_token(token)


    # 2. Si Google rechaza el token
    if not google_user or google_user.get("success") is False:
        return {
            "success": False,
            "message": "No se pudo autenticar con Google"
        }


    # 3. Extraer información del usuario
    email = google_user.get("email")


    if not email:
        return {
            "success": False,
            "message": "Google no devolvió email"
        }


    # 4. Buscar usuario en MongoDB
    user = get_user_by_email(email)


    # 5. Usuario existente
    if user:

        update_last_login(email)

        return {
            "success": True,
            "message": "Usuario existente",
            "user": {
                "id": str(user["_id"]),
                "email": user["email"],
                "name": user.get("name"),
                "picture": user.get("picture")
            }
        }


    # 6. Usuario nuevo
    new_user = {

        "email": email,

        "name": google_user.get("name"),

        "picture": google_user.get("picture"),

        "google_id": google_user.get("sub"),

        "created_at": datetime.utcnow(),

        "last_login": datetime.utcnow()
    }


    created_user = create_user(new_user)


    return {
        "success": True,
        "message": "Usuario creado",
        "user": {
            "id": str(created_user["_id"]),
            "email": created_user["email"],
            "name": created_user.get("name"),
            "picture": created_user.get("picture")
        }
    }