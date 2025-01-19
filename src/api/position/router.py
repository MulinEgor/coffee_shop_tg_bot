from typing import List

from fastapi import APIRouter, Depends, status

from src.api.position.dependencies import get_position_service
from src.api.position.settings import router_settings
from src.core.position.schemas import (
    PositionCreateSchema,
    PositionGetSchema,
    PositionUpdateSchema,
)
from src.core.position.service import PositionService

router = APIRouter(**router_settings.model_dump())


@router.get(
    "/{id}",
    response_model=PositionGetSchema,
    status_code=status.HTTP_200_OK,
    description="Получение позиции по ID",
)
async def get(
    id: int, service: PositionService = Depends(get_position_service)
) -> PositionGetSchema:
    """
    Получение позиции по ID.

    Аргументы:
        id: ID позиции
        service: Сервис для работы с позициями

    Возвращает:
        PositionGetSchema: Данные позиции
    """
    return await service.get(id)


@router.get(
    "/",
    response_model=List[PositionGetSchema],
    status_code=status.HTTP_200_OK,
    description="Получение списка всех позиций",
)
async def get_all(
    service: PositionService = Depends(get_position_service),
) -> List[PositionGetSchema]:
    """
    Получение списка всех позиций.

    Аргументы:
        service: Сервис для работы с позициями

    Возвращает:
        List[PositionGetSchema]: Список позиций
    """
    return await service.get_all()


@router.post(
    "/",
    response_model=PositionGetSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание новой позиции",
)
async def create(
    data: PositionCreateSchema, service: PositionService = Depends(get_position_service)
) -> PositionGetSchema:
    """
    Создание новой позиции.

    Аргументы:
        data: Данные для создания позиции
        service: Сервис для работы с позициями

    Возвращает:
        PositionGetSchema: Созданная позиция
    """
    return await service.create(data)


@router.put(
    "/{id}",
    response_model=PositionGetSchema,
    status_code=status.HTTP_200_OK,
    description="Обновление позиции по ID",
)
async def update(
    id: int,
    data: PositionUpdateSchema,
    service: PositionService = Depends(get_position_service),
) -> PositionGetSchema:
    """
    Обновление позиции по ID.

    Аргументы:
        id: ID позиции для обновления
        data: Данные для обновления позиции
        service: Сервис для работы с позициями

    Возвращает:
        PositionGetSchema: Обновленная позиция
    """
    return await service.update(id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление позиции по ID",
)
async def delete(id: int, service: PositionService = Depends(get_position_service)):
    """
    Удаление позиции по ID.

    Аргументы:
        id: ID позиции для удаления
        service: Сервис для работы с позициями

    Возвращает:
        None
    """
    await service.delete(id)
