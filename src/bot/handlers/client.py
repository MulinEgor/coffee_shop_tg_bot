from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


from src.core.user.models import Role
from src.core.user.service import UserService
from src.core.category.service import CategoryService
from src.bot.keyboards import get_categories_keyboard
from src.bot.states import OrderStates


router = Router()


@router.message(Command("menu"))
async def menu_handler(message: Message, state: FSMContext, user_service: UserService, category_service: CategoryService):
    """Обработчик команды /menu."""
    user = await user_service.get(message.from_user.id, False)
    if not user:
        await message.answer(
            "Вы не зарегистрированы.\n"
            "Используйте /start для регистрации"
        )
        return
    
    if user.role == Role.BARISTA:
        await message.answer(
            "Используйте /orders чтобы посмотреть список заказов"
        )
        return
    
    await state.set_state(OrderStates.selecting_category)
    
    categories = await category_service.get_all()
    text = "Выберите категорию:"
    
    if isinstance(message, CallbackQuery):
        await message.message.edit_text(text, reply_markup=get_categories_keyboard(categories))
    else:
        await message.answer(text, reply_markup=get_categories_keyboard(categories)) 
    