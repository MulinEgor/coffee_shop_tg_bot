from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.core.user.service import UserService
from src.core.user.schemas import UserCreateSchema
from src.core.user.models import Role
from src.bot.states import UserStates


router = Router()


@router.callback_query(UserStates.selecting_role, F.data.startswith("role:"))
async def role_callback(callback: CallbackQuery, state: FSMContext, user_service: UserService):
    """Обработчик выбора роли."""
    role = callback.data.split(":")[1]
    
    # Создаем пользователя
    await user_service.create(UserCreateSchema(
        id=callback.from_user.id,
        role=Role(role)
    ))
    
    await state.clear()
    await callback.message.edit_text(
        "Роль успешно выбрана!\n"
        "Используйте /menu чтобы открыть меню"
    ) 