import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from consts import URL
from service.service_tire import save_tire_info
from service.service_auth import JWTBearerForAdminOnly, authorize
import dto
from sql_app.crud import get_tire_info
from sql_app.database import get_db

from typing import List

router = APIRouter(prefix="/tire")


@router.post("/register", dependencies=[Depends(JWTBearerForAdminOnly())], tags=['tire'])
def create_user(tire_register_list: List[dto.TireRegister], db: Session = Depends(get_db),
                user_id: int = Depends(authorize)):
    success_list= []
    for tire_register in tire_register_list:
        trim_id = tire_register.trimId
        url = "".join([URL, str(trim_id)])
        try:
            response = requests.get(url, timeout=3)
        except Exception:
            raise Exception

        car_info = response.json()
        success_list = save_tire_info(car_info, db, tire_register, trim_id, user_id,success_list)

    return JSONResponse(content={"success_list": success_list}, status_code=200)


@router.get("/info", dependencies=[Depends(JWTBearerForAdminOnly())], tags=['tire'])
def tire_info(db: Session = Depends(get_db), user_id: int = Depends(authorize)):
    return get_tire_info(db, user_id)
