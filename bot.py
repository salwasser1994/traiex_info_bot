import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# === Конфиг ===
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = -1003081706651
OFFER_PDF_FILE_ID = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# === Хранилище данных пользователей ===
user_data = {}

# === Warm-up ===
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_data[message.from_user.id] = {}
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, хочу узнать! 🚀", callback_data="warmup_yes")],
        [InlineKeyboardButton(text="Нет, просто хочу идеи 💡", callback_data="warmup_no")]
    ])
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я твой финансовый помощник. 💼\n"
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
    await query.message.edit_text("А у тебя есть опыт инвестирования?", reply_markup=kb)

@dp.callback_query(F.data.startswith("experience_"))
async def experience_handler(query: CallbackQuery):
    user_data[query.from_user.id]["experience"] = query.data.replace("experience_", "")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, дисциплинирован 📊", callback_data="discipline_yes")],
        [InlineKeyboardButton(text="Не совсем дисциплинирован ⚠️", callback_data="discipline_no")]
    ])
    await query.message.edit_text("Ты следишь за своими финансами и инвестициями?", reply_markup=kb)

# === Вопросы для оценки финансовой грамотности ===
fingram_questions = [
    {"question": "Что такое пассивный доход?", "options": ["Доход без активной работы", "Зарплата", "Бонусы"], "correct": 0},
    {"question": "Что такое диверсификация?", "options": ["Вложение в разные активы", "Только акции", "Не вкладываться"], "correct": 0},
    {"question": "Что такое инвестиционный риск?", "options": ["Потеря части или всех вложений", "Гарантированная прибыль", "Беспроигрышная ставка"], "correct": 0},
    {"question": "Что обычно сопровождает высокую доходность?", "options": ["Высокий риск", "Гарантированный доход", "Малую волатильность"], "correct": 0},
    {"question": "Что такое ликвидность?", "options": ["Способность быстро продать актив", "Доходность инвестиций", "Налог на прибыль"], "correct": 0},
    {"question": "Что такое инфляция?", "options": ["Рост цен и снижение покупательной способности", "Снижение цен", "Рост зарплаты"], "correct": 0},
    {"question": "Что такое облигация?", "options": ["Долговая ценная бумага", "Акция компании", "Депозит"], "correct": 0},
    {"question": "Что такое акция?", "options": ["Доля в компании", "Депозит", "Кредит"], "correct": 0},
    {"question": "Что такое ETF?", "options": ["Биржевой фонд", "Банковский вклад", "Криптовалюта"], "correct": 0},
    {"question": "Что такое капитализация?", "options": ["Стоимость компании", "Зарплата", "Налог"], "correct": 0}
]

@dp.callback_query(F.data.startswith("discipline_"))
async def discipline_handler(query: CallbackQuery):
    user_data[query.from_user.id]["discipline"] = query.data.replace("discipline_", "")
    user_data[query.from_user.id]["quiz_index"] = 0
    user_data[query.from_user.id]["quiz_score"] = 0
    await send_fingram_question(query.from_user.id, query.message)

async def send_fingram_question(user_id, message):
    index = user_data[user_id]["quiz_index"]
    q = fingram_questions[index]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=opt, callback_data=f"quiz_{index}_{i}")] for i, opt in enumerate(q["options"])
    ])
    await message.edit_text(f"{q['question']}", reply_markup=kb)

@dp.callback_query(F.data.startswith("quiz_"))
async def quiz_handler(query: CallbackQuery):
    parts = query.data.split("_")
    q_index, opt_index = int(parts[1]), int(parts[2])
    if opt_index == fingram_questions[q_index]["correct"]:
        user_data[query.from_user.id]["quiz_score"] += 1
    user_data[query.from_user.id]["quiz_index"] += 1
    if user_data[query.from_user.id]["quiz_index"] < len(fingram_questions):
        await send_fingram_question(query.from_user.id, query.message)
    else:
        # Переход к вводу первоначального взноса
        sums_initial = ["10 000 ₽", "20 000 ₽", "30 000 ₽", "40 000 ₽", "50 000 ₽",
                        "100 000 ₽", "250 000 ₽", "500 000 ₽", "1 000 000 ₽"]
        keyboard_rows = []
        for i in range(0, len(sums_initial), 3):
            row = [InlineKeyboardButton(text=s, callback_data=f"initial_{s}") for s in sums_initial[i:i+3]]
            keyboard_rows.append(row)
        kb_initial = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
        await query.message.answer("Сколько денег ты готов вложить первоначально?", reply_markup=kb_initial)

# === Ввод первоначального взноса и ежемесячного вложения ===
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

# === Прогноз Trading Bot ===
@dp.callback_query(F.data.startswith("sum_"))
async def sum_handler(query: CallbackQuery):
    user_data[query.from_user.id]["sum"] = query.data.replace("sum_", "")
    initial_sum = int(user_data[query.from_user.id]["initial_sum"].replace("₽","").replace(" ",""))
    monthly_invest = int(user_data[query.from_user.id]["sum"].replace("₽","").replace(" ",""))
    rate = 0.09
    periods = [1,3,6,12,24]

    balance = 0
    forecast_text = f"💡 Прогноз Trading Bot при первоначальном взносе {initial_sum:,} ₽ и ежемесячном вложении {monthly_invest:,} ₽ (9%/мес)\n\n"

    for month in range(1, max(periods)+1):
        invested_this_month = initial_sum if month==1 else monthly_invest
        balance += invested_this_month
        passive_income = int(balance * rate)
        balance += passive_income
        if month in periods:
            forecast_text += (f"Месяц {month}\n"
                              f"💵 Вложение в этом месяце: {invested_this_month:,} ₽\n"
                              f"Пассивный доход: {passive_income:,} ₽ (9%)\n"
                              f"Баланс: {balance:,} ₽\n\n")
    kb_next = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Далее", callback_data="offer_read")]
    ])
    await query.message.edit_text(forecast_text, reply_markup=kb_next)

# === Оферта ===
@dp.callback_query(F.data=="offer_read")
async def offer_handler(query: CallbackQuery):
    await bot.send_document(chat_id=query.from_user.id, document=OFFER_PDF_FILE_ID)
    kb_accept = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я согласен с офертой ✅", callback_data="offer_accept")]
    ])
    await query.message.answer("Прочитайте оферту и подтвердите согласие:", reply_markup=kb_accept)

# === Подтверждение оферты и выбор способа связи ===
@dp.callback_query(F.data=="offer_accept")
async def offer_accept_handler(query: CallbackQuery):
    kb_contact = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Телеграм", callback_data="contact_telegram")],
        [InlineKeyboardButton(text="Email", callback_data="contact_email")],
        [InlineKeyboardButton(text="Телефон", callback_data="contact_phone")],
        [InlineKeyboardButton(text="Другое", callback_data="contact_other")]
    ])
    await query.message.answer("Выберите удобный способ связи с личным помощником:", reply_markup=kb_contact)

@dp.callback_query(F.data.startswith("contact_"))
async def contact_method_handler(query: CallbackQuery):
    method = query.data.replace("contact_","")
    user_data[query.from_user.id]["contact_method"] = method
    if method == "telegram":
        if query.from_user.username:
            user_data[query.from_user.id]["contact_info"] = f"@{query.from_user.username}"
            await send_to_admin(query.from_user.id)
            await query.message.answer("Отлично! Мы свяжемся с вами через Telegram.")
        else:
            await query.message.answer("Ваш аккаунт приватный или нет username. Напишите, пожалуйста, ваш Telegram вручную:")
    else:
        await query.message.answer("Напишите, пожалуйста, как с вами лучше связаться (Email, телефон или другое):")

@dp.message()
async def contact_text_handler(message: Message):
    if "contact_method" in user_data.get(message.from_user.id, {}) and \
       message.text and not message.text.startswith("/"):
        user_data[message.from_user.id]["contact_info"] = message.text
        await send_to_admin(message.from_user.id)
        await message.answer("Спасибо! Ваши данные отправлены нашему эксперту.")

# === Отправка данных в поддержку ===
async def send_to_admin(user_id):
    data = user_data.get(user_id, {})
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(f"🔥 Новый инвестор!\n\n"
              f"👤 Пользователь: @{data.get('username','—')}\n"
              f"Имя: {data.get('full_name','—')}\n"
              f"ID: {user_id}\n\n"
              f"📌 Опыт инвестирования: {data.get('experience','—')}\n"
              f"📌 Дисциплина: {data.get('discipline','—')}\n"
              f"📌 Финансовая грамотность: {data.get('quiz_score',0)}/{len(fingram_questions)}\n"
              f"💰 Первоначальный взнос: {data.get('initial_sum','—')}\n"
              f"💵 Ежемесячные вложения: {data.get('sum','—')}\n"
              f"📌 Контактный метод: {data.get('contact_method','—')}\n"
              f"📌 Контакт: {data.get('contact_info','—')}\n")
    )

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
