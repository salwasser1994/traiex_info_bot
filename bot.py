import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Берём токен прямо из Environment Render
TOKEN = os.getenv("API_Token")  # ключ в Render: API_Token

# Проверка токена
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

# Создаем бота и диспетчер
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Главное меню
def main_menu():
    keyboard = [
        [InlineKeyboardButton(text="📊 Общая картина", callback_data="overview")],
        [InlineKeyboardButton(text="📝 Пройти тест", callback_data="test")],
        [InlineKeyboardButton(text="💰 Готов инвестировать", callback_data="invest")],
        [InlineKeyboardButton(text="📄 Просмотр договора оферты", callback_data="agreement")],
        [InlineKeyboardButton(text="🤖 Что такое бот на ИИ", callback_data="ai_bot")],
        [InlineKeyboardButton(text="❓ Дополнительные вопросы", callback_data="faq")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Выбирай нужный пункт меню:", reply_markup=main_menu())

# Пока кнопки без действия
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    await callback.answer()  # подтверждение нажатия

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
