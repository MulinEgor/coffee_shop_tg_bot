from fastapi import APIRouter, status, Depends
from typing import List

from src.core.position.service import PositionService
from src.core.position.schemas import PositionCreateSchema, PositionGetSchema, PositionUpdateSchema
from src.api.position.settings import router_settings
from src.api.position.dependencies import get_position_service


router = APIRouter(
    **router_settings.model_dump()
)


@router.get(
    "/{id}",
    response_model=PositionGetSchema,
    status_code=status.HTTP_200_OK
)
async def get(
    id: int,
    service: PositionService = Depends(get_position_service)
) -> PositionGetSchema:
    return await service.get(id)


@router.get(
    "/",
    response_model=List[PositionGetSchema],
    status_code=status.HTTP_200_OK
)
async def get_all(
    service: PositionService = Depends(get_position_service)
) -> List[PositionGetSchema]:
    return await service.get_all()


@router.post(
    "/",
    response_model=PositionGetSchema,
    status_code=status.HTTP_201_CREATED
)
async def create(
    data: PositionCreateSchema,
    service: PositionService = Depends(get_position_service)
) -> PositionGetSchema:
    return await service.create(data)

@router.put(
    "/{id}",
    response_model=PositionGetSchema,
    status_code=status.HTTP_200_OK
)
async def update(
    id: int,
    data: PositionUpdateSchema,
    service: PositionService = Depends(get_position_service)
) -> PositionGetSchema: 
    return await service.update(id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)   
async def delete(
    id: int,
    service: PositionService = Depends(get_position_service)
):
    await service.delete(id)
    