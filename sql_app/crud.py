from sqlalchemy.orm import Session
import bcrypt
from . import models
import dto
from pydantic import parse_obj_as
from typing import List

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_register_id(db: Session, register_id: str):
    return db.query(models.User).filter(models.User.register_id == register_id).first()


def create_user(db: Session, user: dto.UserRegister):
    hashed_password = bcrypt.hashpw(user.pw.encode("utf-8"), bcrypt.gensalt()).decode()
    db_user = models.User(register_id=user.register_id, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_tire_info(db: Session, tire: models.Tire):
    db.add(tire)
    db.commit()
    db.refresh(tire)
    return tire

def get_tire_info(db: Session, user_id: int):
    tire_list = db.query(models.Tire).filter(models.Tire.user_id == user_id).all()
    return parse_obj_as(List[dto.TireInfo], tire_list)
