from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core.order.models import ObtainingMethod, Status
from src.core.user.models import Role


def get_role_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора роли."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Бариста", callback_data=f"role:{Role.BARISTA.value}"
        ),
        InlineKeyboardButton(text="Клиент", callback_data=f"role:{Role.CLIENT.value}"),
    )
    return builder.as_markup()


def get_categories_keyboard(categories: list) -> InlineKeyboardMarkup:
    """Клавиатура выбора категории."""
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.add(
            InlineKeyboardButton(
                text=category.name, callback_data=f"category:{category.id}"
            )
        )
    builder.add(InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"))

    builder.adjust(2)
    return builder.as_markup()


def get_positions_keyboard(positions: list, category_id: int) -> InlineKeyboardMarkup:
    """Клавиатура выбора позиции."""
    builder = InlineKeyboardBuilder()
    for position in positions:
        builder.add(
            InlineKeyboardButton(
                text=f"{position.name} - {position.price}₽",
                callback_data=f"position:{position.id}",
            )
        )
    builder.add(
        InlineKeyboardButton(text="◀️ Назад", callback_data="categories"),
        InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"),
    )
    builder.adjust(2)
    return builder.as_markup()


def get_quantity_keyboard(position_id: int) -> InlineKeyboardMarkup:
    """Клавиатура выбора количества."""
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.add(
            InlineKeyboardButton(
                text=str(i), callback_data=f"quantity:{position_id}:{i}"
            )
        )
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_positions"))
    builder.adjust(5, 1)
    return builder.as_markup()


def get_cart_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура корзины."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🗑 Очистить", callback_data="clear_cart"),
        InlineKeyboardButton(text="✅ Оформить", callback_data="checkout"),
        InlineKeyboardButton(text="◀️ К меню", callback_data="categories"),
    )
    builder.adjust(2)
    return builder.as_markup()


def get_obtaining_method_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора способа получения."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="С собой",
            callback_data=f"obtaining_method:{ObtainingMethod.TAKEAWAY.value}",
        ),
        InlineKeyboardButton(
            text="На месте",
            callback_data=f"obtaining_method:{ObtainingMethod.INPLACE.value}",
        ),
        InlineKeyboardButton(
            text="Доставка",
            callback_data=f"obtaining_method:{ObtainingMethod.DELIVERY.value}",
        ),
        InlineKeyboardButton(text="◀️ Назад", callback_data="cart"),
    )
    builder.adjust(2)
    return builder.as_markup()


def get_order_status_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Клавиатура изменения статуса заказа."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="✅ Готов", callback_data=f"status:{order_id}:{Status.COMPLETED.value}"
        ),
        InlineKeyboardButton(
            text="❌ Отменён",
            callback_data=f"status:{order_id}:{Status.CANCELLED.value}",
        ),
    )
    return builder.as_markup()


def get_weight_keyboard(position_id: int) -> InlineKeyboardMarkup:
    """Клавиатура выбора веса."""
    builder = InlineKeyboardBuilder()
    weights = [100, 200, 300, 400, 500]  # Доступные варианты веса
    for weight in weights:
        builder.add(
            InlineKeyboardButton(
                text=f"{weight}г", callback_data=f"weight:{position_id}:{weight}"
            )
        )
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_positions"))
    builder.adjust(3, 2, 1)
    return builder.as_markup()
