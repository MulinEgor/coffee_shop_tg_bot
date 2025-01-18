from src.core.position.respository import PositionRepository
from src.core.position.service import PositionService
from src.api.category.dependencies import get_category_service


def get_position_service() -> PositionService:
    return PositionService(PositionRepository(), get_category_service())
