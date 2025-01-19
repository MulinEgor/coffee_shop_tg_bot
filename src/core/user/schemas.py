from typing import Optional

from pydantic import BaseModel

from src.core.order.schemas import OrderGetSchema
from src.core.user.models import Role


class UserCreateSchema(BaseModel):
    """
    Pydantic схема для создания пользователя.
    """

    id: int
    role: Role


class UserUpdateSchema(BaseModel):
    """
    Pydantic схема для обновления пользователя. Все поля необязательные.
    """

    role: Optional[Role] = None


class UserGetSchema(UserCreateSchema):
    """
    Pydantic схема для получения пользователя.
    """

    orders: list[OrderGetSchema]
