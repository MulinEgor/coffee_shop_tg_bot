from typing import List

from fastapi import APIRouter, HTTPException, status

from src.api.order.settings import router_settings
from src.core.order.dependencies import get_order_service
from src.core.order.schemas import OrderCreateSchema, OrderGetSchema, OrderUpdateSchema

router = APIRouter(**router_settings.model_dump())


@router.get(
    "/{id}",
    response_model=OrderGetSchema,
    status_code=status.HTTP_200_OK,
    description="Получение заказа по ID",
)
async def get(id: int) -> OrderGetSchema:
    """
    Получение заказа по ID.

    Аргументы:
        id: ID заказа

    Возвращает:
        OrderGetSchema: Данные заказа
    """
    service = get_order_service(HTTPException)
    return await service.get(id)


@router.get(
    "/",
    response_model=List[OrderGetSchema],
    status_code=status.HTTP_200_OK,
    description="Получение списка всех заказов",
)
async def get_all() -> List[OrderGetSchema]:
    """
    Получение списка всех заказов.

    Возвращает:
        List[OrderGetSchema]: Список заказов
    """
    service = get_order_service(HTTPException)
    return await service.get_all()


@router.post(
    "/",
    response_model=OrderGetSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового заказа",
)
async def create(data: OrderCreateSchema) -> OrderGetSchema:
    """
    Создание нового заказа.

    Аргументы:
        data: Данные для создания заказа

    Возвращает:
        OrderGetSchema: Созданный заказ
    """
    service = get_order_service(HTTPException)
    return await service.create(data)


@router.put(
    "/{id}",
    response_model=OrderGetSchema,
    status_code=status.HTTP_200_OK,
    description="Обновление заказа по ID",
)
async def update(id: int, data: OrderUpdateSchema) -> OrderGetSchema:
    """
    Обновление заказа по ID.

    Аргументы:
        id: ID заказа для обновления
        data: Данные для обновления заказа

    Возвращает:
        OrderGetSchema: Обновленный заказ
    """
    service = get_order_service(HTTPException)
    return await service.update(id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление заказа по ID",
)
async def delete(id: int):
    """
    Удаление заказа по ID.

    Аргументы:
        id: ID заказа для удаления

    Возвращает:
        None
    """
    service = get_order_service(HTTPException)
    await service.delete(id)
