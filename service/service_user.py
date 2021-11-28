import jwt
from typing import Optional
from datetime import datetime, timedelta
from sql_app import schemas

from env import SECRET_KEY, ALGORITHM
import time

import jwt

from fastapi import Request, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def decodeJWT(token: str ) -> dict:
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token if decoded_token["exp"] >= time.time() else None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_token( user: schemas.User):
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"user_id": user.id, "authority": ["ADMIN"]},
                                       expires_delta=access_token_expires).decode("utf-8")
    token = dict(
        Authorization=f"Bearer {access_token}")
    return token


class JWTBearerForAdminOnly(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearerForAdminOnly, self).__init__(auto_error=auto_error)
        self.user_id = 0

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerForAdminOnly, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token or Not admin.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid



def authorize(authorization=Header(None)):
    token_without_bearer=authorization.split()[1]
    payload=decodeJWT(token_without_bearer)
    user_id = payload["user_id"]
    return user_id
