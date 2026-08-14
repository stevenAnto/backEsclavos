from fastapi import APIRouter, File, Query, UploadFile
from app.schemas.auth import GoogleToken
from app.services.auth_service import authenticate_google
from app.database import users_collection
from app.schemas.record import RecordCreate, RecordValueUpdate
from app.services.record_services import create_user_record, get_user_records_by_email, get_user_summary_by_email, import_excel_records, update_user_record_value
from app.services.report_service import get_all_summary, get_user_summary, get_user_records_summary
from fastapi import HTTPException



router = APIRouter()


@router.post("/auth/google")
def google_login(data: GoogleToken):
    return authenticate_google(data.token)


@router.post("/records")
def create_record_endpoint(data: RecordCreate):

    return create_user_record(
        data.token,
        data.value
    )

@router.post("/records/summary")
def records_summary(data: GoogleToken):

    response = get_user_summary(data.token)

    if response.get("success") is False:

        raise HTTPException(
            status_code=response["status_code"],
            detail=response["message"]
        )

    return response


@router.post("/records/all-summary")
def all_summary(data: GoogleToken):

    response = authenticate_google(data.token)

    if response.get("success") is False:
        raise HTTPException(
            status_code=response["status_code"],
            detail=response["message"]
        )

    return get_all_summary()

@router.post("/records/history")
def records_history(data: GoogleToken):

    response = get_user_records_summary(data.token)

    if response.get("success") is False:

        raise HTTPException(
            status_code=response["status_code"],
            detail=response["message"]
        )

    return response

@router.get("/records/summary")
def records_summary(email: str = Query(...)):

    response = get_user_summary_by_email(email)

    if response.get("success") is False:
        raise HTTPException(
            status_code=response["status_code"],
            detail=response["message"]
        )

    return response

@router.get("/records/history")
def records_history(email: str = Query(...)):

    response = get_user_records_by_email(email)

    if response.get("success") is False:
        raise HTTPException(
            status_code=response["status_code"],
            detail=response["message"]
        )

    return response

@router.get("/records/all-summary")
def all_summary():

    return get_all_summary()

@router.post("/records/import-excel")
async def import_excel(
    file: UploadFile = File(...)
):

    result = import_excel_records(
        file.file
    )

    return result

@router.patch("/records/{record_id}/value")
def update_record_value_endpoint(
    record_id: str,
    data: RecordValueUpdate
):

    response = update_user_record_value(
        record_id,
        data.value
    )

    if response.get("success") is False:

        raise HTTPException(
            status_code=response.get("status_code", 500),
            detail=response["message"]
        )

    return response