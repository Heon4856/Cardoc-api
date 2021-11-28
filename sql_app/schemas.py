from pydantic import BaseModel
from typing import List


class UserRegister(BaseModel):
    register_id: str = None
    pw: str = None


class TireRegister(BaseModel):
    id: str = None
    trimId: int = None


class TireRegisterList(BaseModel):
    tire_register_list: List[TireRegister] = None


class Token(BaseModel):
    Authorization: str = None


class User(BaseModel):
    id: int
    register_id: str
    hashed_password: str
    is_active: bool

    class Config:
        orm_mode = True
