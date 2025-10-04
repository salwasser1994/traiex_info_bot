import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# Берём токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в переменных окружения!")

# Создаём объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Отправь мне любой файл (фото, видео, документ, стикер, аудио, голосовое и т.д.), "
        "а я пришлю тебе его file_id."
    )


@dp.message(F.document | F.photo | F.video | F.audio | F.voice | F.video_note | F.sticker)
async def get_file_id(message: Message):
    file = None

    if message.document:
        file = message.document
    elif message.photo:
        file = message.photo[-1]  # самое качественное фото
    elif message.video:
        file = message.video
    elif message.audio:
        file = message.audio
    elif message.voice:
        file = message.voice
    elif message.video_note:
        file = message.video_note
    elif message.sticker:
        file = message.sticker

    if file:
        await message.answer(
            f"✅ file_id:\n<code>{file.file_id}</code>",
            parse_mode="HTML",
        )
    else:
        await message.answer("❌ Не удалось определить тип файла.")


@dp.message()
async def fallback(message: Message):
    await message.answer("📎 Отправь мне файл, чтобы получить его file_id.")


async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
