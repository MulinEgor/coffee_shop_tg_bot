import logging
from sqlalchemy.orm.exc import DetachedInstanceError

from src.core.logger import get_logger
from src.core.user.respository import UserRepository
from src.core.position.service import PositionService
from src.core.order.models import ObtainingMethod, Order, Status
from src.core.order.respository import OrderRepository
from src.core.order.schemas import OrderCreateSchema, OrderGetSchema, OrderPositionGetSchema, OrderUpdateSchema
from src.core.service import Service


class OrderService(Service[Order, OrderCreateSchema, OrderGetSchema, OrderUpdateSchema, OrderRepository]):
    """
    Сервис для заказов.
    """
    _logger: logging.Logger = get_logger("OrderService")
    
    def __init__(self, repository: OrderRepository, position_service: PositionService, user_repository: UserRepository):
        """
        Аргументы:
            repository: Репозиторий, который будет использовать сервис
            position_service: Сервис для позиций
        """
        super().__init__(repository)
        self._position_service = position_service
        self._user_repository = user_repository
        
    async def create(self, data: OrderCreateSchema, include_related: bool = True) -> OrderGetSchema:
        """
        Создание объекта.
        
        Аргументы:
            data: Данные для создания объекта
            include_related: Загружать ли связанные объекты
        """
        self._logger.info(f"Создание объекта: {data.model_dump(exclude_unset=True)}")
        
        # Проверка на наличие пользователя в бд
        if not await self._user_repository.get(data.user_id, False):
            self._handle_error("Пользователь с таким ID не найден", status_code=404)
        
        # Проверка на наличие позиций в бд
        for order_position in data.order_positions:
            await self._position_service.get(order_position.position_id, False)
        
        obj: Order = await self._repository.create(data, include_related)
        if not obj:
            self._handle_error("Не удалось создать объект", status_code=400)
        self._logger.info(f"Объект успешно создан с id: {obj.id}")
        
        return self._convert_to_schema(obj)
    
    async def update(self, id: int, data: OrderUpdateSchema, include_related: bool = True) -> OrderGetSchema:
        """
        Обновление объекта.
        
        Аргументы:
            id: ID объекта
            data: Данные для обновления объекта
            include_related: Загружать ли связанные объекты
        """
        self._logger.info(f"Обновление объекта с id: {id} и данными: {data.model_dump(exclude_unset=True)}")
        await self.get(id)
        
        # Проверка на наличие пользователя в бд
        if data.user_id is not None and not await self._user_repository.get(data.user_id, False):
            self._handle_error("Пользователь с таким ID не найден", status_code=404)
        
        # Проверка на наличие позиций в бд
        if data.order_positions:
            for order_position in data.order_positions:
                await self._position_service.get(order_position.position_id)

        obj: Order = await self._repository.update(id, data, include_related)
        if not obj:
            self._handle_error(f"Не удалось обновить объект с id: {id}", status_code=400)
        self._logger.info(f"Объект с id: {id} успешно обновлен")
        
        return self._convert_to_schema(obj)
    
    def _convert_to_schema(self, obj: Order) -> OrderGetSchema:
        """
        Преобразование модели в схему.
        
        Аргументы:
            obj: Модель для преобразования
        """
        try:
            order_positions = [
                OrderPositionGetSchema(
                    position_id=position.position_id,
                    quantity=position.quantity,
                    position=self._position_service._convert_to_schema(position.position)
                )
                for position in obj.order_positions
            ]
            price_sum = obj.price_sum
        except DetachedInstanceError as e: # Если объект не загружен, то возвращаем пустой список
            order_positions = []
            price_sum = None

        return OrderGetSchema(
            id=obj.id,
            user_id=obj.user_id,
            date=obj.date,
            status=Status(obj.status),
            obtaining_method=ObtainingMethod(obj.obtaining_method),
            price_sum=price_sum,
            order_positions=order_positions
        )
        