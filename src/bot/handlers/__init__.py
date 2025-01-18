from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from src.bot.handlers.base import router as base_router
from src.bot.handlers.client import router as client_router
from src.bot.handlers.barista import router as barista_router


def register_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков."""
    # Регистрируем middleware для автоматического ответа на callback
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    
    # Регистрируем роутеры
    dp.include_router(base_router)
    dp.include_router(client_router)
    dp.include_router(barista_router) 
    