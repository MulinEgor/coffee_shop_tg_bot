from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fastapi import HTTPException

from src.core.order.schemas import OrderUpdateSchema
from src.core.user.service import UserService
from src.core.user.models import Role
from src.core.order.service import OrderService
from src.core.order.models import Status
from src.bot.keyboards import get_order_status_keyboard
from src.bot.utils import format_order_text


router = Router()


@router.message(Command("orders"))
async def orders_handler(message: Message, user_service: UserService, order_service: OrderService):
    """Обработчик команды /orders."""
    try:
        user = await user_service.get(message.from_user.id, False)
    except HTTPException:
        await message.answer(
            "Вы не зарегистрированы.\n"
            "Используйте /start для регистрации"
        )
        return
    
    if user.role != Role.BARISTA:
        await message.answer("У вас нет доступа к этой команде")
        return
    
    try:
        orders = await order_service.get_all(filters=OrderUpdateSchema(status=Status.PROCESSING))
    except HTTPException:
        await message.answer("Активных заказов нет")
        return
    
    for order in orders:
        await message.answer(
            format_order_text(order),
            reply_markup=get_order_status_keyboard(order.id)
        ) 