import requests
from fastapi import HTTPException


GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"


def verify_google_token(token: str):

    try:
        response = requests.get(
            GOOGLE_TOKEN_INFO_URL,
            params={"id_token": token}
         )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Token invalido o expirado"
        )


        
    return response.json()