import logging
from sqlalchemy.orm.exc import DetachedInstanceError

from src.core.logger import get_logger
from src.core.order.service import OrderService
from src.core.user.models import Role, User
from src.core.user.respository import UserRepository
from src.core.user.schemas import UserCreateSchema, UserGetSchema, UserUpdateSchema
from src.core.service import Service


class UserService(Service[User, UserCreateSchema, UserGetSchema, UserUpdateSchema, UserRepository]):
    """
    Сервис для пользователей.
    """
    _logger: logging.Logger = get_logger("UserService")
    
    def __init__(self, repository: UserRepository, order_service: OrderService):
        """
        Инициализация сервиса.
        
        Аргументы:
            repository: Репозиторий, который будет использовать сервис
            order_service: Сервис для заказов
        """
        super().__init__(repository)
        self._order_service = order_service
        
    async def create(self, data: UserCreateSchema, include_related: bool = True) -> UserGetSchema:
        """
        Создание объекта. Проверяет наличие пользователя с таким ID.
        
        Аргументы:
            data: Данные для создания объекта
            include_related: Загружать ли связанные объекты
        """
        if await self._repository.get(data.id, False):
            self._handle_error("Пользователь с таким ID уже существует", status_code=409)
        
        self._logger.info(f"Создание объекта: {data.model_dump(exclude_unset=True)}")
        obj: User = await self._repository.create(data, include_related)
        if not obj:
            self._handle_error("Не удалось создать объект", status_code=400)
        self._logger.info(f"Объект успешно создан с id: {obj.id}")
        
        return self._convert_to_schema(obj)
    
    async def update(self, id: int, data: UserUpdateSchema, include_related: bool = True) -> UserGetSchema:
        """
        Обновление объекта. Проверяет наличие пользователя с таким ID.
        
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
        
        if data.id and await self.get(data.id, False):
            self._handle_error("Пользователь с таким ID уже существует", status_code=409)

        obj: User = await self._repository.update(id, data, include_related)
        if not obj:
            self._handle_error(f"Не удалось обновить объект с id: {id}", status_code=400)
        self._logger.info(f"Объект с id: {id} успешно обновлен")
        
        return self._convert_to_schema(obj)
        

    def _convert_to_schema(self, obj: User) -> UserGetSchema:
        """
        Преобразование модели в схему.
        
        Аргументы:
            obj: Модель для преобразования
        """ 
        try:
            orders = [self._order_service._convert_to_schema(order) for order in obj.orders]
        except DetachedInstanceError as e: # Если объект не загружен, то возвращаем пустой список
            orders = []
        
        return UserGetSchema(
            id=obj.id,
            role=Role(obj.role),
            orders=orders,
        )
