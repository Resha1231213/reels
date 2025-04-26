from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from states.avatar import AvatarStates
from states.avatar import save_avatar, process_avatar

router = Router()

@router.message(F.text == "/avatar")
async def ask_avatar(msg: Message, state: FSMContext):
    await msg.answer("Загрузите до 5 фото (или видео до 15 секунд), которые станут аватарами.")
    await state.set_state(AvatarStates.waiting_for_avatars)

@router.message(AvatarStates.waiting_for_avatars, F.photo | F.video)
async def receive_avatar(msg: Message, state: FSMContext):
    data = await state.get_data()
    avatars = data.get("avatars", [])
    if msg.photo:
        file_id = msg.photo[-1].file_id
    else:
        file_id = msg.video.file_id
    avatars.append(file_id)
    await state.update_data(avatars=avatars)
    if len(avatars) < 5:
        await msg.answer(f"Аватар {len(avatars)} загружен. Отправьте ещё или напишите /done.")
    else:
        await msg.answer("Достигнут лимит. Все аватары загружены. Продолжить? (напишите /done)")
        await state.set_state(AvatarStates.avatars_ready)

@router.message(AvatarStates.waiting_for_avatars, F.text == "/done")
async def done_avatars(msg: Message, state: FSMContext):
    await state.set_state(AvatarStates.avatars_ready)
    await msg.answer("Аватары успешно загружены. Можно продолжать работу.")