from pydantic import BaseModel


class BaseProfile(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    phone_number: str
    position: str
    unique_id: int
