import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Берём токен из Environment Variables
TOKEN = os.getenv("API_Token")
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start — приветствие
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Пришли любой файл, и я сразу дам его file_id.")

# Обработка любого файла
@dp.message()
async def handle_file(message: types.Message):
    if message.document:
        await message.answer(f"Вот file_id твоего файла:\n\n{message.document.file_id}")
    else:
        await message.answer("Отправь любой файл.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
