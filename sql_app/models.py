from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from .database import Base
from  sqlalchemy.types import Enum

from .schemas import TirePosition


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    register_id = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Tire(Base):
    __tablename__ = "tires"

    tire_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trim_id = Column(Integer)
    position = Column("position", Enum(TirePosition))
    width = Column(Integer)
    flatness_ratio = Column(Integer)
    wheel_size = Column(Integer)
