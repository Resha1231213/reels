# ai_services.py

import os
import requests
import openai

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

openai.api_key = OPENAI_API_KEY

def generate_scenario(prompt: str, lang: str = "ru") -> str:
    """
    Генерация сценария через OpenAI по промпту (описанию, теме) и языку.
    """
    openai.api_key = OPENAI_API_KEY

    messages = [
        {"role": "system", "content": f"Ты профессиональный сценарист видео Reels на {lang.upper()}."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Или другой нужный тебе, например gpt-4
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        n=1
    )
    scenario = response['choices'][0]['message']['content'].strip()
    return scenario

def generate_speech(text, language="ru", output_path="voice.mp3"):
    try:
        response = openai.audio.speech.create(
            model="tts-1",            # или нужную тебе модель
            voice="alloy",            # можно менять voice (alloy, echo, fable, onyx, nova, shimmer)
            input=text,
            response_format="mp3",
            speed=1.0
        )
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"[OpenAI ERROR]: {e}")
        return False

def generate_heygen_video(photo_path, audio_path, output_path):
    '''
    Пример генерации talking-head видео через Heygen API
    '''
    url = "https://api.heygen.com/v1/video/generate"
    headers = {
        "Authorization": f"Bearer {HEYGEN_API_KEY}"
    }
    files = {
        'photo': open(photo_path, 'rb'),
        'audio': open(audio_path, 'rb')
    }
    data = {
        "voice": "auto",         # или нужные тебе параметры
        "preset": "default",     # можно настроить под задачу
    }
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        # Ожидание генерации видео (если асинхронно - получить job_id и доп. проверять статус)
        result_json = response.json()
        video_url = result_json.get("video_url")
        # Качаем финальное видео
        if video_url:
            video_data = requests.get(video_url)
            with open(output_path, "wb") as f:
                f.write(video_data.content)
            return output_path
        else:
            print(f"[Heygen ERROR]: Video URL not found! Response: {result_json}")
            return None
    except Exception as e:
        print(f"[Heygen ERROR]: {e}")
        return None