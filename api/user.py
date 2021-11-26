from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models import UserRegister, Token

router = APIRouter(prefix="/auth")

@router.post("/register}", status_code=201, response_model=Token)
async def register( reg_info: UserRegister, session: Session = Depends(db.session)):
    """
    `회원가입 API`\n
    :param session:
    :return:
    """
    if sns_type == SnsType.email:
        is_exist = await is_email_exist(reg_info.register_id)
        if not reg_info.email or not reg_info.pw:
            return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
        if is_exist:
            return JSONResponse(status_code=400, content=dict(msg="EMAIL_EXISTS"))
        hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
        new_user = Users.create(session, auto_commit=True, pw=hash_pw, email=reg_info.email)
        token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'pw', 'marketing_agree'}),)}")
        return token
    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))


async def is_email_exist(email: str):
    get_email = Users.get(email=email)
    if get_email:
        return True
    return False