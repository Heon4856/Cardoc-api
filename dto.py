from pydantic import BaseModel, conint
from typing import List
from enum import Enum

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

class TirePosition(Enum):
    FRONT = "FRONT"
    REAR = "REAR"


class TireInfo(BaseModel):
    trim_id: int
    position: TirePosition
    width: conint(gt=0)
    flatness_ratio: conint(gt=0)
    wheel_size: conint(gt=0)
    class Config:
        orm_mode = True