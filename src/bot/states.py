from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    """Состояния пользователя."""
    selecting_role = State()
    

class OrderStates(StatesGroup):
    """Состояния заказа."""
    selecting_category = State()
    selecting_position = State()
    selecting_weight = State()
    selecting_quantity = State()
    selecting_obtaining_method = State()
    confirming_order = State() 