import os
import asyncio
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- Токены ---
API_TOKEN = os.getenv("API_TOKEN")              # Telegram Bot
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")    # OpenAI GPT-4
openai.api_key = OPENAI_API_KEY

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Главное меню ---
main_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Курсы"), KeyboardButton(text="📰 Новости")],
        [KeyboardButton(text="ℹ️ О бирже"), KeyboardButton(text="❓ Задать вопрос")]
    ],
    resize_keyboard=True
)

main_menu_en = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Rates"), KeyboardButton(text="📰 News")],
        [KeyboardButton(text="ℹ️ About Exchange"), KeyboardButton(text="❓ Ask a question")]
    ],
    resize_keyboard=True
)

# --- Язык пользователя ---
user_language = {}

# --- /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    lang_menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")]],
        resize_keyboard=True
    )
    await message.answer("🌐 Выберите язык / Choose your language:", reply_markup=lang_menu)

# --- Выбор языка и обработка кнопок ---
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Выбор языка
    if text == "🇷🇺 Русский":
        user_language[user_id] = "ru"
        await message.answer("✅ Язык установлен: Русский", reply_markup=main_menu_ru)
        return
    elif text == "🇬🇧 English":
        user_language[user_id] = "en"
        await message.answer("✅ Language set: English", reply_markup=main_menu_en)
        return

    # Определяем язык для меню
    lang = user_language.get(user_id, "ru")
    menu = main_menu_ru if lang == "ru" else main_menu_en

    # Кнопки меню
    if text in ["📊 Курсы", "📊 Rates"]:
        await message.answer("📈 BTC: 65,000 $ | ETH: 3,500 $", reply_markup=menu)
    elif text in ["📰 Новости", "📰 News"]:
        await message.answer("📰 Последние новости Traiex...", reply_markup=menu)
    elif text in ["ℹ️ О бирже", "ℹ️ About Exchange"]:
        await message.answer("💡 Traiex — современная криптобиржа", reply_markup=menu)
    elif text in ["❓ Задать вопрос", "❓ Ask a question"]:
        await message.answer("✍ Напишите ваш вопрос, и я отвечу с помощью AI!", reply_markup=menu)
    else:
        # --- AI ответ через OpenAI GPT-4 (новый API) ---
        try:
            await message.answer("🤖 Думаю...", reply_markup=menu)
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ты помощник по бирже Traiex."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=250
            )
            answer = response.choices[0].message.content.strip()
            await message.answer(answer, reply_markup=menu)
        except Exception as e:
            await message.answer(f"❌ Ошибка AI: {e}", reply_markup=menu)

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
