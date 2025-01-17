from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base


class Category(Base):
    """
    Sqlalchemy модель категории.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    positions: Mapped[list["Position"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan"
    )
    