from pydantic import BaseModel

class UserRegister(BaseModel):
    register_id: str = None
    pw: str = None


class Token(BaseModel):
    Authorization: str = None


class User(BaseModel):
    id :int
    register_id :str
    hashed_password : str
    is_active : bool

    class Config:
        orm_mode = True