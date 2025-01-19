from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.states import UserStates
from src.core.types import ServiceException
from src.core.user.models import Role
from src.core.user.schemas import UserCreateSchema
from src.core.user.service import UserService

router = Router()


@router.callback_query(UserStates.selecting_role, F.data.startswith("role:"))
async def role_callback(
    callback: CallbackQuery, state: FSMContext, user_service: UserService
):
    """Обработчик выбора роли."""
    role = callback.data.split(":")[1]

    # Создаем пользователя
    try:
        user = await user_service.create(
            UserCreateSchema(id=callback.from_user.id, role=Role(role))
        )
    except ServiceException as e:
        await callback.message.answer(
            f"Произошла ошибка при создании пользователя: {e.detail}"
        )
        return

    await state.clear()

    if user.role == Role.CLIENT:
        await callback.message.edit_text(
            "Роль успешно выбрана!\n" "Используйте /menu чтобы открыть меню"
        )
    elif user.role == Role.BARISTA:
        await callback.message.edit_text(
            "Роль успешно выбрана!\n"
            "Используйте /orders чтобы посмотреть список заказов"
        )
