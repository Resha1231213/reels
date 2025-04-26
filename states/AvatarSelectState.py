from aiogram.fsm.state import StatesGroup, State

class AvatarSelectState(StatesGroup):
    waiting_for_avatar = State()
    confirm_avatar = State()