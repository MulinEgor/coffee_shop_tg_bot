from typing import List

from fastapi import APIRouter, HTTPException, status

from src.api.category.settings import router_settings
from src.core.category.dependencies import get_category_service
from src.core.category.schemas import CategoryCreateSchema, CategoryGetSchema
from src.core.category.service import CategoryService

router = APIRouter(**router_settings.model_dump())


@router.get(
    "/{id}",
    response_model=CategoryGetSchema,
    status_code=status.HTTP_200_OK,
    description="Получение категории по ID",
)
async def get(
    id: int
) -> CategoryGetSchema:
    """
    Получение категории по ID.

    Аргументы:
        id: ID категории

    Возвращает:
        CategoryGetSchema: Данные категории
    """
    service = get_category_service(HTTPException)
    return await service.get(id, include_related=False)


@router.get(
    "/",
    response_model=List[CategoryGetSchema],
    status_code=status.HTTP_200_OK,
    description="Получение списка всех категорий",
)
async def get_all() -> List[CategoryGetSchema]:
    """
    Получение списка всех категорий.

    Возвращает:
        List[CategoryGetSchema]: Список категорий
    """
    service = get_category_service(HTTPException)
    return await service.get_all(include_related=False)


@router.post(
    "/",
    response_model=CategoryGetSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание новой категории",
)
async def create(
    data: CategoryCreateSchema
) -> CategoryGetSchema:
    """
    Создание новой категории.

    Аргументы:
        data: Данные для создания категории

    Возвращает:
        CategoryGetSchema: Созданная категория
    """
    service = get_category_service(HTTPException)
    return await service.create(data, include_related=False)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление категории по ID. Рекурсивно удаляет все позиции в этой категории",
)
async def delete(id: int):
    """
    Удаление категории по ID.

    Аргументы:
        id: ID категории для удаления

    Возвращает:
        None
    """
    service = get_category_service(HTTPException)
    await service.delete(id)
    