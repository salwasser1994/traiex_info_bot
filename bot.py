import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Берём токен из Environment Variables Render
TOKEN = os.getenv("API_Token")
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Главное inline-меню
def main_menu():
    keyboard = [
        [InlineKeyboardButton(text="📝 Пройти тест", callback_data="test")],
        [InlineKeyboardButton(text="💰 Готов инвестировать", callback_data="invest")],
        [InlineKeyboardButton(text="📄 Просмотр договора оферты", callback_data="agreement")],
        [InlineKeyboardButton(text="🤖 Что такое бот на ИИ", callback_data="ai_bot")],
        [InlineKeyboardButton(text="❓ Дополнительные вопросы", callback_data="faq")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# File ID видео
WELCOME_VIDEO_ID = "BAACAgQAAxkDAAIC12i4SwjQT7gKv_ccxLe2dV5GAYreAAIqIQACIJ7IUZCFvYLU5H0KNgQ"

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Отправляем видео с кнопкой "Показать меню"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Показать меню", callback_data="show_menu")]
        ]
    )
    await message.answer_video(
        video=WELCOME_VIDEO_ID,
        caption="🎥 Смотри видео до конца, а затем жми кнопку ниже:",
        reply_markup=keyboard
    )

# Обработка нажатий inline-кнопок
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "show_menu":
        await callback.message.answer("📊 Вот главное меню:", reply_markup=main_menu())
    else:
        await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
