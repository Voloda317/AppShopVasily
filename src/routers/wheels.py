from fastapi import APIRouter, Query, Depends
from typing import List, Optional
import logging

from src.repositories.whels_rep import WheelRepository
from src.services.wheel_service import WheelService
from src.models.wheels import WheelCreate, WheelOut, WheelUpdate

router = APIRouter(prefix='/wheels', tags=['Wheels'])

logger = logging.getLogger(__name__)

repo = WheelRepository()
service = WheelService(repo)

@router.get('/', response_model=List[WheelOut])
async def get_wheels():
    return service.search_for_wheel({})

@router.post('/', response_model=WheelOut)
async def create_wheel(wheel: WheelCreate):
    new_wheel = service.create_wheel(wheel.model_dump())
    if new_wheel is None:
        logger.error("Не удалось создать диск (сервис вернул None)")
    return new_wheel

@router.get('/search', response_model=List[WheelOut])
async def search_wheel(
    name: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    diameter: Optional[int] = Query(None),
    width: Optional[int] = Query(None),
    et: Optional[int] = Query(None),
    dia: Optional[float] = Query(None),
    pcd: Optional[str] = Query(None),
):
    filters = {
        key: value
        for key, value in {
            "name": name,
            "brand": brand,
            "model": model,
            "diameter": diameter,
            "width": width,
            "et": et,
            "dia": dia,
            "pcd": pcd,
        }.items()
        if value is not None
    }

    return service.search_for_wheel(filters)

@router.get('/{wheel_id}', response_model=WheelOut)
async def get_wheel(wheel_id: int):
    wheel = service.get_wheel(wheel_id)
    return wheel

@router.patch('/{wheel_id}', response_model=WheelOut)
async def update_wheel(wheel_id: int, wheel_update: WheelUpdate):
    update_data = wheel_update.model_dump(exclude_unset=True)
    updated_wheel = service.update(wheel_id, update_data)
    return updated_wheel

@router.delete('/{wheel_id}')
async def delete_wheel(wheel_id: int):
    service.delete(wheel_id)
    return {"deleted": True}