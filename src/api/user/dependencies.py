from src.core.user.respository import UserRepository
from src.core.user.service import UserService
from src.api.order.dependencies import get_order_service

def get_user_service() -> UserService:
    return UserService(UserRepository(), get_order_service())
