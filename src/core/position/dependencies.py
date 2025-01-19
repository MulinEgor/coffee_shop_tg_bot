from src.core.category.dependencies import get_category_service
from src.core.position.respository import PositionRepository
from src.core.position.service import PositionService
from src.core.types import ServiceException


def get_position_service(exception: Exception = ServiceException) -> PositionService:
    return PositionService(PositionRepository(), get_category_service(), exception)
