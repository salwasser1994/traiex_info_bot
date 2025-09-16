import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command, Text

logging.basicConfig(level=logging.INFO)

# === Конфиг ===
BOT_TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
ADMIN_ID = -1003081706651  # групповой чат для лидов

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище состояния пользователей
user_data = {}

# === Старт ===
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_data[message.from_user.id] = {}
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, хочу узнать! 🚀", callback_data="warmup_yes")],
        [InlineKeyboardButton(text="Нет, просто хочу идеи 💡", callback_data="warmup_no")]
    ])
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я твой финансовый помощник Финансович. 💼\n"
        "Ты когда-нибудь задумывался, как богатые люди заставляют деньги работать на себя?",
        reply_markup=kb
    )

# === Warm-up ===
@dp.callback_query(Text(startswith="warmup_"))
async def warmup_handler(query: CallbackQuery):
    user_data[query.from_user.id]["warmup"] = query.data
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, уже инвестирую 📈", callback_data="experience_yes")],
        [InlineKeyboardButton(text="Нет, хочу начать 🟢", callback_data="experience_no")],
        [InlineKeyboardButton(text="Пробовал, но были неудачи ❌", callback_data="experience_fail")]
    ])
    await query.message.edit_text(
        "Отлично! А у тебя есть опыт инвестирования?",
        reply_markup=kb
    )

# === Опыт инвестирования ===
@dp.callback_query(Text(startswith="experience_"))
async def experience_handler(query: CallbackQuery):
    user_data[query.from_user.id]["experience"] = query.data.replace("experience_", "")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать пассивный доход 💸", callback_data="goal_passive")],
        [InlineKeyboardButton(text="Купить дом 🏠", callback_data="goal_house")],
        [InlineKeyboardButton(text="Купить машину 🚗", callback_data="goal_car")],
        [InlineKeyboardButton(text="Просто приумножить капитал 📊", callback_data="goal_growth")]
    ])
    await query.message.edit_text(
        "Какая твоя главная финансовая цель?",
        reply_markup=kb
    )

# === Финансовая цель ===
@dp.callback_query(Text(startswith="goal_"))
async def goal_handler(query: CallbackQuery):
    goal_map = {
        "goal_passive": "Пассивный доход 💸",
        "goal_house": "Дом 🏠",
        "goal_car": "Машина 🚗",
        "goal_growth": "Приумножить капитал 📊"
    }
    user_data[query.from_user.id]["goal"] = goal_map[query.data]
    
    # Суммы для цели
    if query.data == "goal_passive":
        sums = ["50 000 ₽/мес", "100 000 ₽/мес", "200 000 ₽/мес"]
    elif query.data == "goal_house":
        sums = ["3 000 000 ₽", "5 000 000 ₽", "10 000 000 ₽"]
    elif query.data == "goal_car":
        sums = ["1 000 000 ₽", "2 000 000 ₽", "3 000 000 ₽"]
    else:
        sums = ["100 000 ₽", "200 000 ₽", "500 000 ₽"]

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=s, callback_data=f"sum_{s}")] for s in sums]
    )

    await query.message.edit_text(
        f"Хорошо 👍 Давай уточним.\nСколько денег ты готов вложить для цели «{goal_map[query.data]}»?",
        reply_markup=kb
    )

# === Сумма ===
@dp.callback_query(Text(startswith="sum_"))
async def sum_handler(query: CallbackQuery):
    user_data[query.from_user.id]["sum"] = query.data.replace("sum_", "")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Люблю риск 🚀", callback_data="risk_high")],
        [InlineKeyboardButton(text="Предпочитаю стабильность 🛡️", callback_data="risk_low")],
        [InlineKeyboardButton(text="Комбинирую 🔄", callback_data="risk_medium")]
    ])
    
    await query.message.edit_text(
        "Отлично 👌\nА теперь скажи, как ты относишься к риску?",
        reply_markup=kb
    )

# === Отношение к риску ===
@dp.callback_query(Text(startswith="risk_"))
async def risk_handler(query: CallbackQuery):
    risk_map = {
        "risk_high": "Люблю риск 🚀",
        "risk_low": "Стабильность 🛡️",
        "risk_medium": "Комбинирую 🔄"
    }
    user_data[query.from_user.id]["risk"] = risk_map[query.data]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Связаться с экспертом 👨‍💼", callback_data="contact_expert")]
    ])

    await query.message.edit_text(
        "Отлично! Ты почти готов. Я могу связать тебя с нашим экспертом, "
        "который поможет выбрать лучший путь инвестиций.",
        reply_markup=kb
    )

# === Связь с консультантом ===
@dp.callback_query(Text("contact_expert"))
async def contact_handler(query: CallbackQuery):
    data = user_data.get(query.from_user.id, {})
    await query.message.edit_text(
        "Супер 🎉 Я передал твой запрос нашему консультанту. "
        "В ближайшее время он свяжется с тобой 👨‍💻"
    )

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔥 Новый лид!\n\n"
            f"👤 Пользователь: @{query.from_user.username}\n"
            f"Имя: {query.from_user.full_name}\n"
            f"ID: {query.from_user.id}\n\n"
            f"📌 Опыт инвестирования: {data.get('experience', '—')}\n"
            f"🎯 Цель: {data.get('goal', '—')}\n"
            f"💰 Сумма: {data.get('sum', '—')}\n"
            f"⚡ Риск: {data.get('risk', '—')}\n"
        )
    )

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
