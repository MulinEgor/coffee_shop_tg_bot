from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.core.user.service import UserService
from src.bot.keyboards import get_role_keyboard
from src.bot.states import UserStates


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, user_service: UserService):
    """Обработчик команды /start."""
    user = await user_service.get(message.from_user.id, False)
    if user:
        await message.answer(
            "Добро пожаловать в бот кофейни!\n"
            "Используйте /menu чтобы открыть меню"
        )
        return
    
    await state.set_state(UserStates.selecting_role)
    await message.answer(
        "Добро пожаловать в бот кофейни!\n"
        "Пожалуйста, выберите вашу роль:",
        reply_markup=get_role_keyboard()
    )
