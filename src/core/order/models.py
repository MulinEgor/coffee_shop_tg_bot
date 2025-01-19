from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.user.models import User


class Status(str, Enum):
    """
    Статус заказа.
    """

    PROCESSING = "Обрабатываеться"
    COMPLETED = "Готов"
    CANCELLED = "Отменен"


class ObtainingMethod(str, Enum):
    """
    Способ получения заказа.
    """

    TAKEAWAY = "Самовывоз"
    INPLACE = "На месте"
    DELIVERY = "Доставка"


class OrderPosition(Base):
    """
    Промежуточная sqlalchemy модель для связи заказа и позиций с указанием количества и веса
    """

    __tablename__ = "order_positions"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True
    )
    position_id: Mapped[int] = mapped_column(
        ForeignKey("positions.id", ondelete="CASCADE"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    weight: Mapped[int] = mapped_column(nullable=False)  # Вес в граммах

    position: Mapped["Position"] = relationship(
        back_populates="order_positions"
    )  # Строковой литерал в целях измбегания рекурсии в импортах
    order: Mapped["Order"] = relationship(
        back_populates="order_positions"
    )  # Строковой литерал в целях измбегания рекурсии в импортах

    @property
    def total_price(self) -> int:
        """Вычисляет общую стоимость позиции с учетом веса."""
        return int((self.weight / 100) * self.position.price) * self.quantity


class Order(Base):
    """
    Sqlalchemy модель заказа.
    """

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    status: Mapped[Status] = mapped_column(
        SQLAlchemyEnum(Status), nullable=False, default=Status.PROCESSING
    )
    obtaining_method: Mapped[ObtainingMethod] = mapped_column(
        SQLAlchemyEnum(ObtainingMethod), nullable=False, default=ObtainingMethod.INPLACE
    )
    order_positions: Mapped[List[OrderPosition]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="orders")

    @hybrid_property
    def total_price(self) -> int:
        """Вычисляет общую сумму заказа."""
        return sum(
            order_position.total_price for order_position in self.order_positions
        )
