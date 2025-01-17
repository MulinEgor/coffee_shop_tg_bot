from typing import Generic

from src.core.repository import RepositoryType
from src.core.types import CreateSchemaType, ModelType, UpdateSchemaType
from src.core.logger import get_logger


class Service(Generic[ModelType, CreateSchemaType, UpdateSchemaType, RepositoryType]):
    """
    Базовый класс для сервиса.
    """
    def __init__(self, name: str, repository: RepositoryType):
        self._logger = get_logger(name)
        self._repository = repository

    async def get(self, id: int) -> ModelType:
        """
        Получение объекта по ID.
        """
        self._logger.info(f"Получение объекта с id: {id}")
        data = await self._repository.get(id)
        if not data:
            self._handle_error(f"Объект с id: {id} не найден")
        self._logger.info(f"Объект с id: {id} успешно получен")
        
        return data

    async def get_all(self, filters: UpdateSchemaType | None = None) -> list[ModelType]:
        """
        Получение всех объектов с необязательными фильтрами.
        """
        self._logger.info(f"Получение всех объектов с фильтрами: {filters.model_dump(exclude_unset=True) if filters else 'None'}")
        data = await self._repository.get_all(filters)
        if not data:
            self._handle_error("Объекты не найдены")
        self._logger.info(f"Успешно получено {len(data)} объектов")
        
        return data

    async def create(self, data: CreateSchemaType) -> ModelType:
        """
        Создание объекта.
        """
        self._logger.info(f"Создание объекта: {data.model_dump(exclude_unset=True)}")
        obj = await self._repository.create(data)
        if not obj:
            self._handle_error("Не удалось создать объект")
        self._logger.info(f"Объект успешно создан с uuid: {obj.uuid}")
        
        return obj

    async def update(self, id: int, data: UpdateSchemaType) -> ModelType:
        """
        Обновление объекта.
        """
        self._logger.info(f"Обновление объекта с id: {id} и данными: {data.model_dump(exclude_unset=True)}")
        await self.get(id)

        obj = await self._repository.update(id, data)
        if not obj:
            self._handle_error(f"Не удалось обновить объект с id: {id}")
        self._logger.info(f"Объект с id: {id} успешно обновлен")
        
        return obj

    async def delete(self, id: int) -> ModelType:
        """
        Удаление объекта.
        """
        self._logger.info(f"Удаление объекта с id: {id}")
        await self.get(id)

        obj = await self._repository.delete(id)
        if not obj:
            self._handle_error(f"Не удалось удалить объект с id: {id}")
        self._logger.info(f"Объект с id: {id} успешно удален")
        
        return obj

    def _handle_error(self, message: str):
        """
        Вспомогающий метод для обработки ошибок.
        """
        self._logger.error(message)
        raise Exception(message)
    