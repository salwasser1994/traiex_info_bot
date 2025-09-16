import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

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
@dp.callback_query(F.data.startswith("warmup_"))
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
@dp.callback_query(F.data.startswith("experience_"))
async def experience_handler(query: CallbackQuery):
    user_data[query.from_user.id]["experience"] = query.data.replace("experience_", "")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать пассивный доход 💸", callback_data="goal_passive"),
         InlineKeyboardButton(text="Купить дом 🏠", callback_data="goal_house")],
        [InlineKeyboardButton(text="Купить машину 🚗", callback_data="goal_car"),
         InlineKeyboardButton(text="Просто приумножить капитал 📊", callback_data="goal_growth")]
    ])
    await query.message.edit_text(
        "Какая твоя главная финансовая цель?",
        reply_markup=kb
    )

# === Финансовая цель ===
@dp.callback_query(F.data.startswith("goal_"))
async def goal_handler(query: CallbackQuery):
    goal_map = {
        "goal_passive": "Пассивный доход 💸",
        "goal_house": "Дом 🏠",
        "goal_car": "Машина 🚗",
        "goal_growth": "Приумножить капитал 📊"
    }
    user_data[query.from_user.id]["goal"] = goal_map[query.data]

    # Первый вопрос — первоначальный взнос
    sums_initial = ["10 000 ₽", "20 000 ₽", "30 000 ₽", "40 000 ₽", "50 000 ₽", "100 000 ₽", "250 000 ₽", "500 000 ₽", "1 000 000 ₽"]
    kb_initial = InlineKeyboardMarkup(inline_keyboard=[
        sums_initial[i:i+3] for i in range(0, len(sums_initial), 3)
    ])
    # Конвертируем в кнопки
    for row in kb_initial.inline_keyboard:
        for idx, val in enumerate(row):
            row[idx] = InlineKeyboardButton(text=val, callback_data=f"initial_{val}")

    await query.message.edit_text(
        f"Сколько денег ты готов вложить первоначально для цели «{goal_map[query.data]}»?",
        reply_markup=kb_initial
    )

# === Первоначальный взнос ===
@dp.callback_query(F.data.startswith("initial_"))
async def initial_handler(query: CallbackQuery):
    user_data[query.from_user.id]["initial_sum"] = query.data.replace("initial_", "")

    # Второй вопрос — ежемесячное вложение
    sums_monthly = ["0 ₽", "10 000 ₽", "20 000 ₽", "30 000 ₽", "40 000 ₽", "50 000 ₽", "100 000 ₽"]
    kb_monthly = InlineKeyboardMarkup(inline_keyboard=[
        sums_monthly[i:i+3] for i in range(0, len(sums_monthly), 3)
    ])
    for row in kb_monthly.inline_keyboard:
        for idx, val in enumerate(row):
            row[idx] = InlineKeyboardButton(text=val, callback_data=f"sum_{val}")

    await query.message.edit_text(
        "Сколько денег ты готов вкладывать каждый месяц для цели?",
        reply_markup=kb_monthly
    )

# === Сумма ежемесячного вложения и расчет Trading Bot с прогресс-баром ===
@dp.callback_query(F.data.startswith("sum_"))
async def sum_handler(query: CallbackQuery):
    user_data[query.from_user.id]["sum"] = query.data.replace("sum_", "")

    initial_str = user_data[query.from_user.id]["initial_sum"].replace("₽", "").replace(" ", "")
    monthly_str = query.data.replace("sum_", "").replace("₽", "").replace(" ", "")
    initial_sum = int(initial_str) if initial_str.isdigit() else 0
    monthly_invest = int(monthly_str) if monthly_str.isdigit() else 0

    rate = 0.09
    months_to_show = [4, 6, 12, 24]

    balance = initial_sum
    invested_total = initial_sum
    forecast_text = f"💡 Прогноз Trading Bot при первоначальном взносе {initial_sum:,} ₽ и ежемесячном вложении {monthly_invest:,} ₽ (средняя доходность 9%/мес)\n\n"

    for month in range(1, max(months_to_show)+1):
        balance = balance * (1 + rate) + monthly_invest
        invested_total += monthly_invest
        passive_income = balance - invested_total
        if month in months_to_show:
            bar_length = 10
            percent = min(int(passive_income / max(1, invested_total) * bar_length), bar_length)
            bar = "🟩" * percent + "⬜" * (bar_length - percent)
            forecast_text += (
                f"📅 Через {month} мес:\n"
                f"  Вложено: {invested_total:,} ₽\n"
                f"  Пассивный доход: {int(passive_income):,} ₽ {bar}\n"
                f"  Баланс: {int(balance):,} ₽\n\n"
            )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Люблю риск 🚀", callback_data="risk_high"),
         InlineKeyboardButton(text="Предпочитаю стабильность 🛡️", callback_data="risk_low"),
         InlineKeyboardButton(text="Комбинирую 🔄", callback_data="risk_medium")]
    ])

    await query.message.edit_text(
        forecast_text + "Теперь выбери, как ты относишься к риску:",
        reply_markup=kb
    )

# === Отношение к риску ===
@dp.callback_query(F.data.startswith("risk_"))
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
        "Отлично! Ты почти готов. Я могу связать тебя с нашим экспертом, который поможет выбрать лучший путь инвестиций.",
        reply_markup=kb
    )

# === Связь с консультантом ===
@dp.callback_query(F.data == "contact_expert")
async def contact_handler(query: CallbackQuery):
    data = user_data.get(query.from_user.id, {})
    await query.message.edit_text(
        "Супер 🎉 Я передал твой запрос нашему консультанту. В ближайшее время он свяжется с тобой 👨‍💻"
    )
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(f"🔥 Новый лид!\n\n"
              f"👤 Пользователь: @{query.from_user.username}\n"
              f"Имя: {query.from_user.full_name}\n"
              f"ID: {query.from_user.id}\n\n"
              f"📌 Опыт инвестирования: {data.get('experience', '—')}\n"
              f"🎯 Цель: {data.get('goal', '—')}\n"
              f"💰 Первоначальный взнос: {data.get('initial_sum', '—')}\n"
              f"💵 Ежемесячные вложения: {data.get('sum', '—')}\n"
              f"⚡ Риск: {data.get('risk', '—')}\n")
    )

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
