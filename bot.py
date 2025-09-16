import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# === Конфиг ===
BOT_TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
ADMIN_ID = -1003081706651  # групповой чат для лидов
OFFER_PDF_FILE_ID = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище состояния пользователей
user_data = {}

# === Приветствие и warm-up ===
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

@dp.callback_query(F.data.startswith("warmup_"))
async def warmup_handler(query: CallbackQuery):
    user_data[query.from_user.id]["warmup"] = query.data
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, уже инвестирую 📈", callback_data="experience_yes")],
        [InlineKeyboardButton(text="Нет, хочу начать 🟢", callback_data="experience_no")],
        [InlineKeyboardButton(text="Пробовал, но были неудачи ❌", callback_data="experience_fail")]
    ])
    await query.message.edit_text("Отлично! А у тебя есть опыт инвестирования?", reply_markup=kb)

@dp.callback_query(F.data.startswith("experience_"))
async def experience_handler(query: CallbackQuery):
    user_data[query.from_user.id]["experience"] = query.data.replace("experience_", "")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, дисциплинирован 📊", callback_data="discipline_yes")],
        [InlineKeyboardButton(text="Не совсем дисциплинирован ⚠️", callback_data="discipline_no")]
    ])
    await query.message.edit_text("Ты следишь за своими финансами и инвестициями?", reply_markup=kb)

# === Мини-тест по финансовой грамотности ===
quiz_questions = [
    {"question": "Что такое инвестиционный риск?",
     "options": ["Потеря части или всех вложений", "Гарантированная прибыль", "Беспроигрышная ставка"],
     "correct": 0},
    {"question": "Что такое диверсификация?",
     "options": ["Вложение в разные активы", "Вложение только в акции", "Игнорирование рисков"],
     "correct": 0},
    {"question": "Что обычно сопровождает высокую доходность?",
     "options": ["Высокий риск", "Гарантированный доход", "Малую волатильность"],
     "correct": 0}
]

@dp.callback_query(F.data.startswith("discipline_"))
async def discipline_handler(query: CallbackQuery):
    user_data[query.from_user.id]["discipline"] = query.data.replace("discipline_", "")
    user_data[query.from_user.id]["quiz_index"] = 0
    user_data[query.from_user.id]["quiz_score"] = 0
    await send_quiz_question(query.from_user.id, query.message)

async def send_quiz_question(user_id, message):
    index = user_data[user_id]["quiz_index"]
    q = quiz_questions[index]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=opt, callback_data=f"quiz_{index}_{i}")] for i, opt in enumerate(q["options"])
    ])
    await message.edit_text(f"Вопрос {index+1}:\n{q['question']}", reply_markup=kb)

@dp.callback_query(F.data.startswith("quiz_"))
async def quiz_handler(query: CallbackQuery):
    parts = query.data.split("_")
    q_index, opt_index = int(parts[1]), int(parts[2])
    if opt_index == quiz_questions[q_index]["correct"]:
        user_data[query.from_user.id]["quiz_score"] += 1
    user_data[query.from_user.id]["quiz_index"] += 1
    if user_data[query.from_user.id]["quiz_index"] < len(quiz_questions):
        await send_quiz_question(query.from_user.id, query.message)
    else:
        await query.message.edit_text(
            f"Тест завершен! Ты набрал {user_data[query.from_user.id]['quiz_score']}/"
            f"{len(quiz_questions)} баллов.\n\n"
            "Теперь можно перейти к прогнозу и ознакомлению с офертой."
        )
        # Далее сразу запрос первоначального взноса
        sums_initial = ["10 000 ₽", "20 000 ₽", "30 000 ₽", "40 000 ₽", "50 000 ₽",
                        "100 000 ₽", "250 000 ₽", "500 000 ₽", "1 000 000 ₽"]
        keyboard_rows = []
        for i in range(0, len(sums_initial), 3):
            row = [InlineKeyboardButton(text=s, callback_data=f"initial_{s}") for s in sums_initial[i:i+3]]
            keyboard_rows.append(row)
        kb_initial = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
        await query.message.answer("Сколько денег ты готов вложить первоначально?", reply_markup=kb_initial)

# === Первоначальный взнос ===
@dp.callback_query(F.data.startswith("initial_"))
async def initial_handler(query: CallbackQuery):
    user_data[query.from_user.id]["initial_sum"] = query.data.replace("initial_", "")
    sums_monthly = ["0 ₽", "10 000 ₽", "20 000 ₽", "30 000 ₽", "40 000 ₽", "50 000 ₽", "100 000 ₽"]
    keyboard_rows = []
    for i in range(0, len(sums_monthly), 3):
        row = [InlineKeyboardButton(text=s, callback_data=f"sum_{s}") for s in sums_monthly[i:i+3]]
        keyboard_rows.append(row)
    kb_monthly = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await query.message.edit_text("Сколько денег ты готов вкладывать каждый месяц?", reply_markup=kb_monthly)

# === Сумма ежемесячного вложения и прогноз ===
@dp.callback_query(F.data.startswith("sum_"))
async def sum_handler(query: CallbackQuery):
    user_data[query.from_user.id]["sum"] = query.data.replace("sum_", "")
    initial_sum = int(user_data[query.from_user.id]["initial_sum"].replace("₽","").replace(" ",""))
    monthly_invest = int(user_data[query.from_user.id]["sum"].replace("₽","").replace(" ",""))
    rate = 0.09
    periods = [1,3,6,12,24]  # месяцы для прогноза

    balance = 0
    forecast_text = f"💡 Прогноз Trading Bot при первоначальном взносе {initial_sum:,} ₽ и ежемесячном вложении {monthly_invest:,} ₽ (9%/мес)\n\n"

    for month in range(1, max(periods)+1):
        # Вложение текущего месяца
        if month == 1:
            invested_this_month = initial_sum
        else:
            invested_this_month = monthly_invest
        balance += invested_this_month

        # Пассивный доход за месяц
        passive_income = int(balance * rate)
        balance += passive_income

        if month in periods:
            forecast_text += (f"Месяц {month}\n"
                              f"💵 Вложение в этом месяце: {invested_this_month:,} ₽\n"
                              f"Пассивный доход: {passive_income:,} ₽ (9%)\n"
                              f"Баланс: {balance:,} ₽\n\n")

    # Предложение ознакомиться с офертой
    kb_offer = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ознакомиться с офертой 📄", callback_data="offer_read")]
    ])
    await query.message.edit_text(forecast_text, reply_markup=kb_offer)

# === Ознакомление с офертой ===
@dp.callback_query(F.data=="offer_read")
async def offer_handler(query: CallbackQuery):
    await bot.send_document(chat_id=query.from_user.id, document=OFFER_PDF_FILE_ID)
    kb_accept = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я согласен с офертой ✅", callback_data="offer_accept")]
    ])
    await query.message.answer("Прочитайте оферту и подтвердите согласие:", reply_markup=kb_accept)

# === Подтверждение оферты и связь с экспертом ===
@dp.callback_query(F.data=="offer_accept")
async def offer_accept_handler(query: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Связаться с экспертом 👨‍💼", callback_data="contact_expert")]
    ])
    await query.message.answer("Спасибо! Теперь ты можешь оставить заявку.", reply_markup=kb)

@dp.callback_query(F.data=="contact_expert")
async def contact_handler(query: CallbackQuery):
    data = user_data.get(query.from_user.id, {})
    await query.message.answer("Супер 🎉 Я передал твой запрос нашему консультанту. В ближайшее время он свяжется с тобой 👨‍💻")
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(f"🔥 Новый лид!\n\n"
              f"👤 Пользователь: @{query.from_user.username}\n"
              f"Имя: {query.from_user.full_name}\n"
              f"ID: {query.from_user.id}\n\n"
              f"📌 Опыт инвестирования: {data.get('experience','—')}\n"
              f"💰 Первоначальный взнос: {data.get('initial_sum','—')}\n"
              f"💵 Ежемесячные вложения: {data.get('sum','—')}\n")
    )

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
