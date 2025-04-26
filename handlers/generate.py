from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from states.FinalGenerateState import FinalGenerateState
from utils.video_editor import add_subtitles_to_video, apply_format_overlay
from ai_services import generate_speech
from heygen_video_generation import generate_heygen_video
from pathlib import Path
from uuid import uuid4
import os

router = Router()

@router.message(FinalGenerateState.confirm_generate)
async def generate_final_reels(msg: Message, state: FSMContext):
    data = await state.get_data()
    user_id = msg.from_user.id

    avatar_path = data.get("avatar")
    voice_path = data.get("voice")
    script = data.get("script")
    lang = data.get("language")
    format_type = data.get("format")
    subtitles = data.get("subtitles", False)
    font_path = data.get("font", None)

    media_dir = Path(f"media/{user_id}")
    media_dir.mkdir(parents=True, exist_ok=True)
    raw_video_path = media_dir / f"raw_{uuid4().hex}.mp4"
    final_video_path = media_dir / f"reels_{uuid4().hex}.mp4"

    # Генерация голоса, если файл отсутствует
    if not voice_path or not os.path.exists(voice_path):
        success = generate_speech(script, language=lang, output_path=voice_path)
        if not success:
            await msg.answer("Ошибка генерации голоса.")
            return

    # Генерация talking-head видео через Heygen
    result_path = generate_heygen_video(
        photo_path=avatar_path,
        audio_path=voice_path,
        output_path=raw_video_path
    )
    if not result_path or not os.path.exists(result_path):
        await msg.answer("Ошибка генерации talking-head видео через Heygen.")
        return

    result_video = result_path

    # Добавление субтитров
    if subtitles:
        subtitled_path = media_dir / f"subtitled_{uuid4().hex}.mp4"
        result_video = add_subtitles_to_video(
            result_video,
            script,
            subtitled_path,
            font_path=font_path
        )
        if not os.path.exists(result_video):
            await msg.answer("Ошибка при добавлении субтитров.")
            return

    # Применение формата
    formatted_path = apply_format_overlay(result_video, format_type, final_video_path)
    if not os.path.exists(formatted_path):
        await msg.answer("Ошибка финального рендера.")
        return

    await msg.answer_video(video=FSInputFile(formatted_path), caption="Ваш Reels готов!")
    await state.clear()