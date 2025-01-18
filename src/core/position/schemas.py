from typing import Optional
from pydantic import BaseModel

from src.core.category.schemas import CategoryGetSchema
from src.core.schemas import OptionalSchemaMeta


class PositionBaseSchema(BaseModel):
    """
    Базовая схема для позиции.
    """
    name: str
    gramms_weight: int
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
    category: Optional[CategoryGetSchema] = None # Обьект являеться опциональным, потому что может быть не нужен


class PositionUpdateSchema(PositionCreateSchema, metaclass=OptionalSchemaMeta):
    """
    Pydantic схема для обновления позиции.
    """
    id: int
