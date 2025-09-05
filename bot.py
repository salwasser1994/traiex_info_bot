import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Берём токен из Environment Variables Render
TOKEN = os.getenv("API_Token")
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

# Создаем бота с default properties
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Главное меню (ReplyKeyboard, 2 кнопки в ряд)
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="🤖 Что такое бот на ИИ"), KeyboardButton(text="❓ Дополнительные вопросы")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Кнопка "В меню"
def back_to_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В меню")]],
        resize_keyboard=True
    )

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(
        video=file_id,
        caption="Вот видео с общей картиной 📊",
        reply_markup=back_to_menu()
    )

# Обработка кнопок
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "В меню":
        await message.answer("Выберите пункт меню:", reply_markup=main_menu())
    else:
        await message.answer(f"Вы нажали: {message.text}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
