from fastapi import APIRouter, status, Depends
from typing import List

from src.core.category.service import CategoryService
from src.core.category.schemas import CategoryCreateSchema, CategoryGetSchema
from src.api.category.settings import router_settings
from src.api.category.dependencies import get_category_service


router = APIRouter(
    **router_settings.model_dump()
)


@router.get(
    "/{id}",
    response_model=CategoryGetSchema,
    status_code=status.HTTP_200_OK
)
async def get(
    id: int,
    service: CategoryService = Depends(get_category_service)
) -> CategoryGetSchema:
    return await service.get(id, include_related=False)


@router.get(
    "/",
    response_model=List[CategoryGetSchema],
    status_code=status.HTTP_200_OK
)
async def get_all(
    service: CategoryService = Depends(get_category_service)
) -> List[CategoryGetSchema]:
    return await service.get_all(include_related=False)


@router.post(
    "/",
    response_model=CategoryGetSchema,
    status_code=status.HTTP_201_CREATED
)
async def create(
    data: CategoryCreateSchema,
    service: CategoryService = Depends(get_category_service)
) -> CategoryGetSchema:
    return await service.create(data, include_related=False)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)   
async def delete(
    id: int,
    service: CategoryService = Depends(get_category_service)
):
    await service.delete(id)
    