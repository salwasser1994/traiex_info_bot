import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

TOKEN = os.getenv("API_Token")
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Кнопка под видео
def show_menu_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="«Показать меню»", callback_data="show_menu")]
        ]
    )

# Главное меню (только в клавиатуре снизу)
def reply_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Пройти тест")],
            [KeyboardButton(text="💰 Готов инвестировать")],
            [KeyboardButton(text="📄 Просмотр договора оферты")],
            [KeyboardButton(text="🤖 Что такое бот на ИИ")],
            [KeyboardButton(text="❓ Дополнительные вопросы")]
        ],
        resize_keyboard=True
    )

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    video_file_id = "BAACAgQAAxkDAAIC12i4SwjQT7gKv_ccxLe2dV5GAYreAAIqIQACIJ7IUZCFvYLU5H0KNgQ"
    await message.answer_video(
        video=video_file_id,
        caption="Посмотрите видео, а затем нажмите кнопку ниже:",
        reply_markup=show_menu_button()
    )

# Обработка inline-кнопки "Показать меню"
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "show_menu":
        await callback.message.answer("Меню открыто ✅", reply_markup=reply_main_menu())
        await callback.message.delete()  # удаляем сообщение с кнопкой под видео
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
