import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from service import service_auth
from sql_app import crud
import dto
from sql_app.database import get_db

router = APIRouter(prefix="/auth")



@router.post("/register", response_model=dto.User, tags=['auth'])
def create_user(user: dto.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_register_id(db, register_id=user.register_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@router.post("/login", response_model=dto.Token, tags=['auth'])
def login(user: dto.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_register_id(db, register_id=user.register_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(user.pw.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        return HTTPException(status_code=400, detail="패스워드를 확인해주세요")
    create_token = service_auth.create_token(db_user)

    return create_token