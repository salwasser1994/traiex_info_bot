import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

API_TOKEN = os.getenv("API_TOKEN")  # Токен из Render Environment Variables

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Главное меню ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❓ Задать вопрос")],
        [KeyboardButton(text="📊 Курсы"), KeyboardButton(text="📰 Новости")],
        [KeyboardButton(text="ℹ️ О бирже")]
    ],
    resize_keyboard=True
)

# --- Список ответов на частые вопросы ---
faq = {
    "что такое traiex": "💡 Traiex — это криптовалютная биржа для торговли цифровыми активами.",
    "как зарегистрироваться": "📝 Регистрация доступна на официальном сайте Traiex. Нужно указать почту и придумать пароль.",
    "какие комиссии": "💰 Комиссия за торговые операции составляет 0.1%. Пополнение и вывод зависят от способа.",
    "поддержка": "📞 Связаться с поддержкой можно через email support@traiex.com."
}


# --- Команда /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот Traiex.\n\n"
        "Выберите действие из меню или задайте свой вопрос.",
        reply_markup=main_menu
    )


# --- Обработка вопросов ---
@dp.message()
async def handle_question(message: types.Message):
    text = message.text.lower().strip()

    if text in faq:
        await message.answer(faq[text])
    elif text == "❓ задать вопрос":
        await message.answer("✍ Напишите ваш вопрос, и я постараюсь ответить.")
    elif text == "📊 курсы":
        await message.answer("📈 Курс BTC: 65,000$, ETH: 3,200$ (пример).")
    elif text == "📰 новости":
        await message.answer("📰 Сегодня BTC вырос на 5%, а ETH — на 3%.")
    elif text == "ℹ️ о бирже":
        await message.answer("💡 Traiex — современная криптобиржа с безопасной торговлей.")
    else:
        await message.answer("🤔 Я пока не знаю ответа на этот вопрос. Попробуйте задать по-другому.")


# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
