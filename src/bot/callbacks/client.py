from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from fastapi import HTTPException

from src.core.user.service import UserService
from src.core.user.models import Role
from src.core.user.schemas import UserUpdateSchema
from src.core.position.schemas import PositionUpdateSchema
from src.core.category.service import CategoryService
from src.core.position.service import PositionService
from src.core.order.service import OrderService
from src.core.order.schemas import OrderCreateSchema
from src.core.order.models import ObtainingMethod
from src.bot.keyboards import (
    get_categories_keyboard,
    get_positions_keyboard,
    get_quantity_keyboard,
    get_cart_keyboard,
    get_obtaining_method_keyboard
)
from src.bot.states import OrderStates
from src.bot.cart import get_cart
from src.bot.utils import format_cart_text


router = Router()


@router.callback_query(OrderStates.selecting_category, F.data.startswith("category:"))
async def category_callback(callback: CallbackQuery, state: FSMContext, position_service: PositionService):
    """Обработчик выбора категории."""
    category_id = int(callback.data.split(":")[1])
    
    await state.update_data(category_id=category_id)
    
    try:
        positions = await position_service.get_all(filters=PositionUpdateSchema(category_id=category_id))
    except HTTPException:
        await callback.message.answer(
            "Отсутствуют позиции в этой категории.\n"
            "Свяжитесь с администратором"
        )
        return
    
    await state.set_state(OrderStates.selecting_position)
    await callback.message.edit_text(
        "Выберите позицию:",
        reply_markup=get_positions_keyboard(positions, category_id)
    )


@router.callback_query(OrderStates.selecting_position, F.data.startswith("position:"))
async def position_callback(callback: CallbackQuery, state: FSMContext, position_service: PositionService):
    """Обработчик выбора позиции."""
    position_id = int(callback.data.split(":")[1])
    try:
        position = await position_service.get(position_id)
    except HTTPException:
        await callback.message.answer(
            "Отсутствует позиция с таким ID."
        )
        return
    
    await state.update_data(position=position)
    await state.set_state(OrderStates.selecting_quantity)
    await callback.message.edit_text(
        f"Выберите количество для {position.name}:",
        reply_markup=get_quantity_keyboard(position_id)
    )


@router.callback_query(OrderStates.selecting_quantity, F.data.startswith("quantity:"))
async def quantity_callback(callback: CallbackQuery, state: FSMContext, category_service: CategoryService):
    """Обработчик выбора количества."""
    position_id = int(callback.data.split(":")[1])
    quantity = int(callback.data.split(":")[2])
    
    data = await state.get_data()
    position = data["position"]
    
    cart = get_cart(callback.from_user.id)
    cart.add_item(position, quantity)
    
    await callback.message.edit_text(
        f"{position.name} x {quantity} добавлено в корзину",
        reply_markup=get_categories_keyboard(await category_service.get_all())
    )
    await state.set_state(OrderStates.selecting_category)


@router.callback_query(F.data == "cart")
async def cart_callback(callback: CallbackQuery, state: FSMContext):
    """Обработчик просмотра корзины."""
    cart = get_cart(callback.from_user.id)
    await callback.message.edit_text(
        format_cart_text(cart),
        reply_markup=get_cart_keyboard()
    )


@router.callback_query(F.data == "clear_cart")
async def clear_cart_callback(callback: CallbackQuery, state: FSMContext, category_service: CategoryService):
    """Обработчик очистки корзины."""
    cart = get_cart(callback.from_user.id)
    cart.clear()
    
    try:
        categories = await category_service.get_all()
    except HTTPException:
        await callback.message.answer(
            "Отсутствуют категории товаров.\n"
            "Свяжитесь с администратором"
        )
        return
    
    await state.set_state(OrderStates.selecting_category)
    await callback.message.edit_text(
        "Корзина очищена",
        reply_markup=get_categories_keyboard(categories)
    )


@router.callback_query(F.data == "checkout")
async def checkout_callback(callback: CallbackQuery, state: FSMContext):
    """Обработчик оформления заказа."""
    cart = get_cart(callback.from_user.id)
    if cart.is_empty:
        await callback.answer("Корзина пуста")
        return
    
    await state.set_state(OrderStates.selecting_obtaining_method)
    await callback.message.edit_text(
        "Выберите способ получения заказа:",
        reply_markup=get_obtaining_method_keyboard()
    )


@router.callback_query(
    OrderStates.selecting_obtaining_method,
    F.data.startswith("obtaining_method:")
)
async def obtaining_method_callback(callback: CallbackQuery, state: FSMContext, order_service: OrderService, user_service: UserService):
    """Обработчик выбора способа получения."""
    obtaining_method = ObtainingMethod(callback.data.split(":")[1])
    
    cart = get_cart(callback.from_user.id)
    try:
        order = await order_service.create(OrderCreateSchema(
            user_id=callback.from_user.id,
            obtaining_method=obtaining_method,
            order_positions=[
                {"position_id": item.position.id, "quantity": item.quantity}
                    for item in cart.items.values()
            ]
        ))
    except HTTPException as e:
        await callback.message.answer(
            f"Произошла ошибка при создании заказа: {e.detail}"
        )
        return
    
    cart.clear()
    await state.clear()
    await callback.message.edit_text(
        f"Заказ #{order.id} успешно создан!\n"
        "Используйте /menu чтобы сделать новый заказ"
    )
    
    # Отправляем сообщение всем баристам
    bot = callback.bot
    try:
        for barista in await user_service.get_all(filters=UserUpdateSchema(role=Role.BARISTA)):
            await bot.send_message(
                barista.id,
                    f"Появился новый заказ #{order.id}!"
                )
    except HTTPException: # Если баристы не найдены, ничего не делаем
        pass

@router.callback_query(F.data == "categories")
async def back_to_categories_callback(callback: CallbackQuery, state: FSMContext, category_service: CategoryService):
    """Обработчик возврата к категориям."""
    try:
        categories = await category_service.get_all()
    except HTTPException:
        await callback.message.answer(
            "Отсутствуют категории товаров.\n"
            "Свяжитесь с администратором"
        )
        return
    
    await state.set_state(OrderStates.selecting_category)
    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=get_categories_keyboard(categories)
    )


@router.callback_query(F.data == "back_to_positions")
async def back_to_positions_callback(callback: CallbackQuery, state: FSMContext, position_service: PositionService, category_service: CategoryService):
    """Обработчик возврата к позициям."""
    data = await state.get_data()
    category_id = data.get("category_id")
    if not category_id:
        # Если категория не сохранена, возвращаемся к выбору категории
        await back_to_categories_callback(callback, state, category_service)
        return
    
    try:
        positions = await position_service.get_all(filters=PositionUpdateSchema(category_id=category_id))
    except HTTPException:
        await callback.message.answer(
            "Отсутствуют позиции в этой категории.\n"
            "Свяжитесь с администратором"
        )
        return
    
    await state.set_state(OrderStates.selecting_position)
    await callback.message.edit_text(
        "Выберите позицию:",
        reply_markup=get_positions_keyboard(positions, category_id)
    ) 
    