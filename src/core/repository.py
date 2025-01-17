from typing import Type, Generic, TypeVar
from sqlalchemy import func, select

from src.core.category import respository
from src.core.db import get_db_session
from src.core.types import ModelType, CreateSchemaType, UpdateSchemaType


class Repository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс для репозитория.
    Репозиторий нужен для работы с БД.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: int) -> ModelType | None:
        """
        Получение объекта по ID.
        """
        async with get_db_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            
            return result.scalar_one_or_none()

    async def get_all(self, filters: UpdateSchemaType | None = None) -> list[ModelType]:
        """
        Получение всех объектов с необязательными фильтрами.
        """
        async with get_db_session() as session:
            stmt = select(self.model)
                    
            if filters:
                processed_filters = self._convert_filters_to_lower_case(filters)
                stmt = stmt.where(*processed_filters)
                
            result = await session.execute(stmt)
            
            return list(result.scalars().all())

    async def create(self, data: CreateSchemaType) -> ModelType:
        """
        Создание объекта.
        """
        async with get_db_session() as session:
            obj = self.model(**data.model_dump())
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            
            return obj

    async def update(self, id: int, data: UpdateSchemaType) -> ModelType | None:
        """
        Обновление объекта.
        """
        async with get_db_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if obj:
                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(obj, key, value)
                await session.commit()
                await session.refresh(obj)
            
            return obj

    async def delete(self, id: int) -> bool:
        """
        Удаление объекта.
        """
        async with get_db_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if obj:
                await session.delete(obj)
                await session.commit()
                
                return True
            
            return False

    def _convert_filters_to_lower_case(self, filters: UpdateSchemaType) -> list:
        """
        Вспомогательная функция для преобразования фильтров в нижний регистр.
        """
        processed_filters = []
        for k, v in filters.model_dump(exclude_unset=True).items():
            if isinstance(v, str):
                processed_filters.append(func.lower(getattr(self.model, k)).ilike(f'%{v.lower()}%'))
            else:
                processed_filters.append(getattr(self.model, k) == v)

        return processed_filters
    
    
RepositoryType = TypeVar("RepositoryType", bound=Repository)
