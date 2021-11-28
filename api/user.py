import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from service import service_user
from sql_app import schemas, crud
from sql_app.database import SessionLocal

router = APIRouter(prefix="/auth")
#
# @router.post("/register}", status_code=201, response_model=Token)
# async def register( reg_info: UserRegister, session: Session = Depends(db.session)):
#     """
#     `회원가입 API`\n
#     :param session:
#     :return:
#     """
#     if sns_type == SnsType.email:
#         is_exist = await is_email_exist(reg_info.register_id)
#         if not reg_info.email or not reg_info.pw:
#             return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
#         if is_exist:
#             return JSONResponse(status_code=400, content=dict(msg="EMAIL_EXISTS"))
#         hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
#         new_user = Users.create(session, auto_commit=True, pw=hash_pw, email=reg_info.email)
#         token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'pw', 'marketing_agree'}),)}")
#         return token
#     return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))
#
#
# async def is_email_exist(email: str):
#     get_email = Users.get(email=email)
#     if get_email:
#         return True
#     return False
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/auth/register", response_model=schemas.User)
def create_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_register_id(db, register_id=user.register_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@router.post("/auth/login", response_model=schemas.Token)
def login(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_register_id(db, register_id=user.register_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(user.pw.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        return HTTPException(status_code=400, detail="패스워드를 확인해주세요")
    create_token = service_user.create_token(db_user)

    return create_token