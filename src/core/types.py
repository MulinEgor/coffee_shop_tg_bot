from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

# Типы pydantic и sqlalchemy моделей
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
