from enum import Enum

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    role: Mapped[Role] = mapped_column(SQLAlchemyEnum(Role), nullable=False)
    orders: Mapped[list["Order"]] = (
        relationship(  # Строковой литерал в целях измбегания рекурсии в импортах
            back_populates="user", cascade="all, delete-orphan"
        )
    )
