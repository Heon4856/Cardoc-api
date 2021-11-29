import re

from dto import TirePosition
from sql_app import models
from sql_app.crud import create_tire_info


def is_tire_format(tire_info: str) -> bool:
    if re.match(r'\d+/\d+R\d+$', tire_info):
        return True
    return False


def save_tire_info(car_info, db, tire_register, trim_id, user_id, success_list):
    front_tire = car_info["spec"]["driving"]["frontTire"]["value"]
    rear_tire = car_info["spec"]["driving"]["rearTire"]["value"]

    if is_tire_format(front_tire):
        width, flatness_ratio, wheel_size = re.split('[/R]', front_tire)
        create_tire_info(db,
                         models.Tire(
                             user_id=user_id,
                             trim_id=trim_id,
                             position=TirePosition.FRONT,
                             width=width,
                             flatness_ratio=flatness_ratio,
                             wheel_size=wheel_size
                         )
                         )
        success_list.append(f'{tire_register} front_tire')

    if is_tire_format(rear_tire):
        width, flatness_ratio, wheel_size = re.split('[/R]', rear_tire)
        create_tire_info(db, models.Tire(
            user_id=user_id,
            trim_id=trim_id,
            position=TirePosition.REAR,
            width=width,
            flatness_ratio=flatness_ratio,
            wheel_size=wheel_size
        )
        )
        success_list.append(f'{tire_register} rear_tire')

    return success_list
