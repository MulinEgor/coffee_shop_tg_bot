from src.core.category.models import Category
from src.core.category.respository import CategoryRepository
from src.core.category.schemas import CategorySchema
from src.core.service import Service


class CategoryService(Service[Category, CategorySchema, None, CategoryRepository]):
    """
    Сервис для категорий.
    """
    async def create(self, data: CategorySchema) -> Category:
        """
        Создание объекта. Проверяет наличие категории с таким названием.
        """
        if await self._repository.get_by_name(data.name):
            self._handle_error("Категория с таким названием уже существует")
        
        self._logger.info(f"Создание объекта: {data.model_dump(exclude_unset=True)}")
        obj = await self._repository.create(data)
        if not obj:
            self._handle_error("Не удалось создать объект")
        self._logger.info(f"Объект успешно создан с id: {obj.id}")
        
        return obj
    