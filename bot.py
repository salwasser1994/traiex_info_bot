import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
import asyncio

# --- Проверка токена ---
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError(
        "❌ API_TOKEN не найден! "
        "Проверьте Environment Variables на Render. "
        "KEY должно быть 'API_TOKEN', VALUE — токен от BotFather."
    )

# --- Инициализация бота ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Главное меню ---
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📊 Курсы"))
main_menu.add(KeyboardButton("📰 Новости"))
main_menu.add(KeyboardButton("❓ FAQ"))
main_menu.add(KeyboardButton("📞 Поддержка"))

# --- Обработчики ---
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
