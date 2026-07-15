from app.services.google_auth import verify_google_token
from app.repositories.user_repository import get_user_by_email
from app.repositories.record_repository import get_all_users_summary, get_total_by_user



def get_user_summary(token: str):


    google_user = verify_google_token(token)


    if not google_user or google_user.get("success") is False:

        return {
            "success": False,
            "message": "Token inválido",
            "status_code": 401
        }


    email = google_user.get("email")


    user = get_user_by_email(email)


    if not user:

        return {
            "success": False,
            "message": "Usuario no encontrado",
            "status_code": 404
        }


    totals = get_total_by_user(
        str(user["_id"])
    )


    return {

        "success": True,

        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "name": user.get("name"),
            "picture": user.get("picture")
        },

        "summary": totals

    }

def get_all_summary():

    return get_all_users_summary()