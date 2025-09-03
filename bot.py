import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен из Environment Variables Render
TOKEN = os.getenv("API_Token")
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

# Создаем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
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

# Отправка меню сразу, без приветственного текста
@dp.message()
async def send_menu(message: types.Message):
    await message.answer(reply_markup=main_menu())

# Пока кнопки без действия
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    await callback.answer()  # просто подтверждение нажатия

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
