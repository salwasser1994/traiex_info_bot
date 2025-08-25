import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

# --- Подключение токена через переменную окружения ---
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Главное меню (aiogram 3.x) ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Курсы"), KeyboardButton(text="📰 Новости")],
        [KeyboardButton(text="❓ FAQ"), KeyboardButton(text="📞 Поддержка")]
    ],
    resize_keyboard=True
)

# --- Обработчики команд ---
@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "👋 Привет! Я информационный бот биржи Traiex.\nВыбери раздел в меню ниже 👇",
        reply_markup=main_menu
    )

@dp.message(F.text == "📊 Курсы")
async def rates(message: Message):
    await message.answer(
        "📊 Текущие курсы Traiex:\nBTC/USDT: 65,000 $\nETH/USDT: 3,500 $"
    )

@dp.message(F.text == "📰 Новости")
async def news(message: Message):
    await message.answer(
        "📰 Последние новости Traiex:\n- Новая акция для трейдеров!\n- Снижение комиссий до 0.1%."
    )

@dp.message(F.text == "❓ FAQ")
async def faq(message: Message):
    await message.answer(
        "❓ FAQ:\n1. Как зарегистрироваться?\n2. Как пополнить счёт?\n3. Поддержка"
    )

@dp.message(F.text == "📞 Поддержка")
async def support(message: Message):
    await message.answer(
        "📞 Связаться с поддержкой: support@traiex.com\nTelegram: @TraiexSupport"
    )

@dp.message()
async def fallback(message: Message):
    await message.answer(
        "🤔 Я тебя не понял. Выбери раздел в меню 👇",
        reply_markup=main_menu
    )

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
