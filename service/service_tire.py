import re

def is_tire_format(tire_info: str) -> bool:
    if re.match(r'\d+/\d+R\d+$', tire_info):
        return True
    return False