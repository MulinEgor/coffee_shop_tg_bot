from typing import Type, TypeVar, Generic
from sqlalchemy import func, select
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

from core.db import get_db_session

# Типы pydantic и sqlalchemy моделей
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс для репозитория.
    Репозиторий нужен для работы с БД.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, uuid: str) -> ModelType | None:
        """
        Получение объекта по UUID.
        """
        async with get_db_session() as session:
            stmt = select(self.model).where(self.model.uuid == uuid)
            result = await session.execute(stmt)
            
            return result.scalar_one_or_none()

    async def get_all(self, filters: dict) -> list[ModelType]:
        """
        Получение всех объектов с необязательными фильтрами.
        """
        async with get_db_session() as session:
            stmt = select(self.model)
                    
            if filters:
                processed_filters = self.convert_filters_to_lower_case(filters)
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

    async def update(self, uuid: str, data: UpdateSchemaType) -> ModelType | None:
        """
        Обновление объекта.
        """
        async with get_db_session() as session:
            if obj := await self.get(uuid):
                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(obj, key, value)
                await session.commit()
                await session.refresh(obj)
            
            return obj

    async def delete(self, uuid: str) -> bool:
        """
        Удаление объекта.
        """
        async with get_db_session() as session:
            if obj := await self.get(uuid):
                await session.delete(obj)
                await session.commit()
                
                return True
            
            return False

    def convert_filters_to_lower_case(self, filters: dict) -> list:
        """
        Вспомогательная функция для преобразования фильтров в нижний регистр.
        """
        processed_filters = []
        for k, v in filters.items():
            if isinstance(v, str):
                processed_filters.append(func.lower(getattr(self.model, k)).ilike(f'%{v.lower()}%'))
            else:
                processed_filters.append(getattr(self.model, k) == v)

        return processed_filters
    