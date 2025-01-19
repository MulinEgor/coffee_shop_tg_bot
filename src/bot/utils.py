from src.core.order.schemas import OrderGetSchema
from src.core.order.models import Status, ObtainingMethod
from src.bot.cart import Cart


def format_cart_text(cart: Cart) -> str:
    """Форматирование текста корзины."""
    if cart.is_empty:
        return "Корзина пуста"
    
    text = "🛒 Корзина:\n\n"
    for item in cart.items.values():
        text += f"• {item.position.name} ({item.weight}г) x{item.quantity} - {item.total_price}₽\n"
    text += f"\nИтого: {cart.total_price}₽"
    return text


def format_order_text(order: OrderGetSchema) -> str:
    """Форматирование текста заказа."""
    status_emoji = {
        Status.PROCESSING: "⏳",
        Status.COMPLETED: "✅",
        Status.CANCELLED: "❌"
    }
    
    obtaining_method_text = {
        ObtainingMethod.TAKEAWAY: "С собой",
        ObtainingMethod.INPLACE: "На месте",
        ObtainingMethod.DELIVERY: "Доставка"
    }
    
    text = f"Заказ #{order.id}\n"
    text += f"Статус: {status_emoji[order.status]} {order.status.value}\n"
    text += f"Способ получения: {obtaining_method_text[order.obtaining_method]}\n\n"
        
    for position in order.order_positions:
        total_price = int((position.weight / 100) * position.position.price) * position.quantity
        text += f"• {position.position.name} ({position.weight}г) x{position.quantity} - {total_price}₽\n"
    
    text += f"\nИтого: {order.total_price}₽"
    return text 
