from src.core.order.dependencies import get_order_service
from src.core.user.respository import UserRepository
from src.core.user.service import UserService
from src.core.types import ServiceException

def get_user_service(exception: Exception = ServiceException) -> UserService:
    return UserService(UserRepository(), get_order_service(), exception)
