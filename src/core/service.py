from abc import abstractmethod
from typing import Generic

from src.core.repository import RepositoryType
from src.core.types import CreateSchemaType, GetSchemaType, ModelType, UpdateSchemaType
from src.core.logger import get_logger


class Service(Generic[ModelType, CreateSchemaType, GetSchemaType, UpdateSchemaType, RepositoryType]):
    """
    Базовый класс для сервиса.
    """
    def __init__(self, name: str, repository: RepositoryType):
        """
        Аргументы:
            name: Название сервиса
            repository: Репозиторий, который будет использовать сервис
        """
        self._logger = get_logger(name)
        self._repository = repository

    async def get(self, id: int) -> GetSchemaType:
        """
        Получение объекта по ID.
        
        Аргументы:
            id: ID объекта
        """
        self._logger.info(f"Получение объекта с id: {id}")
        data: ModelType = await self._repository.get(id)
        if not data:
            self._handle_error(f"Объект с id: {id} не найден")
        self._logger.info(f"Объект с id: {id} успешно получен")
        
        return self._convert_to_schema(data)

    async def get_all(self, filters: UpdateSchemaType | None = None) -> list[GetSchemaType]:
        """
        Получение всех объектов.
        
        Аргументы:
            filters: Фильтры для поиска
        """
        self._logger.info(f"Получение всех объектов с фильтрами: {filters.model_dump(exclude_unset=True) if filters else 'None'}")
        data = await self._repository.get_all(filters)
        if not data:
            self._handle_error("Объекты не найдены")
        self._logger.info(f"Успешно получено {len(data)} объектов")
        
        return [self._convert_to_schema(obj) for obj in data]

    async def create(self, data: CreateSchemaType) -> GetSchemaType:
        """
        Создание объекта.
        
        Аргументы:
            data: Данные для создания объекта
        """
        self._logger.info(f"Создание объекта: {data.model_dump(exclude_unset=True)}")
        obj: ModelType = await self._repository.create(data)
        if not obj:
            self._handle_error("Не удалось создать объект")
        self._logger.info(f"Объект успешно создан с uuid: {obj.uuid}")
        
        return self._convert_to_schema(obj)

    async def update(self, id: int, data: UpdateSchemaType) -> GetSchemaType:
        """
        Обновление объекта.
        
        Аргументы:
            id: ID объекта
            data: Данные для обновления объекта
        """
        self._logger.info(f"Обновление объекта с id: {id} и данными: {data.model_dump(exclude_unset=True)}")
        await self.get(id)

        obj: ModelType = await self._repository.update(id, data)
        if not obj:
            self._handle_error(f"Не удалось обновить объект с id: {id}")
        self._logger.info(f"Объект с id: {id} успешно обновлен")
        
        return self._convert_to_schema(obj)

    async def delete(self, id: int) -> bool:
        """
        Удаление объекта.
        
        Аргументы:
            id: ID объекта
        """
        self._logger.info(f"Удаление объекта с id: {id}")
        await self.get(id)

        if not await self._repository.delete(id):
            self._handle_error(f"Не удалось удалить объект с id: {id}")
        self._logger.info(f"Объект с id: {id} успешно удален")
        
        return True

    def _handle_error(self, message: str):
        """
        Вспомогающий метод для обработки ошибок.
        
        Аргументы:
            message: Сообщение об ошибке
        """
        self._logger.error(message)
        raise Exception(message)

    @abstractmethod
    def _convert_to_schema(self, obj: ModelType) -> GetSchemaType:
        """
        Преобразует модель в схему.
        Этот метод должен быть переопределен в дочерних классах.
        
        Аргументы:
            obj: Модель для преобразования
        """
        raise NotImplementedError