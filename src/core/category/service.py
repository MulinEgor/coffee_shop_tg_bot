from src.core.category.models import Category
from src.core.category.respository import CategoryRepository
from src.core.category.schemas import CategoryCreateSchema, CategoryGetSchema
from src.core.service import Service


class CategoryService(Service[Category, CategoryCreateSchema, CategoryGetSchema, None, CategoryRepository]):
    """
    Сервис для категорий.
    """
    async def create(self, data: CategoryCreateSchema, include_related: bool = True) -> CategoryGetSchema:
        """
        Создание объекта. Проверяет наличие категории с таким названием.
        
        Аргументы:
            data: Данные для создания объекта
            include_related: Загружать ли связанные объекты
        """
        if await self._repository.get_by_name(data.name, False):
            self._handle_error("Категория с таким названием уже существует")
        
        self._logger.info(f"Создание объекта: {data.model_dump(exclude_unset=True)}")
        obj = await self._repository.create(data, include_related)
        if not obj:
            self._handle_error("Не удалось создать объект")
        self._logger.info(f"Объект успешно создан с id: {obj.id}")
        
        return self._convert_to_schema(obj)
    
    def _convert_to_schema(self, obj: Category) -> CategoryGetSchema:
        """
        Преобразование модели в схему.
        
        Аргументы:
            obj: Модель для преобразования
        """ 
        return CategoryGetSchema(
            id=obj.id,
            name=obj.name,
        )
