from typing import Dict, List
from pydantic import BaseModel, Field

from src.core.position.schemas import PositionGetSchema
from src.core.order.schemas import OrderPositionCreateSchema


class CartItem(BaseModel):
    """Модель элемента корзины."""
    position: PositionGetSchema 
    quantity: int = Field(gt=0, default=1)
        
    @property
    def total_price(self) -> int:
        """Общая стоимость позиции."""
        return self.position.price * self.quantity
    
    def to_order_position(self) -> OrderPositionCreateSchema:
        """Конвертация в позицию заказа."""
        return OrderPositionCreateSchema(
            position_id=self.position.id,
            quantity=self.quantity
        )


class Cart(BaseModel):
    """Модель корзины."""
    items: Dict[int, CartItem] = Field(default_factory=dict)
    
    def add_item(self, position: PositionGetSchema, quantity: int = 1) -> None:
        """
        Добавление позиции в корзину.
        
        Аргументы:
            position: Позиция меню
            quantity: Количество
        """
        if position.id in self.items:
            current_item = self.items[position.id]
            new_quantity = current_item.quantity + quantity
            self.items[position.id] = CartItem(
                position=position,
                quantity=new_quantity
            )
        else:
            self.items[position.id] = CartItem(
                position=position,
                quantity=quantity
            )
    
    def remove_item(self, position_id: int) -> None:
        """
        Удаление позиции из корзины.
        
        Аргументы:
            position_id: ID позиции
        """
        self.items.pop(position_id, None)
    
    def clear(self) -> None:
        """Очистка корзины."""
        self.items.clear()
    
    @property
    def total_price(self) -> int:
        """Общая стоимость всех позиций в корзине."""
        return sum(item.total_price for item in self.items.values())
    
    @property
    def is_empty(self) -> bool:
        """Проверка на пустоту корзины."""
        return len(self.items) == 0
    
    def get_order_positions(self) -> List[OrderPositionCreateSchema]:
        """
        Получение позиций для создания заказа.
        """
        return [item.to_order_position() for item in self.items.values()]


# Хранилище корзин пользователей
user_carts: Dict[int, Cart] = {}


def get_cart(user_id: int) -> Cart:
    """
    Получение корзины пользователя.
    
    Аргументы:
        user_id: ID пользователя
    """
    if user_id not in user_carts:
        user_carts[user_id] = Cart()
    return user_carts[user_id] 