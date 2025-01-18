from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.core.settings import settings
from src.core.db import create_all_tables
from src.api.settings import api_settings
from src.api.category.router import router as category_router
from src.api.position.router import router as position_router
from src.api.order.router import router as order_router
from src.api.user.router import router as user_router


# Настройка API
app = FastAPI(
    **api_settings.model_dump()
)


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    **api_settings.cors.model_dump()
)


# Включение роутеров
routers = [category_router, position_router, order_router, user_router]
for router in routers:
    app.include_router(router)


# Создание таблиц в БД
@app.on_event("startup")
async def startup():
    await create_all_tables()
    
    
if __name__ == "__main__":
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
