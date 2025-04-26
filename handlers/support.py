from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.FinalGenerateState import FinalGenerateState

router = Router()

@router.message(Command("support"))
async def cmd_support(message: types.Message, state: FSMContext):
    await message.answer("Напишите свой вопрос в поддержку:")
    await state.set_state(FinalGenerateState.support_state)  # Убедись, что это состояние есть в states!