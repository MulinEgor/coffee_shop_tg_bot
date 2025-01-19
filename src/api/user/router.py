from typing import List

from fastapi import APIRouter, Depends, status

from src.api.user.dependencies import get_user_service
from src.api.user.settings import router_settings
from src.core.user.schemas import UserCreateSchema, UserGetSchema, UserUpdateSchema
from src.core.user.service import UserService

router = APIRouter(**router_settings.model_dump())


@router.get("/{id}", response_model=UserGetSchema, status_code=status.HTTP_200_OK)
async def get(
    id: int, service: UserService = Depends(get_user_service)
) -> UserGetSchema:
    return await service.get(id)


@router.get("/", response_model=List[UserGetSchema], status_code=status.HTTP_200_OK)
async def get_all(
    service: UserService = Depends(get_user_service),
) -> List[UserGetSchema]:
    return await service.get_all()


@router.post("/", response_model=UserGetSchema, status_code=status.HTTP_201_CREATED)
async def create(
    data: UserCreateSchema, service: UserService = Depends(get_user_service)
) -> UserGetSchema:
    return await service.create(data)


@router.put("/{id}", response_model=UserGetSchema, status_code=status.HTTP_200_OK)
async def update(
    id: int, data: UserUpdateSchema, service: UserService = Depends(get_user_service)
) -> UserGetSchema:
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: UserService = Depends(get_user_service)):
    await service.delete(id)
