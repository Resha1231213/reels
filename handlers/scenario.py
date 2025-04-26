from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.FinalGenerateState import FinalGenerateState
from utils.generate_reels import generate_reels

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("👋 Привет! Я бот для генерации Reels. Нажмите /create чтобы начать.")

@router.message(Command("create"))
async def cmd_create(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FinalGenerateState.waiting_for_avatar)
    await message.answer("Загрузите фото или видео для создания аватара (до 5 файлов).")

@router.message(FinalGenerateState.waiting_for_avatar, F.photo | F.video)
async def handle_avatar(message: Message, state: FSMContext):
    file = message.photo[-1] if message.photo else message.video
    file_id = file.file_id
    await state.update_data(avatar=file_id)
    await state.set_state(FinalGenerateState.waiting_for_voice)
    await message.answer("Теперь отправьте голосовое сообщение или аудиофайл.")

@router.message(FinalGenerateState.waiting_for_voice, F.voice | F.audio)
async def handle_voice(message: Message, state: FSMContext):
    file = message.voice or message.audio
    file_id = file.file_id
    await state.update_data(voice=file_id)
    await state.set_state(FinalGenerateState.enter_script)
    await message.answer("Введите сценарий (текст для видео).")

@router.message(FinalGenerateState.enter_script)
async def handle_script(message: Message, state: FSMContext):
    await state.update_data(script=message.text)
    await state.set_state(FinalGenerateState.select_language)
    await message.answer("Выберите язык озвучки: RU / EN / FR")

@router.message(FinalGenerateState.select_language, F.text.in_(["RU", "EN", "FR"]))
async def handle_language(message: Message, state: FSMContext):
    await state.update_data(language=message.text)
    await state.set_state(FinalGenerateState.select_format)
    await message.answer("Выберите формат видео: фулскрин / 50/50 / круглый аватар")

@router.message(FinalGenerateState.select_format, F.text.in_(["фулскрин", "50/50", "круглый аватар"]))
async def handle_format(message: Message, state: FSMContext):
    await state.update_data(format=message.text)
    await state.set_state(FinalGenerateState.with_subtitles)
    await message.answer("Добавить субтитры? Да / Нет")

@router.message(FinalGenerateState.with_subtitles, F.text.in_(["Да", "Нет"]))
async def handle_subtitles(message: Message, state: FSMContext):
    await state.update_data(subtitles=(message.text == "Да"))
    await state.set_state(FinalGenerateState.confirm_generate)
    await message.answer("Всё готово для генерации! Напишите 'Генерировать', чтобы начать.")

@router.message(FinalGenerateState.confirm_generate, F.text.casefold() == "генерировать")
async def handle_generate(message: Message, state: FSMContext):
    data = await state.get_data()
    result_path = await generate_reels(
        avatar=data.get("avatar"),
        voice=data.get("voice"),
        script=data.get("script"),
        lang=data.get("language"),
        format_type=data.get("format"),
        with_subtitles=data.get("subtitles"),
        user_id=message.from_user.id,
        bot=message.bot
    )
    if result_path:
        await message.answer_video(open(result_path, "rb"), caption="🎬 Ваш Reels готов!")
    else:
        await message.answer("Ошибка при генерации видео.")
    await state.clear()