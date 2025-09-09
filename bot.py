import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("getid"))
async def get_id(message: Message):
    await message.answer(f"Chat ID: {message.chat.id}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
