import sqlite3
from contextlib import contextmanager
from typing import Optional, List
import logging

from src.config.config import settings
from src.models.wheels import WheelOut

logger = logging.getLogger(__name__)

class WheelRepository:
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
                    CREATE TABLE IF NOT EXISTS wheels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        brand TEXT NOT NULL,
                        model TEXT NOT NULL,
                        diameter INTEGER NOT NULL,
                        width INTEGER NOT NULL,
                        et INTEGER,
                        dia REAL,
                        pcd TEXT
                    )
                ''')
                conn.commit()
            logger.info('Таблица wheels успешно создана')
        except Exception as e:
            logger.error(f'Не удалось создать таблицу wheels: {e}')


    def add(self, wheel_data: dict) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(
                '''
                INSERT INTO wheels (name, brand, model, diameter, width, et, dia, pcd)
                VALUES (:name, :brand, :model, :diameter, :width, :et, :dia, :pcd)
                ''', wheel_data
            )
            conn.commit()
            return cursor.lastrowid


    def get_by_id(self, wheel_id: int) -> Optional[WheelOut]:
        with self.get_connection() as conn:
            row = conn.execute(
                'SELECT id, name, brand, model, diameter, width, et, dia, pcd FROM wheels WHERE id = ?',
                (wheel_id,)
            ).fetchone()
            if row:
                wheel = WheelOut(**row)
                logger.info(f'Диск с id {wheel_id} найден')
                return wheel
            logger.warning(f'Диск с id {wheel_id} не найден')
            return None


    def delete(self, wheel_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.execute('DELETE FROM wheels WHERE id = ?', (wheel_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Диск с id {wheel_id} удален")
            else:
                logger.warning(f"Диск с id {wheel_id} не найден, удаление не выполнено")
            return deleted


    def update(self, wheel_id: int, wheel_data: dict) -> Optional[WheelOut]:
        fields = []
        values = []
        for key, value in wheel_data.items():
            if value is not None and key in ['name', 'brand', 'model', 'diameter', 'width', 'et', 'dia', 'pcd']:
                fields.append(f"{key} = ?")
                values.append(value)
        if not fields:
            return self.get_by_id(wheel_id)

        values.append(wheel_id)
        with self.get_connection() as conn:
            conn.execute(
                f'''
                UPDATE wheels
                SET {', '.join(fields)}
                WHERE id = ?
                ''',
                values
            )
            conn.commit()
            return self.get_by_id(wheel_id)


    def get_all(self, filters: Optional[dict] = None) -> List[WheelOut]:
        with self.get_connection() as conn:
            sql = 'SELECT id, name, brand, model, diameter, width, et, dia, pcd FROM wheels'
            params = []
            if filters:
                conds = []
                for key, val in filters.items():
                    if key in ('name', 'brand', 'model'):
                        conds.append(f"{key} LIKE ?")
                        params.append(f"%{val}%")
                    elif key in ('diameter', 'width', 'et', 'dia', 'pcd'):
                        conds.append(f"{key} = ?")
                        params.append(val)
                    elif key == 'id':
                        conds.append("id = ?")
                        params.append(val)
                if conds:
                    sql += ' WHERE ' + ' AND '.join(conds)
            rows = conn.execute(sql, params).fetchall()
            return [WheelOut(**row) for row in rows]
        