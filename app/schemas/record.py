from pydantic import BaseModel


class RecordCreate(BaseModel):
    token: str
    value: int

class RecordValueUpdate(BaseModel):
    value: int