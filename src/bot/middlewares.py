from typing import Any, Awaitable, Callable, Dict

from aiogram import Dispatcher
from aiogram.types import TelegramObject

from src.core.category.dependencies import get_category_service
from src.core.order.dependencies import get_order_service
from src.core.position.dependencies import get_position_service
from src.core.user.dependencies import get_user_service


class ServiceException(Exception):
    """Исключение для сервисов."""

    pass


def register_middlewares(dp: Dispatcher):
    """Регистрация всех middleware."""
    dp.update.outer_middleware(ServicesMiddleware())


class ServicesMiddleware:
    """Middleware для внедрения сервисов в хендлеры."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Добавляем сервисы в data
        data["user_service"] = get_user_service()
        data["category_service"] = get_category_service()
        data["position_service"] = get_position_service()
        data["order_service"] = get_order_service()

        return await handler(event, data)
