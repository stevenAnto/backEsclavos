from datetime import datetime, timezone

from app.services.google_auth import verify_google_token
from app.repositories.user_repository import get_user_by_email
from app.repositories.record_repository import create_record



def create_user_record(token: str, value: int):


    # Validar token Google
    google_user = verify_google_token(token)


    if not google_user or google_user.get("success") is False:
        return {
            "success": False,
            "message": "Token inválido"
        }


    email = google_user.get("email")


    # Buscar usuario
    user = get_user_by_email(email)


    if not user:
        return {
            "success": False,
            "message": "Usuario no registrado"
        }


    # Crear registro
    new_record = {

        "user_id": str(user["_id"]),

        "user_email": user["email"],

        "value": value,

        "created_at": datetime.now(timezone.utc)

    }


    record = create_record(new_record)


    return {
        "success": True,
        "message": "Registro creado",
        "record": record
    }