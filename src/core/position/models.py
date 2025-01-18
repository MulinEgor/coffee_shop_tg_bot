from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.category.models import Category
from src.core.models import Base


class Position(Base):
    """
    Sqlalchemy модель позиции.
    """
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[Category] = relationship(back_populates="positions")
    gramms_weight: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    order_positions: Mapped[list["OrderPosition"]] = relationship( # type: ignore
        back_populates="position",
        cascade="all, delete-orphan"
    )
