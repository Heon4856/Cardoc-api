import requests
import re
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from service.service_user import JWTBearerForAdminOnly, authorize
from sql_app import models
import dto
from sql_app.crud import create_tire_info, get_tire_info
from sql_app.database import SessionLocal

from typing import List

from dto import TirePosition

router = APIRouter(prefix="/tire")

URL = "https://dev.mycar.cardoc.co.kr/v1/trim/"
timeout_seconds = 3


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", dependencies=[Depends(JWTBearerForAdminOnly())], tags=['tire'])
def create_user(tire_register_list: List[dto.TireRegister], db: Session = Depends(get_db),
                user_id: int = Depends(authorize)):
    success_list=[]
    for tire_register in tire_register_list:
        trim_id = tire_register.trimId
        url = "".join([URL, str(trim_id)])
        try:
            response = requests.get(url, timeout=3)
        except Exception:
            raise Exception
        else:
            car_info = response.json()

            front_tire = car_info["spec"]["driving"]["frontTire"]["value"]
            rear_tire = car_info["spec"]["driving"]["rearTire"]["value"]
            print(front_tire)
            tires = []
            if is_tire_format(front_tire):
                width, flat, wheel = re.split('[/R]', front_tire)
                create_tire_info(db,
                    models.Tire(
                        user_id=user_id,
                        trim_id=trim_id,
                        position=TirePosition.FRONT,
                        width=width,
                        flatness_ratio=flat,
                        wheel_size=wheel
                    )
                )
                success_list.append(f'{tire_register} front_tire')
            if is_tire_format(rear_tire):
                width, flat, wheel = re.split('[/R]', rear_tire)
                create_tire_info(db, models.Tire(
                    user_id=user_id,
                    trim_id=trim_id,
                    position=TirePosition.REAR,
                    width=width,
                    flatness_ratio=flat,
                    wheel_size=wheel
                )
                )
                success_list.append(f'{tire_register} rear_tire')


    return JSONResponse(content={"success_list":success_list}, status_code=200)


@router.get("/info", dependencies=[Depends(JWTBearerForAdminOnly())], tags=['tire'])
def tire_info( db: Session = Depends(get_db), user_id: int = Depends(authorize)):

    return get_tire_info(db,user_id)




def is_tire_format(tire_info: str) -> bool:
    if re.match(r'\d+/\d+R\d+$', tire_info):
        return True
    return False
