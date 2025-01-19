from src.core.category.models import Category
from src.core.position.models import Position

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


async def seed_data(connection):
    """Заполнение базы данных начальными данными."""
    # Создание категорий
    for category_data in categories_data:
        await connection.execute(Category.__table__.insert().values(category_data))

    # Получение созданных категорий
    result = await connection.execute(Category.__table__.select())
    categories = {category.name: category.id for category in result.fetchall()}

    # Создание позиций
    for position_data in positions_data:
        category_name = position_data.pop("category_name")
        position_data["category_id"] = categories[category_name]
        await connection.execute(Position.__table__.insert().values(position_data))
