from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.FinalGenerateState import FinalGenerateState

router = Router()

@router.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Добро пожаловать! Нажмите /create для создания Reels.")

@router.message(Command("create"))
async def start_create(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Загрузите фото или видео для аватара.")
    await state.set_state(FinalGenerateState.waiting_for_avatar)

@router.message(FinalGenerateState.waiting_for_avatar, F.photo | F.video | F.document)
async def avatar_uploaded(msg: Message, state: FSMContext):
    file_id = (
        msg.photo[-1].file_id if msg.photo
        else msg.video.file_id if msg.video
        else msg.document.file_id if msg.document
        else None
    )
    if not file_id:
        await msg.answer("Пожалуйста, отправьте фото или видео!")
        return
    await state.update_data(avatar_file_id=file_id)
    await msg.answer("Фото/видео получено! Теперь отправьте голосовое сообщение или аудиофайл.")
    await state.set_state(FinalGenerateState.waiting_for_voice)

@router.message(FinalGenerateState.waiting_for_voice, F.voice | F.audio)
async def voice_uploaded(msg: Message, state: FSMContext):
    voice_id = msg.voice.file_id if msg.voice else msg.audio.file_id if msg.audio else None
    if not voice_id:
        await msg.answer("Пожалуйста, отправьте голосовое сообщение или аудиофайл!")
        return
    await state.update_data(voice_file_id=voice_id)
    await msg.answer("Голос получен! Введите текст сценария или отправьте ссылку на видео.")
    await state.set_state(FinalGenerateState.enter_script)

@router.message(FinalGenerateState.enter_script, F.text)
async def script_uploaded(msg: Message, state: FSMContext):
    await state.update_data(script=msg.text)
    await msg.answer("Сценарий получен! Хотите добавить субтитры? (да/нет)")
    await state.set_state(FinalGenerateState.with_subtitles)

@router.message(FinalGenerateState.with_subtitles, F.text.casefold().in_(["да", "нет"]))
async def handle_subtitles_choice(msg: Message, state: FSMContext):
    if msg.text.casefold() == "да":
        await msg.answer("Загрузите .ttf файл шрифта для субтитров или напишите 'стандарт' для стандартного шрифта.")
        await state.set_state(FinalGenerateState.upload_font)
    else:
        await state.update_data(subtitles=False)
        await msg.answer("Генерирую видео без субтитров...")
        await state.set_state(FinalGenerateState.confirm_generate)
        await generate_reels_state(msg, state)

@router.message(FinalGenerateState.upload_font, F.document)
async def handle_font_upload(msg: Message, state: FSMContext):
    font_id = msg.document.file_id
    await state.update_data(font_file_id=font_id, subtitles=True)
    await msg.answer("Шрифт загружен! Генерирую видео...")
    await state.set_state(FinalGenerateState.confirm_generate)
    await generate_reels_state(msg, state)

@router.message(FinalGenerateState.upload_font, F.text.casefold() == "стандарт")
async def handle_standard_font(msg: Message, state: FSMContext):
    await state.update_data(font_file_id=None, subtitles=True)
    await msg.answer("Использую стандартный шрифт! Генерирую видео...")
    await state.set_state(FinalGenerateState.confirm_generate)
    await generate_reels_state(msg, state)

@router.message(FinalGenerateState.confirm_generate)
async def generate_reels_state(msg: Message, state: FSMContext):
    data = await state.get_data()
    # Здесь вызови свою функцию генерации видео
    # result_path = generate_reels(**data)
    # await msg.answer_video(video=FSInputFile(result_path), caption="🎬 Ваш Reels готов!")
    await msg.answer("🎬 Ваш Reels готов! (здесь будет отправка видео)")
    await state.clear()