import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Прямое использование токена (только для локального теста, не в GitHub)
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start — приветствие
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Пришли любой файл или фото, и я сразу дам его file_id.")

# Обработка любого файла или фото
@dp.message()
async def handle_file(message: types.Message):
    if message.document:  # любой файл
        await message.answer(f"Вот file_id твоего файла:\n\n{message.document.file_id}")
    elif message.photo:  # фото
        # Берем максимальное качество (последний в списке)
        photo = message.photo[-1]
        await message.answer(f"Вот file_id твоего фото:\n\n{photo.file_id}")
    else:
        await message.answer("Отправь любой файл или фото.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
