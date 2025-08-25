import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

API_TOKEN = os.getenv("API_TOKEN")  # токен подтягивается из переменной окружения

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# === Кнопки выбора языка ===
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")]
    ],
    resize_keyboard=True
)

# === Главное меню на русском ===
main_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Курсы"), KeyboardButton(text="📰 Новости")],
        [KeyboardButton(text="ℹ️ О бирже"), KeyboardButton(text="🌐 Website")],
    ],
    resize_keyboard=True
)

# === Главное меню на английском ===
main_menu_en = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Rates"), KeyboardButton(text="📰 News")],
        [KeyboardButton(text="ℹ️ About Exchange"), KeyboardButton(text="🌐 Website")],
    ],
    resize_keyboard=True
)


# === Хранилище выбора языка пользователей ===
user_language = {}


# === Хэндлер /start ===
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Welcome! / Добро пожаловать!\n\n"
        "Пожалуйста, выберите язык / Please select your language:",
        reply_markup=language_keyboard
    )


# === Хэндлер выбора языка ===
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if message.text == "🇷🇺 Русский":
        user_language[user_id] = "ru"
        await message.answer("✅ Язык установлен: Русский", reply_markup=main_menu_ru)

    elif message.text == "🇬🇧 English":
        user_language[user_id] = "en"
        await message.answer("✅ Language set: English", reply_markup=main_menu_en)

    else:
        lang = user_language.get(user_id, "ru")
        if lang == "ru":
            await message.answer("Выберите опцию из меню 👇", reply_markup=main_menu_ru)
        else:
            await message.answer("Choose an option from the menu 👇", reply_markup=main_menu_en)


# === Запуск бота ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
