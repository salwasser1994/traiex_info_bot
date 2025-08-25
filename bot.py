import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

API_TOKEN = os.getenv("API_TOKEN")  # Твой токен от BotFather

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Вопрос и варианты ---
question = "Считаете ли вы, что понимаете свой мир целиком, как это делают богатые и успешные люди?"
options = ["Да, я всё вижу и понимаю", "Нет, о чём вы говорите?", "Мой вариант ответа"]

# --- Кнопки для опроса ---
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=opt, callback_data=f"vote_{i}")] for i, opt in enumerate(options)
    ]
)

# --- /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Давай проведем опрос:", reply_markup=None)
    await message.answer(question, reply_markup=keyboard)

# --- Обработка голосов ---
@dp.callback_query()
async def handle_vote(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])
    selected_option = options[index]
    await callback.answer(f"Вы выбрали: {selected_option}", show_alert=True)

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
