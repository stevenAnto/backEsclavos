import requests


GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"


def verify_google_token(token: str):

    response = requests.get(
        GOOGLE_TOKEN_INFO_URL,
        params={"id_token": token}
    )

    if response.status_code != 200:
        return {
            "success": False,
            "message": "Token inválido"
        }

    return response.json()