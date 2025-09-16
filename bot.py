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

# === Вопросы финансовой грамотности ===
quiz_questions = [
    {"question": "Что такое пассивный доход?", "options": ["Доход без активной работы", "Зарплата", "Случайные деньги"], "correct": 0},
    {"question": "Что такое диверсификация?", "options": ["Разные активы", "Только акции", "Не инвестировать"], "correct": 0},
    {"question": "Что сопровождает высокую доходность?", "options": ["Высокий риск", "Гарантированная прибыль", "Нет риска"], "correct": 0},
    {"question": "Что такое инвестиционный риск?", "options": ["Потеря вложений", "Гарантированный доход", "Малый риск"], "correct": 0},
    {"question": "Что такое ликвидность?", "options": ["Способность быстро продать актив", "Пассивный доход", "Высокая доходность"], "correct": 0},
    {"question": "Что такое сложный процент?", "options": ["Проценты на проценты", "Проценты на взнос один раз", "Процентная ставка без дохода"], "correct": 0},
    {"question": "Что такое фондовый рынок?", "options": ["Рынок акций и облигаций", "Банк", "Только криптовалюты"], "correct": 0},
    {"question": "Что такое инфляция?", "options": ["Рост цен", "Снижение цен", "Стабильность цен"], "correct": 0},
    {"question": "Что такое кредитное плечо?", "options": ["Заемные деньги для инвестиций", "Личные деньги", "Доход без риска"], "correct": 0},
    {"question": "Что такое портфель инвестиций?", "options": ["Совокупность активов", "Один актив", "Банковский счет"], "correct": 0},
]

# === Старт ===
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_data[message.from_user.id] = {
        "username": message.from_user.username or "—",
        "full_name": message.from_user.full_name or "—"
    }
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, хочу пройти опрос! 🚀", callback_data="start_quiz")],
        [InlineKeyboardButton(text="Просто посмотреть идеи 💡", callback_data="skip_quiz")]
    ])
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "💡 Мы хотим узнать твой уровень финансовой грамотности, чтобы максимально помочь тебе.\n"
        "После прохождения опроса ты получишь доступ к:\n"
        "• Полезной информации и секретам успеха\n"
        "• Связи с личным помощником (реальным человеком)\n"
        "• Приватной группе единомышленников, интересующихся финансами\n\n"
        "Готов начать?",
        reply_markup=kb
    )

# === Начало опроса ===
@dp.callback_query(F.data=="start_quiz")
async def start_quiz_handler(query: CallbackQuery):
    user_data[query.from_user.id]["quiz_index"] = 0
    user_data[query.from_user.id]["quiz_score"] = 0
    await send_quiz_question(query.from_user.id, query.message)

async def send_quiz_question(user_id, message):
    index = user_data[user_id]["quiz_index"]
    q = quiz_questions[index]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=opt, callback_data=f"quiz_{index}_{i}")] for i, opt in enumerate(q["options"])
    ])
    await message.edit_text(f"{q['question']}", reply_markup=kb)

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
        # После опроса идём к выбору цели
        kb_goals = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Создать пассивный доход 💸", callback_data="goal_passive"),
             InlineKeyboardButton(text="Купить дом 🏠", callback_data="goal_house"),
             InlineKeyboardButton(text="Купить машину 🚗", callback_data="goal_car"),
             InlineKeyboardButton(text="Просто приумножить капитал 📊", callback_data="goal_growth")]
        ])
        await query.message.edit_text(
            "Отлично! Теперь выбери свою финансовую цель:", reply_markup=kb_goals
        )

# === Выбор цели ===
@dp.callback_query(F.data.startswith("goal_"))
async def goal_handler(query: CallbackQuery):
    goal_map = {
        "goal_passive": "Пассивный доход 💸",
        "goal_house": "Дом 🏠",
        "goal_car": "Машина 🚗",
        "goal_growth": "Приумножить капитал 📊"
    }
    user_data[query.from_user.id]["goal"] = goal_map[query.data]
    # Первоначальный взнос
    sums_initial = ["10 000 ₽","20 000 ₽","30 000 ₽","40 000 ₽","50 000 ₽","100 000 ₽","250 000 ₽","500 000 ₽","1 000 000 ₽"]
    keyboard_rows = []
    for i in range(0, len(sums_initial), 3):
        row = [InlineKeyboardButton(text=s, callback_data=f"initial_{s}") for s in sums_initial[i:i+3]]
        keyboard_rows.append(row)
    kb_initial = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await query.message.edit_text("Сколько денег вы готовы вложить первоначально?", reply_markup=kb_initial)

# === Первоначальный взнос ===
@dp.callback_query(F.data.startswith("initial_"))
async def initial_handler(query: CallbackQuery):
    user_data[query.from_user.id]["initial_sum"] = query.data.replace("initial_", "")
    sums_monthly = ["0 ₽","10 000 ₽","20 000 ₽","30 000 ₽","40 000 ₽","50 000 ₽","100 000 ₽"]
    keyboard_rows = []
    for i in range(0, len(sums_monthly), 3):
        row = [InlineKeyboardButton(text=s, callback_data=f"sum_{s}") for s in sums_monthly[i:i+3]]
        keyboard_rows.append(row)
    kb_monthly = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await query.message.edit_text("Сколько денег вы готовы вкладывать каждый месяц?", reply_markup=kb_monthly)

# === Расчет пассивного дохода ===
@dp.callback_query(F.data.startswith("sum_"))
async def sum_handler(query: CallbackQuery):
    user_data[query.from_user.id]["sum"] = query.data.replace("sum_","")
    initial = int(user_data[query.from_user.id]["initial_sum"].replace("₽","").replace(" ",""))
    monthly = int(user_data[query.from_user.id]["sum"].replace("₽","").replace(" ",""))
    rate = 0.09
    periods = [1,3,6,12,24]
    balance = 0
    forecast_text = ""
    for month in periods:
        invest_this_month = initial if month==1 else monthly
        balance += invest_this_month
        passive = balance*rate
        balance += passive
        forecast_text += f"📅 Месяц {month}\n💵 Вложение в этом месяце: {invest_this_month:,} ₽\n"
        forecast_text += f"Пассивный доход: {int(passive):,} ₽ (9%)\nБаланс: {int(balance):,} ₽\n\n"
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

# === Согласие и выбор контакта ===
@dp.callback_query(F.data=="offer_accept")
async def offer_accept_handler(query: CallbackQuery):
    kb_contact = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Telegram", callback_data="contact_telegram"),
         InlineKeyboardButton(text="Email", callback_data="contact_email")],
        [InlineKeyboardButton(text="Телефон", callback_data="contact_phone"),
         InlineKeyboardButton(text="Другое", callback_data="contact_other")]
    ])
    await query.message.answer("Выберите удобный способ связи с личным помощником:", reply_markup=kb_contact)

@dp.callback_query(F.data.startswith("contact_"))
async def contact_method_handler(query: CallbackQuery):
    method = query.data.replace("contact_","")
    user_data[query.from_user.id]["contact_method"] = method
    if method=="telegram":
        username = user_data[query.from_user.id].get("username","—")
        if username=="—":
            await query.message.answer("У вас нет публичного username в Telegram. Напишите другой способ связи.")
        else:
            user_data[query.from_user.id]["contact"] = f"@{username}"
            await send_to_admin(query.from_user.id)
            await query.message.answer("Отлично! Ваш запрос передан консультанту.")
    else:
        await query.message.answer("Напишите, как с вами лучше связаться:")
        # следующий текст пользователя нужно передать в поддержку

async def send_to_admin(user_id):
    data = user_data.get(user_id,{})
    text = (
        f"🔥 Новый инвестор!\n\n"
        f"👤 Пользователь: @{data.get('username','—')}\n"
        f"Имя: {data.get('full_name','—')}\n"
        f"ID: {user_id}\n\n"
        f"📌 Опыт инвестирования: {data.get('experience','—')}\n"
        f"📌 Дисциплина: {data.get('discipline','—')}\n"
        f"📌 Финансовая грамотность: {data.get('quiz_score','0')}/{len(quiz_questions)}\n"
        f"🎯 Цель: {data.get('goal','—')}\n"
        f"💰 Первоначальный взнос: {data.get('initial_sum','—')}\n"
        f"💵 Ежемесячные вложения: {data.get('sum','—')}\n"
        f"📌 Контактный метод: {data.get('contact_method','—')}\n"
        f"📌 Контакт: {data.get('contact','—')}\n"
    )
    await bot.send_message(chat_id=ADMIN_ID,text=text)

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
