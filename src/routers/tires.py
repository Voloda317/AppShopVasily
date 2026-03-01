from fastapi import APIRouter, Query, Depends
from typing import List, Optional
import logging

from src.repositories.tire_rep import TireRep
from src.services.tire_services import TireService
from src.models.tires import TireOut, TireUpdate, TireCreate

router = APIRouter(prefix='/tires', tags=['Tires'])

logger = logging.getLogger(__name__)

repo = TireRep()
service = TireService(repo)

@router.get('/', response_model=List[TireOut])
async def get_tires():
    return service.search_for_tire({})

@router.post('/', response_model=TireOut)
async def create_tire(tire: TireCreate):
    new_tire = service.create_tire(tire.model_dump())
    if new_tire is None:
        logger.error("Не удалось создать шину (сервис вернул None)")
    return new_tire

@router.get('/search', response_model=List[TireOut])
async def search_tire(
    name: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    seasons: Optional[str] = Query(None),
    width: Optional[int] = Query(None),
    height: Optional[int] = Query(None),
    radius: Optional[int] = Query(None),
):
    filters = {
        key: value
        for key, value in {
            "name": name,
            "brand": brand,
            "model": model,
            "seasons": seasons,
            "width": width,
            "height": height,
            "radius": radius,
        }.items()
        if value is not None
    }

    return service.search_for_tire(filters)
# @router.get('/search', response_model=List[TireOut])
# async def search_tire(
#     name: Optional[str] = Query(None),
#     brand: Optional[str] = Query(None),
#     model: Optional[str] = Query(None),
#     seasons: Optional[str] = Query(None),
#     width: Optional[int] = Query(None),
#     height: Optional[int] = Query(None),
#     radius: Optional[int] = Query(None)
#     ):
#     filters = {}
#     if name: filters['name'] = name
#     if brand: filters['brand'] = brand
#     if model: filters['model'] = model
#     if seasons: filters['seasons'] = seasons
#     if width: filters['width'] = width
#     if height: filters['height'] = height
#     if radius: filters['radius'] = radius

#     return service.search_for_tire(filters)

@router.get('/{tire_id}', response_model=TireOut)
async def get_tire(tire_id: int):
    tire = service.get_tire(tire_id)
    return tire


@router.patch('/{tire_id}', response_model=TireOut)
async def update_tire(tire_id: int, tire_update: TireUpdate):
    update_data = tire_update.model_dump(exclude_unset=True)
    updated_tire = service.update(tire_id, update_data)
    return updated_tire

@router.delete('/{tire_id}')
async def delete_tire(tire_id: int):
    service.delete(tire_id)
    return {"deleted": True}