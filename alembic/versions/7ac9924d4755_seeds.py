"""seeds

Revision ID: 7ac9924d4755
Revises: c6729e9838e3
Create Date: 2025-01-19 20:27:24.449777

"""

from typing import Sequence, Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.category.models import Category
from src.core.position.models import Position
from src.core.settings import settings

# revision identifiers, used by Alembic.
revision: str = "7ac9924d4755"
down_revision: Union[str, None] = "c6729e9838e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Начальные данные для категорий
categories_data = [{"name": "Кофе"}, {"name": "Чай"}, {"name": "Десерты"}]

# Начальные данные для позиций
positions_data = [
    # Кофе
    {"name": "Американо", "category_name": "Кофе", "price": 150},
    {"name": "Капучино", "category_name": "Кофе", "price": 200},
    {"name": "Латте", "category_name": "Кофе", "price": 200},
    # Чай
    {"name": "Зеленый чай", "category_name": "Чай", "price": 100},
    {"name": "Черный чай", "category_name": "Чай", "price": 100},
    # Десерты
    {"name": "Чизкейк", "category_name": "Десерты", "price": 250},
    {"name": "Тирамису", "category_name": "Десерты", "price": 300},
]


def seed_data(connection):
    """Заполнение базы данных начальными данными."""
    # Создание категорий
    for category_data in categories_data:
        connection.execute(Category.__table__.insert().values(category_data))

    # Получение созданных категорий
    result = connection.execute(Category.__table__.select())
    categories = {category.name: category.id for category in result.fetchall()}

    # Создание позиций
    for position_data in positions_data:
        category_name = position_data.pop("category_name")
        position_data["category_id"] = categories[category_name]
        connection.execute(Position.__table__.insert().values(position_data))


def upgrade() -> None:
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        seed_data(session)
        session.commit()


def downgrade() -> None:
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        session.execute("DELETE FROM categories")
        session.execute("DELETE FROM positions")
        session.commit()
