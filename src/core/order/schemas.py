from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.core.schemas import OptionalSchemaMeta
from src.core.position.schemas import PositionGetSchema
from src.core.order.models import ObtainingMethod, Status

    
class OrderPositionCreateSchema(BaseModel):
    """
    Pydantic схема для создания позиции в заказе.
    """
    position_id: int
    quantity: int
    
    
class OrderPositionGetSchema(OrderPositionCreateSchema):
    """
    Pydantic схема для получения позиции в заказе.
    """
    position: Optional[PositionGetSchema] = None
    

class OrderCreateSchema(BaseModel):
    """
    Pydantic схема для создания заказа.
    """ 
    user_id: int
    order_positions: list[OrderPositionCreateSchema]
    obtaining_method: ObtainingMethod
    
    
class OrderUpdateSchema(OrderCreateSchema, metaclass=OptionalSchemaMeta):
    """
    Pydantic схема для обновления заказа.
    """
    date: datetime
    status: Status
    

class OrderGetSchema(OrderCreateSchema):
    """
    Pydantic схема для получения заказа.
    """
    id: int
    date: datetime
    status: Status
    price_sum: int | None
    order_positions: list[OrderPositionGetSchema]
