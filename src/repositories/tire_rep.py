import sqlite3
from contextlib import contextmanager
from typing import Optional, List
import logging

from src.config.config import settings
from src.models.tires import TireOut

logger = logging.getLogger(__name__)

class TireRep:
    def __init__(self, db_path: str = settings.DB_NAME):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def create_table(self):
        try:
            with self.get_connection() as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS tires (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        brand TEXT NOT NULL,
                        model TEXT NOT NULL,
                        seasons TEXT NOT NULL,
                        width INTEGER NOT NULL,
                        height INTEGER NOT NULL,
                        radius INTEGER NOT NULL
                    )
                ''')
                conn.commit()
            logger.info('Таблица tires успешно создана')
        except Exception as e:
            logger.error(f'Не удалось создать таблицу tires: {e}')

    def add(self, tire_data: dict) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(
                '''
                INSERT INTO tires (name, brand, model, seasons, width, height, radius)
                VALUES (:name, :brand, :model, :seasons, :width, :height, :radius)
                ''', tire_data
            )
            conn.commit()
            return cursor.lastrowid

    def get_by_id(self, tire_id: int) -> Optional[TireOut]:
        with self.get_connection() as conn:
            row = conn.execute(
                'SELECT id, name, brand, model, seasons, width, height, radius FROM tires WHERE id = ?',
                (tire_id,)
            ).fetchone()
            if row:
                tire = TireOut(**row)
                logger.info(f'Шина с id {tire_id} найдена')
                return tire
            logger.warning(f'Шина с id {tire_id} не найдена')
            return None

    def delete(self, tire_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.execute('DELETE FROM tires WHERE id = ?', (tire_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Шина с id {tire_id} удалена")
            else:
                logger.warning(f"Шина с id {tire_id} не найдена, удаление не выполнено")
            return deleted

    def update(self, tire_id: int, tire_data: dict) -> Optional[TireOut]:
        # Динамически строим SET на основе переданных полей
        fields = []
        values = []
        for key, value in tire_data.items():
            if value is not None and key in ['name', 'brand', 'model', 'seasons', 'width', 'height', 'radius']:
                fields.append(f"{key} = ?")
                values.append(value)
        if not fields:
            return self.get_by_id(tire_id)

        values.append(tire_id)
        with self.get_connection() as conn:
            conn.execute(
                f'''
                UPDATE tires
                SET {', '.join(fields)}
                WHERE id = ?
                ''',
                values
            )
            conn.commit()
            return self.get_by_id(tire_id)

    def get_all(self, filters: Optional[dict] = None) -> List[TireOut]:
        with self.get_connection() as conn:
            sql = 'SELECT id, name, brand, model, seasons, width, height, radius FROM tires'
            params = []
            if filters:
                conds = []
                for key, val in filters.items():
                    if key in ('name', 'brand', 'model', 'seasons'):
                        conds.append(f"{key} LIKE ?")
                        params.append(f"%{val}%")
                    elif key in ('width', 'height', 'radius'):
                        conds.append(f"{key} = ?")
                        params.append(val)
                    elif key == 'id':
                        conds.append("id = ?")
                        params.append(val)
                if conds:
                    sql += ' WHERE ' + ' AND '.join(conds)
            rows = conn.execute(sql, params).fetchall()
            return [TireOut(**row) for row in rows]