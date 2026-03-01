from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from src.logger.logger import setup_logging
from src.config.config import settings
from src.routers.tires import router as tires_router
from src.routers.wheels import router as wheels_router
from src.repositories.tire_rep import TireRep
from src.repositories.whels_rep import WheelRepository

setup_logging()
logger = logging.getLogger(__name__)

tire_repo = TireRep()
wheel_repo = WheelRepository()

@asynccontextmanager
async def lifespan(app: FastAPI):
    tire_repo.create_table()
    wheel_repo.create_table()
    logger.info('Сервер начал работу')
    yield
    logger.info('Сервер завершил работу')

app = FastAPI(lifespan=lifespan, title=settings.APP_TITLE)

app.include_router(tires_router)
app.include_router(wheels_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=True)