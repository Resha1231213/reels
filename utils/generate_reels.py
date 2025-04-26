import os
from pathlib import Path
from ai_services import generate_speech
from heygen_video_generation import generate_heygen_video
from utils.video_editor import add_subtitles_to_video, apply_format_overlay

async def generate_reels(user_id, avatar_path, voice_path, script, format_type, subtitles, font, lang):
    media_dir = Path(f"media/{user_id}")
    media_dir.mkdir(parents=True, exist_ok=True)
    voice_file = media_dir / "voice.ogg"
    if not os.path.exists(voice_path):
        ok = await generate_speech(script, lang, voice_file)
        if not ok:
            return None
    video_path = generate_heygen_video(avatar_path, voice_file)
    if not video_path or not os.path.exists(video_path):
        return None
    if subtitles:
        subtitled_path = media_dir / "subtitled.mp4"
        add_subtitles_to_video(video_path, script, subtitled_path, font)
        video_path = subtitled_path
    final_path = media_dir / "final_reels.mp4"
    apply_format_overlay(video_path, format_type, final_path)
    return str(final_path)