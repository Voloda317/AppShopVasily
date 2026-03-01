from pydantic import BaseModel
from typing import Optional

class Tire(BaseModel):
    name: str
    brand: str
    model: str
    seasons: str
    width: int 
    height: int 
    radius: int 

class TireCreate(Tire):
    pass 

class TireOut(Tire):
    id: int 

class TireUpdate(BaseModel): 
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    seasons: Optional[str] = None
    width: Optional[int] = None  
    height: Optional[int] = None  
    radius: Optional[int] = None 