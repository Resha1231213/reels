from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

def real_analyze_competitor_link(link: str) -> str:
    # Тут должна быть реальная логика парсера. Пока простая заглушка-ответ.
    if "instagram" in link:
        return "Instagram-конкурент: 56 Reels, вовлечённость 8.3%, лучшие: top1, top2, top3"
    elif "tiktok" in link:
        return "TikTok-конкурент: 140 роликов, вовлечённость 10.7%, лучшие: topA, topB"
    elif "youtube" in link:
        return "YouTube Shorts: 80 роликов, средний просмотр: 12k"
    else:
        return "Неизвестная платформа. Проверь ссылку."

def real_analyze_competitor_name(name: str) -> str:
    # Здесь может быть реальный вызов к API или парсеру.
    return f"Конкурент {name}: бренд найден, вовлечённость 7.2/10, успешных роликов — 3"

@router.message(Command("competitors"))
async def handle_competitors_command(message: types.Message, state: FSMContext):
    await message.answer(
        "Введи ссылку на Reels конкурента (Instagram/TikTok/YouTube) или название конкурента для анализа:"
    )

@router.message(F.text.regexp(r'https?://(www\.)?(instagram|tiktok|youtube)\.'))
async def handle_competitor_link(message: types.Message, state: FSMContext):
    link = message.text.strip()
    analytics = real_analyze_competitor_link(link)
    await message.answer(f"🔍 Анализ конкурента по ссылке:\n{analytics}")

@router.message()
async def handle_competitor_name(message: types.Message, state: FSMContext):
    competitor = message.text.strip()
    analytics = real_analyze_competitor_name(competitor)
    await message.answer(f"🔍 Анализ конкурента по названию:\n{analytics}")