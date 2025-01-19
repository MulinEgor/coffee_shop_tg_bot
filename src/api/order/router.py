from typing import List

from fastapi import APIRouter, Depends, status

from src.api.order.dependencies import get_order_service
from src.api.order.settings import router_settings
from src.core.order.schemas import OrderCreateSchema, OrderGetSchema, OrderUpdateSchema
from src.core.order.service import OrderService

router = APIRouter(**router_settings.model_dump())


@router.get("/{id}", response_model=OrderGetSchema, status_code=status.HTTP_200_OK)
async def get(
    id: int, service: OrderService = Depends(get_order_service)
) -> OrderGetSchema:
    return await service.get(id)


@router.get("/", response_model=List[OrderGetSchema], status_code=status.HTTP_200_OK)
async def get_all(
    service: OrderService = Depends(get_order_service),
) -> List[OrderGetSchema]:
    return await service.get_all()


@router.post("/", response_model=OrderGetSchema, status_code=status.HTTP_201_CREATED)
async def create(
    data: OrderCreateSchema, service: OrderService = Depends(get_order_service)
) -> OrderGetSchema:
    return await service.create(data)


@router.put("/{id}", response_model=OrderGetSchema, status_code=status.HTTP_200_OK)
async def update(
    id: int, data: OrderUpdateSchema, service: OrderService = Depends(get_order_service)
) -> OrderGetSchema:
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: OrderService = Depends(get_order_service)):
    await service.delete(id)
