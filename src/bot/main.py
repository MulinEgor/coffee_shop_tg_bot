import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.callbacks import register_callbacks
from src.bot.handlers import register_handlers
from src.bot.middlewares import register_middlewares
from src.core.settings import settings


async def main():
    """
    Точка входа бота.
    """
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация обработчиков, middleware и callbackов
    register_handlers(dp)
    register_middlewares(dp)
    register_callbacks(dp)

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
