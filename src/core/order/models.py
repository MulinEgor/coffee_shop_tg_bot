from datetime import datetime
from typing import List
from enum import Enum 
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.core.position.models import Position
from src.core.models import Base


class Status(str, Enum):
    """
    Статус заказа.
    """
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    
    
class ObtainingMethod(str, Enum):
    """
    Способ получения заказа.
    """
    TAKEAWAY = "takeaway" # С собой
    INPLACE = "inplace" # Здесь
    DELIVERY = "delivery" # Доставка
    
    
class OrderPosition(Base):
    """
    Промежуточная sqlalchemy модель для связи заказа и позиций с указанием количества
    """
    __tablename__ = "order_positions"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    
    position: Mapped["Position"] = relationship(back_populates="order_positions")
    order: Mapped["Order"] = relationship(back_populates="order_positions")


class Order(Base):
    """
    Sqlalchemy модель заказа.
    """
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    status: Mapped[Status] = mapped_column(
        SQLAlchemyEnum(Status),
        nullable=False,
        default=Status.PROCESSING
    )
    obtaining_method: Mapped[ObtainingMethod] = mapped_column(
        SQLAlchemyEnum(ObtainingMethod),
        nullable=False,
        default=ObtainingMethod.INPLACE
    )
    order_positions: Mapped[List[OrderPosition]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    @hybrid_property
    def price_sum(self) -> int:
        """Вычисляет общую сумму заказа."""
        return sum(order_position.position.price * order_position.quantity for order_position in self.order_positions)
    