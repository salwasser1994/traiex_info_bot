import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

logging.basicConfig(level=logging.INFO)

# === Конфиг ===
BOT_TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
ADMIN_ID = -1003081706651
OFFER_PDF_FILE_ID = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_data = {}

# === Приветствие ===
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_data[message.from_user.id] = {"quiz_index":0,"quiz_score":0}
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать опрос 🚀", callback_data="start_survey")]
    ])
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Давай узнаем твой уровень финансовой грамотности, твои цели и готовность инвестировать. "
        "Это поможет нам дать тебе полезную информацию, секреты успеха и доступ к личному помощнику. "
        "Ты также получишь доступ к приватной группе единомышленников.\n\n"
        "Готов пройти опрос?",
        reply_markup=kb
    )

# === Вопросы по финансовой грамотности ===
quiz_questions = [
    {"question": "Что такое пассивный доход?", "options":["Деньги работают сами","Зарплата","Выигрыш в лотерею"], "correct":0},
    {"question": "Что такое диверсификация?", "options":["Разные активы","Все в акции","Все в один актив"], "correct":0},
    {"question": "Что такое инвестиционный риск?", "options":["Потеря части или всех вложений","Гарантированная прибыль","Нет риска"], "correct":0},
    {"question": "Что повышает доходность?", "options":["Больше риска","Гарантия","Ничего"], "correct":0},
    {"question": "Что обычно сопровождает высокую доходность?", "options":["Высокий риск","Гарантия","Малый риск"], "correct":0},
    {"question": "Что такое ликвидность?", "options":["Скорость превращения в деньги","Доход","Риск"], "correct":0},
    {"question": "Что такое капитал?", "options":["Накопленные средства","Долг","Зарплата"], "correct":0},
    {"question": "Что такое инфляция?", "options":["Рост цен и падение покупательной способности","Рост дохода","Падение цен"], "correct":0},
    {"question": "Что такое доходность?", "options":["Прибыль от инвестиций","Вклад в банк","Покупка акций"], "correct":0},
    {"question": "Что такое резервный фонд?", "options":["Сбережения на черный день","Инвестиции в акции","Кредиты"], "correct":0}
]

# === Функция отправки вопроса ===
async def send_quiz_question(user_id, message):
    index = user_data[user_id]["quiz_index"]
    if index < len(quiz_questions):
        q = quiz_questions[index]
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=opt, callback_data=f"quiz_{index}_{i}")] for i,opt in enumerate(q["options"])
        ])
        await message.edit_text(f"{q['question']}", reply_markup=kb)
    else:
        # После финграмоты спрашиваем цели
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пассивный доход 💸", callback_data="goal_passive")],
            [InlineKeyboardButton(text="Дом 🏠", callback_data="goal_house")],
            [InlineKeyboardButton(text="Машина 🚗", callback_data="goal_car")],
            [InlineKeyboardButton(text="Приумножить капитал 📊", callback_data="goal_growth")]
        ])
        await message.edit_text("Какая твоя главная финансовая цель?", reply_markup=kb)

# === Обработка ответов на финграмоту ===
@dp.callback_query(F.data.startswith("quiz_"))
async def quiz_handler(query: CallbackQuery):
    parts = query.data.split("_")
    q_index, opt_index = int(parts[1]), int(parts[2])
    if opt_index == quiz_questions[q_index]["correct"]:
        user_data[query.from_user.id]["quiz_score"] += 1
    user_data[query.from_user.id]["quiz_index"] += 1
    await send_quiz_question(query.from_user.id, query.message)

# === Цели ===
@dp.callback_query(F.data.startswith("goal_"))
async def goal_handler(query: CallbackQuery):
    goal_map = {
        "goal_passive": "Пассивный доход 💸",
        "goal_house": "Дом 🏠",
        "goal_car": "Машина 🚗",
        "goal_growth": "Приумножить капитал 📊"
    }
    user_data[query.from_user.id]["goal"] = goal_map[query.data]

    sums_initial = ["10 000 ₽", "20 000 ₽", "30 000 ₽", "40 000 ₽", "50 000 ₽",
                    "100 000 ₽", "250 000 ₽", "500 000 ₽", "1 000 000 ₽"]
    keyboard_rows = []
    for i in range(0, len(sums_initial), 3):
        row = [InlineKeyboardButton(text=s, callback_data=f"initial_{s}") for s in sums_initial[i:i+3]]
        keyboard_rows.append(row)
    kb_initial = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await query.message.edit_text("Сколько денег ты готов вложить первоначально?", reply_markup=kb_initial)

# === Первоначальный взнос ===
@dp.callback_query(F.data.startswith("initial_"))
async def initial_handler(query: CallbackQuery):
    user_data[query.from_user.id]["initial_sum"] = query.data.replace("initial_","")
    sums_monthly = ["0 ₽","10 000 ₽","20 000 ₽","30 000 ₽","40 000 ₽","50 000 ₽","100 000 ₽"]
    keyboard_rows=[]
    for i in range(0,len(sums_monthly),3):
        row = [InlineKeyboardButton(text=s, callback_data=f"sum_{s}") for s in sums_monthly[i:i+3]]
        keyboard_rows.append(row)
    kb_monthly = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await query.message.edit_text("Сколько денег готов вкладывать ежемесячно?", reply_markup=kb_monthly)

# === Прогноз ===
@dp.callback_query(F.data.startswith("sum_"))
async def sum_handler(query: CallbackQuery):
    user_data[query.from_user.id]["sum"] = query.data.replace("sum_","")
    initial_sum = int(user_data[query.from_user.id]["initial_sum"].replace("₽","").replace(" ",""))
    monthly_invest = int(user_data[query.from_user.id]["sum"].replace("₽","").replace(" ",""))
    rate = 0.09
    periods = [1,3,6,12,24]
    balance = 0
    forecast_text = f"💡 Прогноз Trading Bot при первоначальном взносе {initial_sum:,} ₽ и ежемесячном вложении {monthly_invest:,} ₽ (9%/мес)\n\n"
    for month in periods:
        invest = initial_sum if month==1 else monthly_invest
        balance += invest
        passive = balance * rate
        balance += passive
        forecast_text += f"Месяц {month}\n💵 Вложение в этом месяце: {invest:,} ₽\nПассивный доход: {int(passive):,} ₽\nБаланс: {int(balance):,} ₽\n\n"
    kb_offer = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ознакомиться с офертой 📄", callback_data="offer_read")]
    ])
    await query.message.edit_text(forecast_text, reply_markup=kb_offer)

# === Оферта ===
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
        [InlineKeyboardButton(text="Телеграм", callback_data="contact_telegram")],
        [InlineKeyboardButton(text="Email", callback_data="contact_email")],
        [InlineKeyboardButton(text="Телефон", callback_data="contact_phone")],
        [InlineKeyboardButton(text="Другое", callback_data="contact_other")]
    ])
    await query.message.answer("Выберите, как вам удобнее связаться с личным помощником:", reply_markup=kb_contact)

# === Контакты и проверка username ===
@dp.callback_query(F.data.startswith("contact_"))
async def contact_method_handler(query: CallbackQuery):
    method = query.data.replace("contact_","")
    user_data[query.from_user.id]["contact_method"] = method
    if method=="telegram":
        await query.message.answer("Пожалуйста, укажите ваш @username для связи через Telegram:")
    else:
        await query.message.answer("Напишите, как с вами лучше связаться:")

@dp.message()
async def capture_contact_info(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data: return
    contact_method = user_data[user_id].get("contact_method")
    if contact_method=="telegram":
        username = message.text.strip()
        if not username.startswith("@"):
            await message.answer("Неверный формат. Укажите ваш @username.")
            return
        # Проверяем доступность аккаунта
        try:
            chat = await bot.get_chat(username)
        except TelegramBadRequest:
            await message.answer("Этот username недоступен или приватный, введите другой @username.")
            return
        user_data[user_id]["contact_info"] = username
    else:
        user_data[user_id]["contact_info"] = message.text

    # Отправляем все данные в поддержку
    data = user_data[user_id]
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔥 Новый инвестор!\n\n"
            f"👤 Пользователь: @{message.from_user.username or '—'}\n"
            f"Имя: {message.from_user.full_name}\n"
            f"ID: {message.from_user.id}\n\n"
            f"📌 Финансовая грамотность: {data.get('quiz_score','—')}/{len(quiz_questions)}\n"
            f"📌 Цель: {data.get('goal','—')}\n"
            f"💰 Первоначальный взнос: {data.get('initial_sum','—')}\n"
            f"💵 Ежемесячные вложения: {data.get('sum','—')}\n"
            f"📌 Контактный метод: {data.get('contact_method','—')}\n"
            f"📌 Контакт: {data.get('contact_info','—')}\n"
        )
    )
    await message.answer("Спасибо! Ваши данные отправлены, наш личный помощник свяжется с вами в ближайшее время.")

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
