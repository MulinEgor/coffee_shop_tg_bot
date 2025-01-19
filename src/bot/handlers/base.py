from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import get_role_keyboard
from src.bot.states import UserStates
from src.core.types import ServiceException
from src.core.user.models import Role
from src.core.user.service import UserService

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, user_service: UserService):
    """Обработчик команды /start."""
    try:
        user = await user_service.get(message.from_user.id, False)
    except ServiceException:
        await state.set_state(UserStates.selecting_role)
        await message.answer(
            "Добро пожаловать в бот кофейни!\n" "Пожалуйста, выберите вашу роль:",
            reply_markup=get_role_keyboard(),
        )
        return

    if user.role == Role.CLIENT:
        await message.answer(
            "Добро пожаловать в бот кофейни!\n"
            "Используйте /menu чтобы открыть меню\n"
            "Используйте /help чтобы увидеть список команд"
        )
    elif user.role == Role.BARISTA:
        await message.answer(
            "Добро пожаловать в бот кофейни!\n"
            "Используйте /orders чтобы посмотреть список заказов\n"
            "Используйте /help чтобы увидеть список команд"
        )


@router.message(Command("exit"))
async def exit_handler(message: Message, state: FSMContext, user_service: UserService):
    """Обработчик команды /exit."""
    try:
        await user_service.get(message.from_user.id, False)
    except ServiceException:
        await message.answer(
            "Вы не авторизованы\n" "Используйте /start чтобы начать работать с ботом"
        )
        return

    await user_service.delete(message.from_user.id)

    await message.answer(
        "Вы вышли из аккаунта\n" "Используйте /start чтобы начать работать с ботом"
    )


@router.message(Command("help"))
async def help_handler(message: Message, user_service: UserService):
    """Обработчик команды /help."""
    try:
        user = await user_service.get(message.from_user.id, False)
    except ServiceException:
        await message.answer("Произошла ошибка при получении данных пользователя")
        return

    if user.role == Role.CLIENT:
        await message.answer(
            "Доступные команды:\n"
            "/start - Начать работу с ботом\n"
            "/exit - Выйти из аккаунта\n"
            "/menu - Открыть меню\n"
            "/help - Показать список команд"
        )
    elif user.role == Role.BARISTA:
        await message.answer(
            "Доступные команды:\n"
            "/start - Начать работу с ботом\n"
            "/exit - Выйти из аккаунта\n"
            "/orders - Посмотреть список заказов\n"
            "/help - Показать список команд"
        )
