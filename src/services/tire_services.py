import logging

from src.repositories.tire_rep import TireRep
from src.models.tires import TireCreate, TireOut, TireUpdate

logger = logging.getLogger(__name__)

class TireService:
    def __init__(self, repository: TireRep):
        self.repository = repository

    def create_tire(self, tire_data: dict):
        tire_id = self.repository.add(tire_data)
        new_tire = self.repository.get_by_id(tire_id)
        if new_tire is None:
            logger.error('Не удалось создать шину')
        else:
            logger.info(f'Шина создана с id {tire_id}')
        return new_tire
    
    
    def get_tire(self, tire_id: int):
        tire = self.repository.get_by_id(tire_id)
        if tire:
            logger.info(f'Шина с id {tire_id} найдена')
        else:
            logger.warning(f'Шина с id {tire_id} не найдена')
        return tire
    

    def delete(self, tire_id: int):
        deleted = self.repository.delete(tire_id)
        if deleted:
            logger.info(f'Шина с id {tire_id} удалена')
        else:
            logger.warning(f'Шина с id {tire_id} не найдена, удаление не выполнено')
        return deleted
    

    def update(self, tire_id: int, tire_data: dict):
        updated = self.repository.update(tire_id, tire_data)
        if updated:
            logger.info(f'Шина с id {tire_id} обновлена')
        else:
            logger.error('Неизвестная ошибка при обновлении')
        return updated


    def search_for_tire(self, filters: dict):
        results = self.repository.get_all(filters)
        if results:
            logger.info(f'ВСе хорошо')
        else:
            logger.info('Ни одной шины не найдено по фильтру')
        return results
