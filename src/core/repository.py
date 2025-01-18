from typing import Type, Generic, TypeVar
from sqlalchemy import Select, delete, func, select
from sqlalchemy.orm import joinedload

from src.core.db import get_db_session
from src.core.types import ModelType, CreateSchemaType, UpdateSchemaType


class Repository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс для репозитория.
    Репозиторий нужен для работы с БД.
    """
    def __init__(self, model: Type[ModelType]):
        """
        Аргументы:
            model: Sqlalchemy модель, которую будет использовать репозиторий.
        """
        self.model = model

    async def get(self, id: int, include_related: bool) -> ModelType | None:
        """
        Получение объекта по ID.
        
        Аргументы:
            id: ID объекта
            include_related: Загружать ли связанные объекты
        """
        async with get_db_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            if include_related:
                stmt = self._include_related(stmt)
            result = await session.execute(stmt)
            return result.unique().scalar_one_or_none()

    async def get_all(self, include_related: bool, filters: UpdateSchemaType | None = None) -> list[ModelType]:
        """
        Получение всех объектов с необязательными фильтрами.
        
        Аргументы:
            include_related: Загружать ли связанные объекты
            filters: Фильтры для поиска
        """
        async with get_db_session() as session:
            stmt = select(self.model)
            if include_related:
                stmt = self._include_related(stmt)
                    
            if filters:
                processed_filters = self._convert_filters_to_lower_case(filters)
                stmt = stmt.where(*processed_filters)
                
            result = await session.execute(stmt)
            return list(result.unique().scalars().all())

    async def create(self, data: CreateSchemaType, include_related: bool) -> ModelType:
        """
        Создание объекта.
        
        Аргументы:
            data: Данные для создания объекта
            include_related: Загружать ли связанные объекты
        """
        async with get_db_session() as session:
            obj = self.model(**data.model_dump())
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            
            stmt = select(self.model).where(self.model.id == obj.id)
            if include_related:
                stmt = self._include_related(stmt)
            result = await session.execute(stmt)
            return result.unique().scalar_one()

    async def update(self, id: int, data: UpdateSchemaType, include_related: bool) -> ModelType | None:
        """
        Обновление объекта.
        
        Аргументы:
            id: ID объекта
            data: Данные для обновления объекта
            include_related: Загружать ли связанные объекты
        """
        async with get_db_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            if include_related:
                stmt = self._include_related(stmt)
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
        
        Аргументы:
            id: ID объекта
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
        
    async def delete_all(self):
        """
        Удаление всех объектов.
        """
        async with get_db_session() as session:
            await session.execute(delete(self.model))
            await session.commit()

    def _convert_filters_to_lower_case(self, filters: UpdateSchemaType) -> list:
        """
        Вспомогательная функция для преобразования фильтров в нижний регистр.
        
        Аргументы:
            filters: Фильтры для поиска
        """
        processed_filters = []
        for k, v in filters.model_dump(exclude_unset=True).items():
            if isinstance(v, str):
                processed_filters.append(func.lower(getattr(self.model, k)).ilike(f'%{v.lower()}%'))
            else:
                processed_filters.append(getattr(self.model, k) == v)

        return processed_filters
    
    def _include_related(self, stmt: Select) -> Select:
        """
        Вспомогательная функция для включения связанных объектов.
        
        Аргументы:
            stmt: SQLAlchemy запрос
        """
        for relationship in self.model.__mapper__.relationships:
            stmt = stmt.options(joinedload(getattr(self.model, relationship.key)))
        return stmt
    
    
RepositoryType = TypeVar("RepositoryType", bound=Repository)
