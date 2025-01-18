from sqlalchemy import select

from src.core.category.models import Category
from src.core.category.schemas import CategoryCreateSchema
from src.core.db import get_db_session
from src.core.repository import Repository


class CategoryRepository(Repository[Category, CategoryCreateSchema, None]):
    """
    Репозиторий для категорий. 
    """
    
    def __init__(self):
        super().__init__(Category)
    
    async def get_by_name(self, name: str, include_related: bool) -> Category:
        """
        Получение категории по названию.
        
        Аргументы:
            name: Название категории
            include_related: Загружать ли связанные объекты
        """
        async with get_db_session() as session:
            stmt = select(Category).where(Category.name == name)
            if include_related:
                stmt = self._include_related(stmt)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
