import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import random

API_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

# Кнопки меню
button_info = KeyboardButton("📈 Информация о крипте")
button_tips = KeyboardButton("💡 Инвестиционные советы")
button_motivation = KeyboardButton("🔥 Мотивация")
button_faq = KeyboardButton("❓ Задать вопрос")
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [button_info, button_tips],
        [button_motivation, button_faq]
    ],
    resize_keyboard=True
)

# Примеры данных
crypto_info = {
    "Bitcoin": "Bitcoin — первая криптовалюта, созданная в 2009 году. BTC ограничен 21 млн монет.",
    "Ethereum": "Ethereum — платформа для смарт-контрактов и криптовалюта ETH.",
    "Altcoins": "Altcoins — все криптовалюты, кроме Bitcoin. Например, Litecoin, Cardano, Solana."
}

investment_tips = [
    "Не инвестируй больше, чем готов потерять.",
    "Диверсифицируй портфель, не держи всё в одной монете.",
    "Изучи проект перед инвестированием: команда, цель, технология.",
    "Следи за новостями и трендами рынка криптовалют."
]

motivation_quotes = [
    "Кто рискует — тот выигрывает. Начни инвестировать в крипту сегодня!",
    "Лучшее время для инвестиций было вчера, второе лучшее — сейчас.",
    "Постоянство и знания создают богатство.",
    "Не бойся маленьких шагов — они приводят к большим результатам."
]

faq_answers = {
    "Что такое криптовалюта?": "Криптовалюта — это цифровая валюта, основанная на технологии блокчейн.",
    "Как начать инвестировать?": "Для начала выбери надёжную биржу, создай кошелёк и инвестируй небольшие суммы.",
    "Какая крипта самая надёжная?": "Bitcoin и Ethereum считаются наиболее надёжными и популярными."
}

# Обработчики команд
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я твой крипто-бот 🚀\n"
        "Я помогу тебе узнать о криптовалюте и инвестициях.\n"
        "Выбирай одну из опций ниже:",
        reply_markup=main_menu
    )

# Обработчик кнопок
@dp.message()
async def handle_message(message: types.Message):
    text = message.text

    if text == "📈 Информация о крипте":
        info_text = "\n\n".join([f"<b>{k}</b>: {v}" for k, v in crypto_info.items()])
        await message.answer(info_text)

    elif text == "💡 Инвестиционные советы":
        tip = random.choice(investment_tips)
        await message.answer(f"💡 Совет:\n{tip}")

    elif text == "🔥 Мотивация":
        quote = random.choice(motivation_quotes)
        await message.answer(f"🔥 Мотивация:\n{quote}")

    elif text == "❓ Задать вопрос":
        await message.answer("Напиши свой вопрос про крипту, и я постараюсь помочь!")

    else:
        # Проверяем FAQ
        answer = faq_answers.get(text)
        if answer:
            await message.answer(answer)
        else:
            await message.answer(
                "Извини, я пока не знаю ответа на этот вопрос 😅\n"
                "Попробуй задать другой вопрос или выбери опцию из меню.",
                reply_markup=main_menu
            )

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
