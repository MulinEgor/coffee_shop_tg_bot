from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

from src.core.order.models import Order
from src.core.models import Base


class Role(Enum):
    BARISTA = "barista"
    CLIENT = "client"


class User(Base):
    """
    Sqlalchemy модель пользователя.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role :Mapped[Role] = mapped_column(SQLAlchemyEnum(Role), nullable=False)
    orders: Mapped[list[Order]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    