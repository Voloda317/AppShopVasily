import logging
from src.repositories.whels_rep import WheelRepository
from src.models.wheels import WheelOut, WheelCreate, WheelUpdate

logger = logging.getLogger(__name__)

class WheelService:
    def __init__(self, repository: WheelRepository):
        self.repository = repository

    def create_wheel(self, wheel_data: dict):
        wheel_id = self.repository.add(wheel_data)
        new_wheel = self.repository.get_by_id(wheel_id)
        if new_wheel is None:
            logger.error('Не удалось создать диск')
        else:
            logger.info(f'Диск создан с id {wheel_id}')
        return new_wheel

    def get_wheel(self, wheel_id: int):
        wheel = self.repository.get_by_id(wheel_id)
        if wheel:
            logger.info(f'Диск с id {wheel_id} найден')
        else:
            logger.warning(f'Диск с id {wheel_id} не найден')
        return wheel

    def delete(self, wheel_id: int):
        deleted = self.repository.delete(wheel_id)
        if deleted:
            logger.info(f'Диск с id {wheel_id} удален')
        else:
            logger.warning(f'Диск с id {wheel_id} не найден, удаление не выполнено')
        return deleted

    def update(self, wheel_id: int, wheel_data: dict):
        updated = self.repository.update(wheel_id, wheel_data)
        if updated:
            logger.info(f'Диск с id {wheel_id} обновлен')
        else:
            logger.error('Неизвестная ошибка при обновлении')
        return updated

    def search_for_wheel(self, filters: dict):
        results = self.repository.get_all(filters)
        if results:
            logger.info(f'Найдено {len(results)} дисков по фильтру')
        else:
            logger.info('Ни одного диска не найдено по фильтру')
        return results