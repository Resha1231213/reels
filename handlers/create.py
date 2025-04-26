from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

create_router = Router()

@create_router.message(Command("create"))
async def create_handler(msg: Message):
    await msg.answer("Давайте создадим новый Reels! Загрузите фото или видео для аватара.")
    # Здесь дальше логика FSM/сценария по генерации reels