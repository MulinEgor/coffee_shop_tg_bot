from typing import Optional

from pydantic import BaseModel

from src.core.category.schemas import CategoryGetSchema


class PositionBaseSchema(BaseModel):
    """
    Базовая pydantic схема для позиции.
    """

    name: str
    price: int


class PositionCreateSchema(PositionBaseSchema):
    """
    Pydantic схема для создания позиции.
    """

    category_id: int


class PositionGetSchema(PositionBaseSchema):
    """
    Pydantic схема для получения позиции.
    """

    id: int
    category: Optional[CategoryGetSchema] = None


class PositionUpdateSchema(BaseModel):
    """
    Pydantic схема для обновления позиции. Все поля необязательные.
    """

    category_id: Optional[int] = None
    name: Optional[str] = None
    gramms_weight: Optional[int] = None
    price: Optional[int] = None
