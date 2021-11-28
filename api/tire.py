import bcrypt
import requests
import re
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from service import service_user
from service.service_user import JWTBearerForAdminOnly, authorize
from sql_app import schemas, crud, models
from sql_app.crud import create_tire_info, get_tire_info
from sql_app.database import SessionLocal

from typing import List

from sql_app.schemas import TirePosition

router = APIRouter(prefix="/tire")

URL = "https://dev.mycar.cardoc.co.kr/v1/trim/"
timeout_seconds = 3


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", dependencies=[Depends(JWTBearerForAdminOnly())])
def create_user(tire_register_list: List[schemas.TireRegister], db: Session = Depends(get_db),
                user_id: int = Depends(authorize)):
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

    return "good"


@router.get("/info", dependencies=[Depends(JWTBearerForAdminOnly())])
def tire_info( db: Session = Depends(get_db), user_id: int = Depends(authorize)):

    return get_tire_info(db,user_id)




def is_tire_format(tire_info: str) -> bool:
    if re.match(r'\d+/\d+R\d+$', tire_info):
        return True
    return False
