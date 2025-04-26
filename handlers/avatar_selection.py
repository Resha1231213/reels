from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.fsm.context import FSMContext
from states.AvatarSelectState import AvatarSelectState
from states.FinalGenerateState import FinalGenerateState
from pathlib import Path

router = Router()
MAX_AVATARS = 5

@router.message(AvatarSelectState.waiting_for_avatar)
async def handle_avatar_upload(msg: Message, state: FSMContext):
    if not (msg.photo or msg.document):
        await msg.answer("Пожалуйста, отправьте фото или документ для аватара.")
        return

    user_id = msg.from_user.id
    media_dir = Path(f"media/{user_id}")
    media_dir.mkdir(parents=True, exist_ok=True)
    file_path = media_dir / "avatar.jpg"

    if msg.photo:
        await msg.photo[-1].download(destination=file_path)
    elif msg.document:
        await msg.document.download(destination=file_path)
    await state.update_data(avatar=str(file_path))

    await msg.answer_photo(
        FSInputFile(file_path),
        caption="Фото успешно загружено! Продолжить?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Да, продолжить", callback_data="avatar_ok")],
                [InlineKeyboardButton(text="🔄 Загрузить другое", callback_data="avatar_again")]
            ]
        )
    )
    await state.set_state(AvatarSelectState.confirm_avatar)

@router.callback_query(AvatarSelectState.confirm_avatar, F.data == "avatar_ok")
async def avatar_confirmed(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Аватар сохранён! Теперь загрузите голосовое сообщение.")
    await state.set_state(FinalGenerateState.waiting_for_voice)
    await callback.answer()

@router.callback_query(AvatarSelectState.confirm_avatar, F.data == "avatar_again")
async def avatar_again(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправьте новое фото для аватара.")
    await state.set_state(AvatarSelectState.waiting_for_avatar)
    await callback.answer()