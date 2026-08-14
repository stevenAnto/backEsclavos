from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.services.google_auth import verify_google_token
from app.repositories.user_repository import get_user_by_email
from app.repositories.record_repository import create_record, get_user_records, update_record_value
from app.repositories.record_repository import get_total_by_user




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


def get_user_summary_by_email(email: str):

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

def get_user_records_by_email(email: str):

    user = get_user_by_email(email)

    if not user:
        return {
            "success": False,
            "message": "Usuario no encontrado",
            "status_code": 404
        }

    records = get_user_records(
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
        "records": records
    }


import pandas as pd

from datetime import datetime

from app.repositories.user_repository import get_user_by_email
from app.repositories.record_repository import create_records


def import_excel_records(file):

    df = pd.read_excel(
        file,
        header=None
    )

    records = []
    errors = []

    # Primera fila = nombres
    names = df.iloc[0]

    # Segunda fila = correos
    emails = df.iloc[1]

    # ---------------------------------------------------------
    # Recorrer datos
    # ---------------------------------------------------------

    for row_index in range(2, len(df)):

        row = df.iloc[row_index]

        date_value = row.iloc[0]

        # Ignorar filas sin fecha
        if pd.isna(date_value):
            continue

        # Ignorar filas TOTAL
        if "TOTAL" in str(date_value).upper():
            continue

        # -----------------------------------------------------
        # Fecha
        # -----------------------------------------------------

        try:

            record_date = pd.to_datetime(date_value).to_pydatetime()

            record_date = record_date.replace(
                tzinfo=ZoneInfo("America/Lima")
            )

        except Exception:

            errors.append({
                "row": row_index + 1,
                "error": f"Fecha inválida: {date_value}"
            })

            continue

        # -----------------------------------------------------
        # Usuarios
        # -----------------------------------------------------

        for column_index in range(1, len(df.columns)):

            name = names.iloc[column_index]

            email = emails.iloc[column_index]

            value = row.iloc[column_index]

            # -------------------------------------------------
            # No hay correo -> ignorar
            # -------------------------------------------------

            if pd.isna(email):
                continue

            email = str(email).strip()

            if not email:
                continue

            # -------------------------------------------------
            # Valor vacío -> ignorar
            # -------------------------------------------------

            if pd.isna(value):
                continue

            # -------------------------------------------------
            # "-" -> ignorar
            # -------------------------------------------------

            if str(value).strip() == "-":
                continue

            # -------------------------------------------------
            # Buscar usuario
            # -------------------------------------------------

            user = get_user_by_email(email)

            if not user:

                errors.append({
                    "row": row_index + 1,
                    "name": str(name),
                    "email": email,
                    "error": "Usuario no encontrado"
                })

                continue

            # -------------------------------------------------
            # Convertir valor
            # -------------------------------------------------

            try:

                value = int(value)

            except (ValueError, TypeError):

                errors.append({
                    "row": row_index + 1,
                    "name": str(name),
                    "email": email,
                    "value": value,
                    "error": "Valor inválido"
                })

                continue

            # -------------------------------------------------
            # Crear registro
            # -------------------------------------------------

            records.append({

                "user_id": str(user["_id"]),

                "user_email": user["email"],

                "value": value,

                "created_at": record_date

            })

    # ---------------------------------------------------------
    # Insertar
    # ---------------------------------------------------------

    inserted = create_records(records)

    return {

        "success": True,

        "message": "Excel importado correctamente",

        "inserted": inserted,

        "errors": errors

    }

def update_user_record_value(record_id: str, value: int):

    try:
        result = update_record_value(
            record_id,
            value
        )

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

    if result.matched_count == 0:
        return {
            "success": False,
            "message": "Registro no encontrado",
            "status_code": 404
        }

    return {
        "success": True,
        "message": "Valor actualizado correctamente"
    }
