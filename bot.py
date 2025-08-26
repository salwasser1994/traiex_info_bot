import logging
import asyncio
import os
import random
from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
from bs4 import BeautifulSoup
from aiogram.client.bot import Bot as AiogramBot
from aiogram.client.bot import DefaultBotProperties

# Токен из переменной окружения API_Token
API_TOKEN = os.getenv("API_Token")
if not API_TOKEN:
    raise ValueError("API_Token не задан! Установите переменную окружения с токеном.")

logging.basicConfig(level=logging.INFO)

# Инициализация бота с parse_mode через DefaultBotProperties
bot = AiogramBot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher(storage=MemoryStorage())

# Кнопки меню (только именованные аргументы)
button_info = KeyboardButton(text="📈 Информация о крипте")
button_tips = KeyboardButton(text="💡 Инвестиционные советы")
button_motivation = KeyboardButton(text="🔥 Мотивация")
button_faq = KeyboardButton(text="❓ Задать вопрос")
button_profit = KeyboardButton(text="💰 Калькулятор прибыли")
button_news = KeyboardButton(text="📰 Новости крипты")

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [button_info, button_tips],
        [button_motivation, button_faq],
        [button_profit, button_news]
    ],
    resize_keyboard=True
)

# Данные
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

# Для хранения состояний пользователя (калькулятор прибыли)
user_states = {}

# Команда /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я твой крипто-бот 🚀\n"
        "Я помогу тебе узнать о криптовалюте, инвестициях и мотивации.\n"
        "Выбирай одну из опций ниже:",
        reply_markup=main_menu
    )

# Обработка сообщений и кнопок
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Проверяем состояние калькулятора прибыли
    if user_states.get(user_id) == "awaiting_profit_input":
        try:
            parts = [float(x.strip()) for x in text.split(",")]
            if len(parts) != 3:
                raise ValueError
            amount, buy_price, current_price = parts
            profit = (current_price - buy_price) * amount
            await message.answer(f"💰 Ваша прибыль/убыток: {profit:.2f} у.е.")
        except ValueError:
            await message.answer("❌ Неверный формат. Введите три числа через запятую: количество, цена покупки, текущая цена")
        user_states[user_id] = None
        return

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

    elif text == "💰 Калькулятор прибыли":
        await message.answer("Введите три числа через запятую: количество монет, цена покупки, текущая цена.\nПример: 2, 20000, 25000")
        user_states[user_id] = "awaiting_profit_input"

    elif text == "📰 Новости крипты":
        news = await fetch_crypto_news()
        await message.answer(news, disable_web_page_preview=True)

    else:
        answer = faq_answers.get(text)
        if answer:
            await message.answer(answer)
        else:
            await message.answer(
                "Извини, я пока не знаю ответа на этот вопрос 😅\n"
                "Попробуй задать другой вопрос или выбери опцию из меню.",
                reply_markup=main_menu
            )

# Функция получения новостей с CoinTelegraph
async def fetch_crypto_news():
    url = "https://ru.cointelegraph.com/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                articles = soup.find_all("a", class_="post-card-inline__title-link")[:5]
                if not articles:
                    return "Новости сейчас недоступны."
                news_text = "📰 Последние новости крипты:\n\n"
                for a in articles:
                    title = a.get_text(strip=True)
                    link = a["href"]
                    if not link.startswith("http"):
                        link = "https://ru.cointelegraph.com" + link
                    news_text += f"- <a href='{link}'>{title}</a>\n"
                return news_text
    except Exception as e:
        return f"Ошибка при получении новостей: {e}"

# Ежедневная мотивация
async def daily_motivation():
    while True:
        for chat_id in user_states.keys():
            quote = random.choice(motivation_quotes)
            try:
                await bot.send_message(chat_id, f"🔥 Ежедневная мотивация:\n{quote}")
            except:
                pass
        await asyncio.sleep(24 * 60 * 60)  # раз в 24 часа

# Запуск бота
async def main():
    asyncio.create_task(daily_motivation())
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
