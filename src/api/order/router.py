from typing import List

from fastapi import APIRouter, Depends, status

from src.api.order.dependencies import get_order_service
from src.api.order.settings import router_settings
from src.core.order.schemas import OrderCreateSchema, OrderGetSchema, OrderUpdateSchema
from src.core.order.service import OrderService

router = APIRouter(**router_settings.model_dump())


@router.get(
    "/{id}",
    response_model=OrderGetSchema,
    status_code=status.HTTP_200_OK,
    description="Получение заказа по ID",
)
async def get(
    id: int, service: OrderService = Depends(get_order_service)
) -> OrderGetSchema:
    """
    Получение заказа по ID.

    Аргументы:
        id: ID заказа
        service: Сервис для работы с заказами

    Возвращает:
        OrderGetSchema: Данные заказа
    """
    return await service.get(id)


@router.get(
    "/",
    response_model=List[OrderGetSchema],
    status_code=status.HTTP_200_OK,
    description="Получение списка всех заказов",
)
async def get_all(
    service: OrderService = Depends(get_order_service),
) -> List[OrderGetSchema]:
    """
    Получение списка всех заказов.

    Аргументы:
        service: Сервис для работы с заказами

    Возвращает:
        List[OrderGetSchema]: Список заказов
    """
    return await service.get_all()


@router.post(
    "/",
    response_model=OrderGetSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового заказа",
    )
async def create(
    data: OrderCreateSchema, service: OrderService = Depends(get_order_service)
) -> OrderGetSchema:
    """
    Создание нового заказа.

    Аргументы:
        data: Данные для создания заказа
        service: Сервис для работы с заказами

    Возвращает:
        OrderGetSchema: Созданный заказ
    """
    return await service.create(data)


@router.put(
    "/{id}",
    response_model=OrderGetSchema,
    status_code=status.HTTP_200_OK,
    description="Обновление заказа по ID",
)
async def update(
    id: int, data: OrderUpdateSchema, service: OrderService = Depends(get_order_service)
) -> OrderGetSchema:
    """
    Обновление заказа по ID.

    Аргументы:
        id: ID заказа для обновления
        data: Данные для обновления заказа
        service: Сервис для работы с заказами

    Возвращает:
        OrderGetSchema: Обновленный заказ
    """
    return await service.update(id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление заказа по ID",
)
async def delete(id: int, service: OrderService = Depends(get_order_service)):
    """
    Удаление заказа по ID.

    Аргументы:
        id: ID заказа для удаления
        service: Сервис для работы с заказами

    Возвращает:
        None
    """
    await service.delete(id)
