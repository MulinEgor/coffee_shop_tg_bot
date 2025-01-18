from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

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
    user = await user_service.get(message.from_user.id, False)
    if not user or user.role != Role.BARISTA:
        await message.answer("У вас нет доступа к этой команде")
        return
    
    orders = await order_service.get_all()
    active_orders = [
        order for order in orders 
        if order.status == Status.PROCESSING
    ]
    
    if not active_orders:
        await message.answer("Активных заказов нет")
        return
    
    for order in active_orders:
        await message.answer(
            format_order_text(order),
            reply_markup=get_order_status_keyboard(order.id)
        ) 