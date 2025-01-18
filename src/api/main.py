from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.settings import api_settings
from src.api.category.router import router as category_router
from src.api.position.router import router as position_router


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
routers = [category_router, position_router]
for router in routers:
    app.include_router(router)
    