from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.core.user.service import UserService
from src.core.user.models import Role
from src.core.order.service import OrderService
from src.core.order.schemas import OrderUpdateSchema
from src.core.order.models import Status
from src.bot.utils import format_order_text


router = Router()


@router.callback_query(F.data.startswith("status:"))
async def status_callback(
    callback: CallbackQuery,
    user_service: UserService,
    order_service: OrderService
):
    """Обработчик изменения статуса заказа."""
    user = await user_service.get(callback.from_user.id, False)
    if not user or user.role != Role.BARISTA:
        await callback.answer("У вас нет доступа к этой команде")
        return
    
    _, order_id, status = callback.data.split(":")
    order_id = int(order_id)
    
    order = await order_service.update(
        order_id,
        OrderUpdateSchema(status=Status(status))
    )
    
    bot = callback.bot
    await bot.send_message(
        order.user_id,
        f"Статус вашего заказа #{order.id} изменен на: {status}"
    )
    
    await callback.message.edit_text(
        format_order_text(order)
    ) 