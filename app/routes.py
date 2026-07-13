from fastapi import APIRouter
from app.schemas.auth import GoogleToken
from app.services.auth_service import authenticate_google
from app.database import users_collection


router = APIRouter()


@router.post("/auth/google")
def google_login(data: GoogleToken):
    return authenticate_google(data.token)


@router.get("/test-mongo")
def test_mongo():

    usuario = {
        "nombre": "Stv",
        "email": "steven.undefined@gmail.com"
    }

    resultado = users_collection.insert_one(usuario)

    return {
        "mensaje": "Usuario creado",
        "id": str(resultado.inserted_id)
    }