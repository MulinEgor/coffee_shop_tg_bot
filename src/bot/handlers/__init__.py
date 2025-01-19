from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from fastapi import HTTPException

from src.bot.handlers.barista import router as barista_router
from src.bot.handlers.base import router as base_router
from src.bot.handlers.client import router as client_router
from src.core.user.service import UserService


def register_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков."""
    # Регистрируем middleware для автоматического ответа на callback
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    # Регистрируем роутеры
    dp.include_router(base_router)
    dp.include_router(client_router)
    dp.include_router(barista_router)

    # Регистрируем обработчик всех остальных сообщений
    @dp.message(F.text.func(lambda text: not text.startswith("/")))
    async def handle_any_message(message: Message, user_service: UserService):
        """Обработчик всех остальных сообщений."""
        try:
            await user_service.get(message.from_user.id, False)
        except HTTPException:
            await message.answer(
                "Произошла ошибка при получении данных пользователя.\n"
                "Используйте /start для регистрации"
            )
            return

        await message.answer("Используйте /help чтобы увидеть список команд")
