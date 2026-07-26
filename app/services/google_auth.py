import jwt
import requests
from fastapi import HTTPException
from datetime import datetime,timezone


GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"


def verify_google_token(token: str):
    try:
        payload=jwt.decode(
            token,
            options={"verify_signature": False}
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=400,
            detail="Token invalido"
        )
    exp = payload.get("exp")

    ahora = datetime.now(timezone.utc).timestamp()

    if exp < ahora:
        raise HTTPException(
            status_code=401,
            detail="Token expirado"
        )

    response = requests.get(
    GOOGLE_TOKEN_INFO_URL,
    params={"id_token": token}
)

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Token inválido"
         )

        
    return response.json()