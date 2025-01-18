from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from src.core.position.models import Position
from src.core.order.models import Order, OrderPosition
from src.core.order.respository import OrderRepository
from src.core.user.models import User
from src.core.user.schemas import UserCreateSchema, UserUpdateSchema
from src.core.repository import Repository


class UserRepository(Repository[User, UserCreateSchema, UserUpdateSchema]):
    """
    Репозиторий для пользователей. 
    """
    
    def __init__(self):
        super().__init__(User)
    
    def _include_related(self, stmt: Select) -> Select:
        stmt = stmt.options(
            joinedload(User.orders).joinedload(Order.order_positions).joinedload(OrderPosition.position).joinedload(Position.category)
        )
        return stmt
