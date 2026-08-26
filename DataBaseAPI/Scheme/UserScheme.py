from pydantic import BaseModel, Field
from typing import Optional

class UserScheme(BaseModel):
    tg_id: str = Field(min_length=1)
    tg_name: Optional[str]

class UserWithIdScheme(UserScheme):
    id: int

class UserOnlyIdScheme(BaseModel):
    id: int

class UserAllOptional(BaseModel):
    tg_id: Optional[str]
    tg_name: Optional[str]
    id: Optional[int]