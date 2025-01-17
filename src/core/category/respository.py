from sqlalchemy import select

from src.core.category.models import Category
from src.core.category.schemas import CategorySchema
from src.core.db import get_db_session
from src.core.repository import Repository


class CategoryRepository(Repository[Category, CategorySchema, None]):
    """
    Репозиторий для категорий. 
    """
    
    def __init__(self):
        super().__init__(Category)
    
    async def get_by_name(self, name: str) -> Category:
        """
        Получение категории по названию.
        """
        async with get_db_session() as session:
            result = await session.execute(select(Category).where(Category.name == name))
            return result.scalar_one_or_none()
