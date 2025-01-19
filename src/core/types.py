from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

# Типы pydantic и sqlalchemy моделей
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ServiceException(Exception):
    """Исключение для сервисов."""

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)
