import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Словарь для хранения выбранного языка пользователей ---
user_language = {}

# --- Клавиатура выбора языка ---
lang_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")]
    ],
    resize_keyboard=True
)

# --- Главное меню на русском ---
main_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📊 Курсы"), KeyboardButton("📰 Новости")],
        [KeyboardButton("❓ FAQ"), KeyboardButton("📞 Поддержка")],
        [KeyboardButton("💡 Советы"), KeyboardButton("📅 События")]
    ],
    resize_keyboard=True
)

# --- Главное меню на английском ---
main_menu_en = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📊 Rates"), KeyboardButton("📰 News")],
        [KeyboardButton("❓ FAQ"), KeyboardButton("📞 Support")],
        [KeyboardButton("💡 Tips"), KeyboardButton("📅 Events")]
    ],
    resize_keyboard=True
)

# --- /start ---
@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🌐 Выберите язык / Choose your language:", reply_markup=lang_menu)

# --- Выбор языка ---
@dp.message(F.text == "🇷🇺 Русский")
async def set_russian(message: Message):
    user_language[message.from_user.id] = "ru"
    await message.answer("Выбран русский язык 🇷🇺", reply_markup=main_menu_ru)

@dp.message(F.text == "🇬🇧 English")
async def set_english(message: Message):
    user_language[message.from_user.id] = "en"
    await message.answer("English selected 🇬🇧", reply_markup=main_menu_en)

# --- Обработчики кнопок на русском ---
@dp.message(F.text == "📊 Курсы")
async def rates_ru(message: Message):
    if user_language.get(message.from_user.id) == "ru":
        await message.answer("📊 Текущие курсы Traiex:\nBTC/USDT: 65,000 $\nETH/USDT: 3,500 $")

@dp.message(F.text == "📰 Новости")
async def news_ru(message: Message):
    if user_language.get(message.from_user.id) == "ru":
        await message.answer("📰 Последние новости Traiex:\n- Новая акция\n- Снижение комиссий")

@dp.message(F.text == "❓ FAQ")
async def faq_ru(message: Message):
    if user_language.get(message.from_user.id) == "ru":
        await message.answer("❓ FAQ:\n1. Как зарегистрироваться?\n2. Пополнение счёта\n3. Поддержка")

@dp.message(F.text == "📞 Поддержка")
async def support_ru(message: Message):
    if user_language.get(message.from_user.id) == "ru":
        await message.answer("📞 Связь с поддержкой: support@traiex.com\nTelegram: @TraiexSupport")

@dp.message(F.text == "💡 Советы")
async def tips_ru(message: Message):
    if user_language.get(message.from_user.id) == "ru":
        await message.answer("💡 Советы трейдерам:\n- Следи за курсами\n- Не рискуй больше, чем можешь позволить")

@dp.message(F.text == "📅 События")
async def events_ru(message: Message):
    if user_language.get(message.from_user.id) == "ru":
        await message.answer("📅 Ближайшие события:\n- Вебинар: 28 августа\n- Конкурс: 1 сентября")

# --- Обработчики кнопок на английском ---
@dp.message(F.text == "📊 Rates")
async def rates_en(message: Message):
    if user_language.get(message.from_user.id) == "en":
        await message.answer("📊 Current Traiex rates:\nBTC/USDT: 65,000 $\nETH/USDT: 3,500 $")

@dp.message(F.text == "📰 News")
async def news_en(message: Message):
    if user_language.get(message.from_user.id) == "en":
        await message.answer("📰 Latest Traiex news:\n- New promotion\n- Fees reduced to 0.1%")

@dp.message(F.text == "💡 Tips")
async def tips_en(message: Message):
    if user_language.get(message.from_user.id) == "en":
        await message.answer("💡 Tips for traders:\n- Watch rates\n- Don't risk too much\n- Use stop-losses")

@dp.message(F.text == "📅 Events")
async def events_en(message: Message):
    if user_language.get(message.from_user.id) == "en":
        await message.answer("📅 Upcoming events:\n- Webinar: Aug 28\n- Trading contest: Sep 1")

@dp.message(F.text == "❓ FAQ")
async def faq_en(message: Message):
    if user_language.get(message.from_user.id) == "en":
        await message.answer("❓ FAQ:\n1. How to register?\n2. How to deposit?\n3. Support")

@dp.message(F.text == "📞 Support")
async def support_en(message: Message):
    if user_language.get(message.from_user.id) == "en":
        await message.answer("📞 Contact support: support@traiex.com\nTelegram: @TraiexSupport")

# --- fallback ---
@dp.message()
async def fallback(message: Message):
    lang = user_language.get(message.from_user.id, "ru")
    if lang == "ru":
        await message.answer("🤔 Я тебя не понял. Выбери раздел в меню 👇", reply_markup=main_menu_ru)
    else:
        await message.answer("🤔 I didn't understand. Choose a section 👇", reply_markup=main_menu_en)

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
