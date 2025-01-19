from src.core.order.respository import OrderRepository
from src.core.order.service import OrderService
from src.core.position.dependencies import get_position_service
from src.core.types import ServiceException
from src.core.user.respository import UserRepository


def get_order_service(exception: Exception = ServiceException) -> OrderService:
    return OrderService(
        OrderRepository(), get_position_service(), UserRepository(), exception
    )
