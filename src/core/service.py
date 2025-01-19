import logging
from abc import abstractmethod
from typing import Generic

from src.core.repository import RepositoryType
from src.core.types import CreateSchemaType, GetSchemaType, ModelType, UpdateSchemaType, ServiceException


class Service(
    Generic[
        ModelType, 
        CreateSchemaType, 
        GetSchemaType, 
        UpdateSchemaType, 
        RepositoryType, 
    ]
):
    """E
    Базовый класс для сервиса.
    """

    _logger: logging.Logger

    def __init__(
        self,
        repository: RepositoryType,
        exception: Exception,
    ):
        """
        Аргументы:
            repository: Репозиторий, который будет использовать сервис
            exception: Исключение, которое будет использовать сервис
        """
        self._repository = repository
        self._exception = exception

    async def get(self, id: int, include_related: bool = True) -> GetSchemaType:
        """
        Получение объекта по ID.

        Аргументы:
            id: ID объекта
            include_related: Загружать ли связанные объекты
        """
        self._logger.info(f"Получение объекта с id: {id}")
        data: ModelType = await self._repository.get(id, include_related)
        if not data:
            self._handle_error(f"Объект с id: {id} не найден", status_code=404)
        self._logger.info(f"Объект с id: {id} успешно получен")

        return self._convert_to_schema(data)

    async def get_all(
        self, filters: UpdateSchemaType | None = None, include_related: bool = True
    ) -> list[GetSchemaType]:
        """
        Получение всех объектов.

        Аргументы:
            filters: Фильтры для поиска
            include_related: Загружать ли связанные объекты
        """
        self._logger.info(
            f"Получение всех объектов с фильтрами: {filters.model_dump(exclude_unset=True) if filters else 'None'}"
        )
        data = await self._repository.get_all(include_related, filters)
        if not data:
            self._handle_error("Объекты не найдены", status_code=404)
        self._logger.info(f"Успешно получено {len(data)} объектов")

        return [self._convert_to_schema(obj) for obj in data]

    async def create(
        self, data: CreateSchemaType, include_related: bool = True
    ) -> GetSchemaType:
        """
        Создание объекта.

        Аргументы:
            data: Данные для создания объекта
            include_related: Загружать ли связанные объекты
        """
        self._logger.info(f"Создание объекта: {data.model_dump(exclude_unset=True)}")
        obj: ModelType = await self._repository.create(data, include_related)
        if not obj:
            self._handle_error("Не удалось создать объект", status_code=400)
        self._logger.info(f"Объект успешно создан с id: {obj.id}")

        return self._convert_to_schema(obj)

    async def update(
        self, id: int, data: UpdateSchemaType, include_related: bool = True
    ) -> GetSchemaType:
        """
        Обновление объекта.

        Аргументы:
            id: ID объекта
            data: Данные для обновления объекта
            include_related: Загружать ли связанные объекты
        """
        self._logger.info(
            f"Обновление объекта с id: {id} и данными: {data.model_dump(exclude_unset=True)}"
        )
        await self.get(id)

        obj: ModelType = await self._repository.update(id, data, include_related)
        if not obj:
            self._handle_error(
                f"Не удалось обновить объект с id: {id}", status_code=400
            )
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
            self._handle_error(f"Не удалось удалить объект с id: {id}", status_code=400)
        self._logger.info(f"Объект с id: {id} успешно удален")

        return True

    def _handle_error(self, message: str = None, status_code: int = 400):
        """
        Вспомогающий метод для обработки ошибок.

        Аргументы:
            message: Сообщение об ошибке
            status_code: Код статуса HTTP
        """
        self._logger.error(message)
        if issubclass(self._exception, ServiceException):
            raise self._exception(message)
        else:
            raise self._exception(status_code=status_code, detail=message)

    @abstractmethod
    def _convert_to_schema(self, obj: ModelType) -> GetSchemaType:
        """
        Преобразует модель в схему.
        Этот метод должен быть переопределен в дочерних классах.

        Аргументы:
            obj: Модель для преобразования
        """
        raise NotImplementedError
