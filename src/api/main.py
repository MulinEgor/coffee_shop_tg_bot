import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.category.router import router as category_router
from src.api.order.router import router as order_router
from src.api.position.router import router as position_router
from src.api.settings import api_settings
from src.api.user.router import router as user_router
from src.core.settings import settings

# Настройка API
app = FastAPI(**api_settings.model_dump())


# Настройка CORS
app.add_middleware(CORSMiddleware, **api_settings.cors.model_dump())


# Включение роутеров
routers = [category_router, position_router, order_router, user_router]
for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
