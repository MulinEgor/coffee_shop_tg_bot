from typing import List

from fastapi import APIRouter, Depends, status

from src.api.user.dependencies import get_user_service
from src.api.user.settings import router_settings
from src.core.user.schemas import UserCreateSchema, UserGetSchema, UserUpdateSchema
from src.core.user.service import UserService

router = APIRouter(**router_settings.model_dump())


@router.get(
    "/{id}",
    response_model=UserGetSchema,
    status_code=status.HTTP_200_OK,
    description="Получение пользователя по ID",
)
async def get(
    id: int, service: UserService = Depends(get_user_service)
) -> UserGetSchema:
    """
    Получение пользователя по ID.

    Аргументы:
        id: ID пользователя
        service: Сервис для работы с пользователями

    Возвращает:
        UserGetSchema: Данные пользователя
    """
    return await service.get(id)


@router.get(
    "/",
    response_model=List[UserGetSchema],
    status_code=status.HTTP_200_OK,
    description="Получение списка всех пользователей",
)
async def get_all(
    service: UserService = Depends(get_user_service),
) -> List[UserGetSchema]:
    """
    Получение списка всех пользователей.

    Аргументы:
        service: Сервис для работы с пользователями

    Возвращает:
        List[UserGetSchema]: Список пользователей
    """
    return await service.get_all()


@router.post(
    "/",
    response_model=UserGetSchema,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового пользователя",
)
async def create(
    data: UserCreateSchema, service: UserService = Depends(get_user_service)
) -> UserGetSchema:
    """
    Создание нового пользователя.

    Аргументы:
        data: Данные для создания пользователя
        service: Сервис для работы с пользователями

    Возвращает:
        UserGetSchema: Созданный пользователь
    """
    return await service.create(data)


@router.put(
    "/{id}",
    response_model=UserGetSchema,
    status_code=status.HTTP_200_OK,
    description="Обновление пользователя по ID",
)
async def update(
    id: int, data: UserUpdateSchema, service: UserService = Depends(get_user_service)
) -> UserGetSchema:
    """
    Обновление пользователя по ID.

    Аргументы:
        id: ID пользователя для обновления
        data: Данные для обновления пользователя
        service: Сервис для работы с пользователями

    Возвращает:
        UserGetSchema: Обновленный пользователь
    """
    return await service.update(id, data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление пользователя по ID",
)
async def delete(id: int, service: UserService = Depends(get_user_service)):
    """
    Удаление пользователя по ID.

    Аргументы:
        id: ID пользователя для удаления
        service: Сервис для работы с пользователями

    Возвращает:
        None
    """
    await service.delete(id)
