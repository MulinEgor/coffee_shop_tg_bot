from sqlalchemy.orm.exc import DetachedInstanceError

from src.core.category.schemas import CategoryGetSchema
from src.core.category.service import CategoryService
from src.core.position.models import Position
from src.core.position.respository import PositionRepository
from src.core.position.schemas import PositionCreateSchema, PositionGetSchema, PositionUpdateSchema
from src.core.service import Service


class PositionService(Service[Position, PositionCreateSchema, PositionGetSchema, PositionUpdateSchema, PositionRepository]):
    """
    Сервис для позиций.
    """
    
    def __init__(self, repository: PositionRepository, category_service: CategoryService):
        """
        Аргументы:
            repository: Репозиторий, который будет использовать сервис
            category_service: Сервис для категорий
        """
        super().__init__("PositionService", repository)
        self._category_service = category_service
        
    
    async def create(self, data: PositionCreateSchema, include_related: bool = True) -> PositionGetSchema:
        """
        Создание объекта. Проверяет наличие категории с таким ID и позиции с таким названием.
        
        Аргументы:
            data: Данные для создания объекта
            include_related: Загружать ли связанные объекты
        """
        if not await self._category_service.get(data.category_id, False):
            self._handle_error("Категория с таким ID не найдена", status_code=404)
        
        if await self._repository.get_by_name(data.name, False):
            self._handle_error("Позиция с таким названием уже существует", status_code=409)
        
        self._logger.info(f"Создание объекта: {data.model_dump(exclude_unset=True)}")
        obj: Position = await self._repository.create(data, include_related)
        if not obj:
            self._handle_error("Не удалось создать объект", status_code=400)
        self._logger.info(f"Объект успешно создан с id: {obj.id}")
        
        return self._convert_to_schema(obj)
    
    async def update(self, id: int, data: PositionUpdateSchema, include_related: bool = True) -> PositionGetSchema:
        """
        Обновление объекта. Проверяет наличие категории с таким ID и позиции с таким названием.
        
        Аргументы:
            id: ID объекта
            data: Данные для обновления объекта
            include_related: Загружать ли связанные объекты
        """
        self._logger.info(f"Обновление объекта с id: {id} и данными: {data.model_dump(exclude_unset=True)}")
        obj = await self.get(id, True)
        
        if len(list(data.model_dump(exclude_unset=True).keys())) == 0:
            self._logger.info(f"Объект с id: {id} не изменен")
            return self._convert_to_schema(obj)
        
        if data.category_id and not await self._category_service.get(data.category_id, False):
            self._handle_error("Категория с таким ID не найдена", status_code=404)
        
        if data.name and await self._repository.get_by_name(data.name, False):
            self._handle_error("Позиция с таким названием уже существует", status_code=409)

        obj: Position = await self._repository.update(id, data, include_related)
        if not obj:
            self._handle_error(f"Не удалось обновить объект с id: {id}", status_code=400)
        self._logger.info(f"Объект с id: {id} успешно обновлен")
        
        return self._convert_to_schema(obj)

    def _convert_to_schema(self, obj: Position) -> PositionGetSchema:
        """
        Преобразование модели в схему.
        
        Аргументы:
            obj: Модель для преобразования
        """
        try:
            category = self._category_service._convert_to_schema(obj.category)
        except DetachedInstanceError: # Если объект не загружен, то возвращаем None
            category = None
        
        return PositionGetSchema(
            id=obj.id,
            name=obj.name,
            gramms_weight=obj.gramms_weight,
            price=obj.price,
            category=category,
        )
