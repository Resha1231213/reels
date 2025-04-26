import re

async def parse_competitor_reel(link: str):
    # Тут твоя логика: распарсить ссылку, скачать текст/описание/транскрипт видео и т.д.
    # Например, если это YouTube - вытянуть описание или через API вытянуть транскрипт.
    # Вернуть {'script': 'Текст сценария'}
    if "youtube.com" in link or "youtu.be" in link:
        # Заглушка, вставь свою реальную обработку!
        return {"script": "Пример сценария, извлеченного из YouTube"}
    elif "instagram.com" in link:
        return {"script": "Пример сценария, извлеченного из Instagram"}
    elif "tiktok.com" in link:
        return {"script": "Пример сценария, извлеченного из TikTok"}
    else:
        return {}