from src.core.user.respository import UserRepository
from src.core.order.respository import OrderRepository
from src.core.order.service import OrderService
from src.api.position.dependencies import get_position_service


def get_order_service() -> OrderService:
    return OrderService(OrderRepository(), get_position_service(), UserRepository())
