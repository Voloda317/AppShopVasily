from pydantic import BaseModel
from typing import Optional

class Wheel(BaseModel):
    name: str
    brand: str
    model: str
    diameter: int          # диаметр (R)
    width: int             # ширина обода
    et: Optional[int] = None     # вылет (может отсутствовать)
    dia: Optional[float] = None  # диаметр ступицы
    pcd: Optional[str] = None    # сверловка, например "5x112"

class WheelCreate(Wheel):
    pass

class WheelOut(Wheel):
    id: int

class WheelUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    diameter: Optional[int] = None
    width: Optional[int] = None
    et: Optional[int] = None
    dia: Optional[float] = None
    pcd: Optional[str] = None