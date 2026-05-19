from pydantic import BaseModel, Field
from typing import Optional 

class UserModel(BaseModel):
    id: Optional[str] = None
    disabled: bool
    email: str
    full_name: str
    count_login: int = Field(default=0)
    rol: str = "estudiante"
    disabled_personalidad: bool = False
    disabled_fisicas: bool = False
    hasta_personalidad: str = "N/A"
    hasta_fisicas: str = "N/A"

class UserDBModel(UserModel):
    password: str
