from pydantic import BaseModel, Field
from typing import Optional 

class UserModel(BaseModel):
    id: Optional[str] = None
    disabled: bool
    email: str
    full_name: str
    count_login: int = Field(default=0)
    are_terms_accepted: bool
    rol: str = "estudiante"
 


class UserDBModel(UserModel):
    password: str
