from typing import List

from fastapi import APIRouter, HTTPException, status

from src.api.user.settings import router_settings
from src.core.user.dependencies import get_user_service
from src.core.user.schemas import UserCreateSchema, UserGetSchema, UserUpdateSchema

router = APIRouter(**router_settings.model_dump())


@router.get(
    "/{id}",
    response_model=UserGetSchema,
    status_code=status.HTTP_200_OK,
    description="Получение пользователя по ID",
)
async def get(id: int) -> UserGetSchema:
    """
    Получение пользователя по ID.

    Аргументы:
        id: ID пользователя

    Возвращает:
        UserGetSchema: Данные пользователя
    """
    service = get_user_service(HTTPException)
    return await service.get(id)


@router.get(
    "/",
    response_model=List[UserGetSchema],
    status_code=status.HTTP_200_OK,
    description="Получение списка всех пользователей",
)
async def get_all() -> List[UserGetSchema]:
    """
    Получение списка всех пользователей.

    Возвращает:
        List[UserGetSchema]: Список пользователей
    """
    service = get_user_service(HTTPException)
    return await service.get_all()


@router.post(
    "/",
    response_model=UserGetSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового пользователя",
)
async def create(data: UserCreateSchema) -> UserGetSchema:
    """
    Создание нового пользователя.

    Аргументы:
        data: Данные для создания пользователя

    Возвращает:
        UserGetSchema: Созданный пользователь
    """
    service = get_user_service(HTTPException)
    return await service.create(data)


@router.put(
    "/{id}",
    response_model=UserGetSchema,
    status_code=status.HTTP_200_OK,
    description="Обновление пользователя по ID",
)
async def update(id: int, data: UserUpdateSchema) -> UserGetSchema:
    """
    Обновление пользователя по ID.

    Аргументы:
        id: ID пользователя для обновления
        data: Данные для обновления пользователя

    Возвращает:
        UserGetSchema: Обновленный пользователь
    """
    service = get_user_service(HTTPException)
    return await service.update(id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление пользователя по ID",
)
async def delete(id: int):
    """
    Удаление пользователя по ID.

    Аргументы:
        id: ID пользователя для удаления

    Возвращает:
        None
    """
    service = get_user_service(HTTPException)
    await service.delete(id)
