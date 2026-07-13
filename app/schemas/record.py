from pydantic import BaseModel


class RecordCreate(BaseModel):
    token: str
    value: int