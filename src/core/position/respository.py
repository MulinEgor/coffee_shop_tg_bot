from sqlalchemy import select

from src.core.position.models import Position
from src.core.position.schemas import PositionCreateSchema, PositionUpdateSchema
from src.core.db import get_db_session
from src.core.repository import Repository


class PositionRepository(Repository[Position, PositionCreateSchema, PositionUpdateSchema]):
    """
    Репозиторий для позиций. 
    """
    
    def __init__(self):
        super().__init__(Position)
    
    async def get_by_name(self, name: str) -> Position:
        """
        Получение позиции по названию.
        
        Аргументы:
            name: Название позиции
        """
        async with get_db_session() as session:
            result = await session.execute(select(Position).where(Position.name == name))
            return result.scalar_one_or_none()
    