import asyncio
import logging
import os

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from config import BOT_TOKEN, ADMIN_ID

from handlers import create_reels, avatar_selection, start, scenario, support, competitor_analyze

# Загружаем переменные окружения
load_dotenv()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Регистрируем роутеры
dp.include_router(start.router)
dp.include_router(create_reels.router)
dp.include_router(avatar_selection.router)
dp.include_router(scenario.router)
dp.include_router(support.router)
dp.include_router(competitor_analyze.router)

async def main():
    logger.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())