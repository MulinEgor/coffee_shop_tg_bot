from typing import Generic

from src.core.types import CreateSchemaType, ModelType, UpdateSchemaType
from src.core.logger import get_logger
from src.core.repository import Repository


class Service(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс для сервиса.
    """
    def __init__(self, name: str, repository: Repository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self._logger = get_logger(name)
        self._repository = repository

    async def get(self, uuid: str) -> ModelType:
        """
        Получение объекта по UUID.
        """
        self._logger.info(f"Получение объекта с uuid: {uuid}")
        data = await self._repository.get(uuid)
        if not data:
            self._handle_error(f"Объект с uuid: {uuid} не найден")
        self._logger.info(f"Объект с uuid: {uuid} успешно получен")
        
        return data

    async def get_all(self, filters: UpdateSchemaType | None = None) -> list[ModelType]:
        """
        Получение всех объектов с необязательными фильтрами.
        """
        self._logger.info(f"Получение всех объектов с фильтрами: \n{
            filters.model_dump(exclude_unset=True) if filters else 'None'}")
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

    async def update(self, uuid: str, data: UpdateSchemaType) -> ModelType:
        """
        Обновление объекта.
        """
        self._logger.info(f"Обновление объекта с uuid: {uuid} и данными: {data.model_dump(exclude_unset=True)}")
        await self.get(uuid)

        obj = await self._repository.update(uuid, data)
        if not obj:
            self._handle_error(f"Не удалось обновить объект с uuid: {uuid}")
        self._logger.info(f"Объект с uuid: {uuid} успешно обновлен")
        
        return obj

    async def delete(self, uuid: str) -> ModelType:
        """
        Удаление объекта.
        """
        self._logger.info(f"Удаление объекта с uuid: {uuid}")
        await self.get(uuid)

        obj = await self._repository.delete(uuid)
        if not obj:
            self._handle_error(f"Не удалось удалить объект с uuid: {uuid}")
        self._logger.info(f"Объект с uuid: {uuid} успешно удален")
        
        return obj

    def _handle_error(self, message: str):
        """
        Вспомогающий метод для обработки ошибок.
        """
        self._logger.error(message)
        raise Exception(message)
    