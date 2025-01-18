from sqlalchemy.orm.exc import DetachedInstanceError

from src.core.order.service import OrderService
from src.core.user.models import Role, User
from src.core.user.respository import UserRepository
from src.core.user.schemas import UserCreateSchema, UserGetSchema, UserUpdateSchema
from src.core.service import Service


class UserService(Service[User, UserCreateSchema, UserGetSchema, UserUpdateSchema, UserRepository]):
    """
    Сервис для пользователей.
    """
    def __init__(self, repository: UserRepository, order_service: OrderService):
        """
        Инициализация сервиса.
        
        Аргументы:
            repository: Репозиторий, который будет использовать сервис
            order_service: Сервис для заказов
        """
        super().__init__("UserService", repository)
        self._order_service = order_service

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
