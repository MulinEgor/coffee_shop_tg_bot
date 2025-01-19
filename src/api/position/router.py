from typing import List

from fastapi import APIRouter, HTTPException, status

from src.api.position.settings import router_settings
from src.core.position.dependencies import get_position_service
from src.core.position.schemas import (
    PositionCreateSchema,
    PositionGetSchema,
    PositionUpdateSchema,
)

router = APIRouter(**router_settings.model_dump())


@router.get(
    "/{id}",
    response_model=PositionGetSchema,
    status_code=status.HTTP_200_OK,
    description="Получение позиции по ID",
)
async def get(id: int) -> PositionGetSchema:
    """
    Получение позиции по ID.

    Аргументы:
        id: ID позиции

    Возвращает:
        PositionGetSchema: Данные позиции
    """
    service = get_position_service(HTTPException)
    return await service.get(id)


@router.get(
    "/",
    response_model=List[PositionGetSchema],
    status_code=status.HTTP_200_OK,
    description="Получение списка всех позиций",
)
async def get_all() -> List[PositionGetSchema]:
    """
    Получение списка всех позиций.

    Возвращает:
        List[PositionGetSchema]: Список позиций
    """
    service = get_position_service(HTTPException)
    return await service.get_all()


@router.post(
    "/",
    response_model=PositionGetSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание новой позиции",
)
async def create(data: PositionCreateSchema) -> PositionGetSchema:
    """
    Создание новой позиции.

    Аргументы:
        data: Данные для создания позиции

    Возвращает:
        PositionGetSchema: Созданная позиция
    """
    service = get_position_service(HTTPException)
    return await service.create(data)


@router.put(
    "/{id}",
    response_model=PositionGetSchema,
    status_code=status.HTTP_200_OK,
    description="Обновление позиции по ID",
)
async def update(id: int, data: PositionUpdateSchema) -> PositionGetSchema:
    """
    Обновление позиции по ID.

    Аргументы:
        id: ID позиции для обновления
        data: Данные для обновления позиции

    Возвращает:
        PositionGetSchema: Обновленная позиция
    """
    service = get_position_service(HTTPException)
    return await service.update(id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление позиции по ID",
)
async def delete(id: int):
    """
    Удаление позиции по ID.

    Аргументы:
        id: ID позиции для удаления

    Возвращает:
        None
    """
    service = get_position_service(HTTPException)
    await service.delete(id)
