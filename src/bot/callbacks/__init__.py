from aiogram import Dispatcher

from src.bot.callbacks.base import router as base_router
from src.bot.callbacks.client import router as client_router
from src.bot.callbacks.barista import router as barista_router


def register_callbacks(dp: Dispatcher):
    """Регистрация всех callback-обработчиков."""
    dp.include_router(base_router)
    dp.include_router(client_router)
    dp.include_router(barista_router) 
    