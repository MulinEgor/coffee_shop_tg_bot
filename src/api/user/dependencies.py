from src.api.order.dependencies import get_order_service
from src.core.user.respository import UserRepository
from src.core.user.service import UserService


def get_user_service() -> UserService:
    return UserService(UserRepository(), get_order_service())
