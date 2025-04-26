import subprocess

def add_subtitles_to_video(video_path, text, out_path, font=None):
    # Создаём временный файл с субтитрами
    subtitles_path = "temp_subtitles.srt"
    with open(subtitles_path, "w", encoding="utf-8") as f:
        f.write(f"1\n00:00:01,000 --> 00:00:10,000\n{text}\n")
    font_str = f":fontfile={font}" if font else ""
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", f"subtitles={subtitles_path}{font_str}",
        out_path
    ]
    subprocess.run(cmd, check=True)
    # Удаляем временный файл
    import os
    os.remove(subtitles_path)

def apply_format_overlay(video_path, format_type, out_path):
    # По формату меняем размер и положение видео (пример для трех типов)
    if format_type == "format_full":
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", "scale=1080:1920", out_path]
    elif format_type == "format_split":
        cmd = [
            "ffmpeg", "-y", "-i", video_path, "-vf",
            "crop=iw/2:ih:0:0,pad=iw*2:ih:(ow-iw)/2:0", out_path
        ]
    elif format_type == "format_circle":
        cmd = [
            "ffmpeg", "-y", "-i", video_path, "-vf",
            "scale=600:600,format=rgba,lut=a=255*between(sqrt((X-300)*(X-300)+(Y-300)*(Y-300)),0,300)", out_path
        ]
    else:
        # По умолчанию — копируем без изменений
        cmd = ["ffmpeg", "-y", "-i", video_path, out_path]
    subprocess.run(cmd, check=True)