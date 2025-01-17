from typing import TypeVar
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel


# Типы pydantic и sqlalchemy моделей
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
