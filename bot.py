# bot_filter.py
import asyncio
import sqlite3
import datetime
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove, Message, CallbackQuery
)

# ========== Настройка ==========
# Поставь сюда токен и id группы помощников (chat id начинается с -100... обычно)
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
HELPERS_CHAT_ID = -1003081706651  # <-- поменяй на свой ID группы помощников

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
DB_PATH = "bot_filter.db"

# ========== Конфигурация бизнес-логики ==========
MONTHLY_RATE = 0.09  # 9% в месяц (как в твоём коде)
MIN_INVESTMENT = 150  # для примера (или можно убрать)
ASSISTANT_NAME = "Алексей Финансович"  # имя «личности» бота
ASSISTANT_LEGEND = (
    "Привет! Меня зовут <b>{name}</b>. Я — твой финансовый помощник. "
    "Я помог многим людям спланировать путь к их мечтам — от машины до пассивного дохода. "
    "Расскажи, какая у тебя цель, и я быстро посчитаю ориентир."
).format(name=ASSISTANT_NAME)

# ========== Подготовка БД ==========
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            language_code TEXT,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            goal TEXT,
            cost INTEGER,
            monthly INTEGER,
            contact TEXT,
            status TEXT,
            group_msg_id INTEGER,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            step TEXT,
            ts TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(user: types.User):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO users (user_id, first_name, username, language_code, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user.id, user.first_name, user.username, user.language_code, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def save_stat(user_id: int, step: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO stats (user_id, step, ts) VALUES (?, ?, ?)",
                (user_id, step, datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def create_request(user_id: int, goal: str, cost: Optional[int], monthly: Optional[int], contact: Optional[str]):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO requests (user_id, goal, cost, monthly, contact, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, goal, cost, monthly, contact, "new", datetime.datetime.utcnow().isoformat()))
    req_id = cur.lastrowid
    conn.commit()
    conn.close()
    return req_id

def update_request_group_msg(req_id: int, group_msg_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE requests SET group_msg_id=?, status=? WHERE id=?", (group_msg_id, "sent", req_id))
    conn.commit()
    conn.close()

def get_request(req_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, goal, cost, monthly, contact, status, group_msg_id, created_at FROM requests WHERE id=?", (req_id,))
    row = cur.fetchone()
    conn.close()
    return row

# ========== Вспомогательные клавиатуры ==========
def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Начать"), KeyboardButton(text="📘 FAQ")],
            [KeyboardButton(text="📝 Пройти тест"), KeyboardButton(text="📈 Калькулятор цели")],
            [KeyboardButton(text="💬 Связаться с помощником")]
        ],
        resize_keyboard=True
    )
    return kb

def goal_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚗 Машина"), KeyboardButton(text="🏡 Дом")],
            [KeyboardButton(text="💸 Пассивный доход"), KeyboardButton(text="⬅ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def cost_options_for(goal: str):
    if goal == "Машина":
        opts = ["100 000 ₽", "500 000 ₽", "1 000 000 ₽"]
    elif goal == "Дом":
        opts = ["3 000 000 ₽", "5 000 000 ₽", "15 000 000 ₽"]
    else:
        opts = ["100 000 ₽", "500 000 ₽", "1 000 000 ₽"]
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in opts:
        kb.add(KeyboardButton(text=opt))
    kb.add(KeyboardButton(text="⬅ Назад"))
    return kb

def monthly_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="10 000 ₽"), KeyboardButton(text="20 000 ₽"), KeyboardButton(text="30 000 ₽")],
            [KeyboardButton(text="⬅ Назад")]
        ],
        resize_keyboard=True
    )
    return kb

def contact_keyboard_request():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Отправить телефон", request_contact=True)],
            [KeyboardButton(text="✉️ Отправить email (ввести текстом)"), KeyboardButton(text="Пропустить")],
        ],
        resize_keyboard=True
    )
    return kb

def cta_inline_for_helpers(req_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить заявку", callback_data=f"confirm_{req_id}")],
    ])
    return kb

# ========== Локальные состояния (в памяти) ==========
# Небольшой стейт-мэп user_id -> state и временных данных
user_state = {}  # example: {user_id: "expect_goal"}
user_temp = {}   # example: {user_id: {"goal": "Дом", "cost": 500000, ...}}

# ========== Утилиты расчёта ==========
def parse_amount(text: str) -> Optional[int]:
    # "1 000 000 ₽" -> 1000000
    try:
        cleaned = text.replace("₽", "").replace(" ", "").replace(",", "")
        return int(cleaned)
    except Exception:
        return None

def run_compound_calc(cost: int, monthly: int, monthly_rate: float = MONTHLY_RATE):
    total = 0.0
    month = 0
    monthly_totals = []
    while total < cost:
        month += 1
        total = (total + monthly) * (1 + monthly_rate)
        monthly_totals.append(int(total))
        # safety break
        if month > 600: break
    return month, monthly_totals

def run_passive_calc(target_income: int, monthly: int, monthly_rate: float = MONTHLY_RATE):
    capital = 0.0
    month = 0
    passive_list = []
    while True:
        month += 1
        capital = (capital + monthly) * (1 + monthly_rate)
        passive = capital * monthly_rate
        passive_list.append(int(passive))
        if passive >= target_income or month > 600:
            break
    return month, passive_list

# ========== Хендлеры ==========
@dp.message(Command("start"))
async def cmd_start(message: Message):
    save_user(message.from_user)
    save_stat(message.from_user.id, "start")
    user_temp.pop(message.from_user.id, None)
    user_state[message.from_user.id] = "idle"

    text = f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n" \
           f"{ASSISTANT_LEGEND}\n\n" \
           "Небольшое замечание: я не продаю инвестиции — я помогаю находить лучшее предложение и перенаправляю тёплые заявки живым помощникам."
    await message.answer(text, reply_markup=main_menu())

@dp.message(F.text == "🚀 Начать")
async def start_flow(message: Message):
    save_stat(message.from_user.id, "start_flow")
    user_state[message.from_user.id] = "expect_goal"
    user_temp[message.from_user.id] = {}
    await message.answer(f"Отлично, {message.from_user.first_name}! Какая у тебя основная цель?", reply_markup=goal_keyboard())

@dp.message(F.text == "📘 FAQ")
async def faq(message: Message):
    await message.answer(
        "FAQ — коротко:\n\n"
        "• Минимальный вход: 150 USDT (примерно по курсу). \n"
        "• Доходность: ориентировочно 6–12% в месяц (вариативно).\n"
        "• Гарантий прибыли нет — помогаем с платформой и рисками.\n\n"
        "Если хочешь подробности — введи вопрос текстом или нажми 'Связаться с помощником'.",
        reply_markup=main_menu()
    )

@dp.message(F.text == "📝 Пройти тест")
async def start_test(message: Message):
    # здесь можно добавить мини-тест — для простоты оставим приглашение
    await message.answer("Тест пока отключен. Давай лучше просчитаем твою цель — нажми '🚀 Начать' чтобы вернуться.", reply_markup=main_menu())

@dp.message(F.text == "💬 Связаться с помощником")
async def contact_helper(message: Message):
    # открываем диалог с живым помощником (в примере — отправляем ссылку на группу/профиль)
    await message.answer(
        "Ты можешь написать нашему командному чату или оставить заявку — нажми '🚀 Начать' и пройди быстрый расчёт, "
        "чтобы мы передали тебе персонального помощника.",
        reply_markup=main_menu()
    )

# ========== Обработка выбора цели ==========
@dp.message(lambda message: user_state.get(message.from_user.id) == "expect_goal")
async def handle_goal(message: Message):
    text = message.text.strip()
    if text == "⬅ Назад":
        user_state[message.from_user.id] = "idle"
        user_temp.pop(message.from_user.id, None)
        await message.answer("Хорошо, давай начнём заново. Я рядом 👇", reply_markup=main_menu())
        return

    mapping = {
        "🚗 Машина": "Машина",
        "🏡 Дом": "Дом",
        "💸 Пассивный доход": "Пассивный доход"
    }
    if text not in mapping:
        await message.answer("Пожалуйста, выбери одну из кнопок ниже 😊", reply_markup=goal_keyboard())
        return

    goal = mapping[text]
    user_temp[message.from_user.id] = {"goal": goal}
    user_state[message.from_user.id] = "expect_cost"
    save_stat(message.from_user.id, f"chosen_goal:{goal}")

    if goal in ["Машина", "Дом"]:
        await message.answer(f"Понял тебя, {message.from_user.first_name}. Скажи, какая примерная стоимость { 'машины' if goal=='Машина' else 'дома' }?", reply_markup=cost_options_for(goal))
    else:
        # пассивный доход
        await message.answer("Сколько в месяц ты хочешь получать пассивного дохода? Выбери один вариант:", reply_markup=cost_options_for(goal))

# ========== Обработка выбора стоимости / дохода ==========
@dp.message(lambda message: user_state.get(message.from_user.id) == "expect_cost")
async def handle_cost(message: Message):
    text = message.text.strip()
    if text == "⬅ Назад":
        user_state[message.from_user.id] = "expect_goal"
        await message.answer("Вернулись назад. Выбери цель.", reply_markup=goal_keyboard())
        return

    amount = parse_amount(text)
    if amount is None:
        await message.answer("Попробуй выбрать одну из кнопок, так будет быстро и точно 😊", reply_markup=cost_options_for(user_temp[message.from_user.id]["goal"]))
        return

    user_temp[message.from_user.id]["cost"] = amount
    user_state[message.from_user.id] = "expect_monthly"
    save_stat(message.from_user.id, f"chosen_cost:{amount}")

    await message.answer("Сколько ты готов инвестировать в месяц? Это поможет рассчитать реальный срок.", reply_markup=monthly_keyboard())

# ========== Обработка выбора ежемесячной суммы ==========
@dp.message(lambda message: user_state.get(message.from_user.id) == "expect_monthly")
async def handle_monthly(message: Message):
    text = message.text.strip()
    if text == "⬅ Назад":
        user_state[message.from_user.id] = "expect_cost"
        await message.answer("Окей — вернулись к выбору стоимости.", reply_markup=cost_options_for(user_temp[message.from_user.id]["goal"]))
        return

    monthly = parse_amount(text)
    if monthly is None:
        await message.answer("Пожалуйста, выбери одну из кнопок ниже.", reply_markup=monthly_keyboard())
        return

    user_temp[message.from_user.id]["monthly"] = monthly
    goal = user_temp[message.from_user.id]["goal"]
    cost = user_temp[message.from_user.id].get("cost")
    save_stat(message.from_user.id, f"chosen_monthly:{monthly}")

    # Рассчитываем
    if goal in ["Машина", "Дом"]:
        months_needed, monthly_totals = run_compound_calc(cost, monthly)
        # Персональное сообщение и эмпатия
        await message.answer(f"Хорошо, {message.from_user.first_name}! Сейчас посчитаю... ⏳")
        # Короткая «человеческая» нота
        await message.answer(
            f"📈 <b>Результат</b>:\n\n"
            f"С инвестициями {monthly:,} ₽/мес ты сможешь { 'купить ' + goal.lower() if goal!='Пассивный доход' else '' } "
            f"стоимостью {cost:,} ₽ примерно через <b>{months_needed}</b> месяцев.\n\n"
            f"Честно: расчёт ориентировочный и принимает стабильную доходность ~9%/мес. Но это даёт представление о сроках. 🚀"
        )
    else:
        target = cost  # for passive goal we stored desired monthly income in 'cost'
        months_needed, passive_list = run_passive_calc(target, monthly)
        await message.answer("Считаю возможный пассивный поток... ⏳")
        await message.answer(
            f"📈 <b>Результат</b>:\n\n"
            f"При вложении {monthly:,} ₽/мес пассивный доход (проценты) приблизится к {target:,} ₽/мес через ≈ <b>{months_needed}</b> месяцев.\n\n"
            "Если хочешь, могу передать твою заявку личному помощнику — он свяжется и подготовит персональный план."
        )

    # Показать краткий прогресс + CTA
    user_state[message.from_user.id] = "post_calc"
    await message.answer(
        "Хочешь, я передам это живому помощнику и он свяжется с тобой для подготовки персонального плана?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Да, свяжитесь со мной"), KeyboardButton(text="✍️ Написать сам (пропустить)")],
                [KeyboardButton(text="⬅ Назад"), KeyboardButton(text="🏠 В главное меню")]
            ],
            resize_keyboard=True
        )
    )

# ========== Пост-расчёт: подтверждение отправки заявки ==========
@dp.message(lambda message: user_state.get(message.from_user.id) == "post_calc")
async def post_calc_handler(message: Message):
    text = message.text.strip()
    if text == "⬅ Назад":
        user_state[message.from_user.id] = "expect_monthly"
        await message.answer("Вернулись к выбору ежемесячной суммы.", reply_markup=monthly_keyboard())
        return
    if text == "🏠 В главное меню":
        user_state[message.from_user.id] = "idle"
        user_temp.pop(message.from_user.id, None)
        await message.answer("Хорошо, давай позже. Возвращайся когда будет удобно.", reply_markup=main_menu())
        return
    if text == "✍️ Написать сам (пропустить)":
        user_state[message.from_user.id] = "idle"
        user_temp.pop(message.from_user.id, None)
        await message.answer("Окей — если передумаешь, нажми '🚀 Начать'.", reply_markup=main_menu())
        return
    if text == "✅ Да, свяжитесь со мной":
        # Просим контакт (кнопка с запросом контакта) — либо пропустить
        user_state[message.from_user.id] = "expect_contact"
        await message.answer(
            "Чтобы помощник мог связаться удобным способом, пришли контакт (телефон) — либо нажми 'Пропустить' и мы отправим только Telegram ID.",
            reply_markup=contact_keyboard_request()
        )
        return
    # если пользователь ввёл что-то ещё
    await message.answer("Пожалуйста, выбери кнопку.", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Да, свяжитесь со мной"), KeyboardButton(text="✍️ Написать сам (пропустить)")],
                [KeyboardButton(text="⬅ Назад"), KeyboardButton(text="🏠 В главное меню")]
            ],
            resize_keyboard=True
        ))

# ========== Сбор контакта ==========
@dp.message(lambda message: user_state.get(message.from_user.id) == "expect_contact" and message.contact)
async def contact_via_request(message: Message):
    # получили контакт через кнопку request_contact
    phone = message.contact.phone_number
    await finalize_and_send_request(message.from_user, contact=phone, message_obj=message)

@dp.message(lambda message: user_state.get(message.from_user.id) == "expect_contact")
async def contact_text_or_skip(message: Message):
    text = message.text.strip()
    if text == "Пропустить":
        await finalize_and_send_request(message.from_user, contact=None, message_obj=message)
        return
    if text == "✉️ Отправить email (ввести текстом)":
        await message.answer("Введи, пожалуйста, email в текстовом сообщении (например: info@you.ru).")
        user_state[message.from_user.id] = "expect_contact_email"
        return
    if user_state.get(message.from_user.id) == "expect_contact_email" or ("@" in text and "." in text):
        # простая проверка для email
        await finalize_and_send_request(message.from_user, contact=text, message_obj=message)
        return
    await message.answer("Пожалуйста, используй кнопки выше или введи телефон/email вручную.", reply_markup=contact_keyboard_request())

async def finalize_and_send_request(user: types.User, contact: Optional[str], message_obj: Message):
    uid = user.id
    temps = user_temp.get(uid, {})
    goal = temps.get("goal")
    cost = temps.get("cost")
    monthly = temps.get("monthly")
    # Сохраняем заявку в БД
    req_id = create_request(uid, goal or "", cost or 0, monthly or 0, contact)
    save_stat(uid, f"created_request:{req_id}")
    # Формируем сообщение для группы помощников
    username = f"@{user.username}" if user.username else "нет"
    contact_info = contact if contact else "не указан (только Telegram)"
    text = (
        f"🚨 <b>Новый инвестор (лид)</b>\n\n"
        f"👤 Имя: {user.full_name}\n"
        f"🆔 ID: {uid}\n"
        f"💬 Username: {username}\n"
        f"🎯 Цель: {goal}\n"
        f"💶 Стоимость/цель: {cost:,} ₽\n"
        f"💸 Готов инвестировать в мес: {monthly:,} ₽\n"
        f"📞 Контакт: {contact_info}\n"
        f"🕒 Время: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} (UTC)\n\n"
        "Нажмите кнопку ниже, чтобы подтвердить заявку и связаться с клиентом."
    )
    # Отправляем в группу помощников с кнопкой подтверждения
    sent = await bot.send_message(chat_id=HELPERS_CHAT_ID, text=text, reply_markup=cta_inline_for_helpers(req_id))
    # Обновляем запись в БД с id сообщения в группе
    update_request_group_msg(req_id, sent.message_id)

    # Отправляем пользователю дружелюбное подтверждение
    await message_obj.answer(
        f"Спасибо, {user.first_name}! Я передал(а) твою заявку живому помощнику. Как только кто-то подтвердит — ты получишь сообщение от него.\n\n"
        "Пока можешь вернуться в главное меню.",
        reply_markup=main_menu()
    )
    # Очистим temp и стейт
    user_state.pop(uid, None)
    user_temp.pop(uid, None)

# ========== Обработка нажатий помощников в группе ==========
@dp.callback_query()
async def handle_callbacks(cb: CallbackQuery):
    data = cb.data or ""
    user = cb.from_user
    chat_id = cb.message.chat.id if cb.message else None
    # Обработка подтверждения заявки: callback_data = confirm_{req_id}
    if data.startswith("confirm_"):
        # только в группе помощников
        if chat_id != HELPERS_CHAT_ID:
            await cb.answer("Кнопка действительна только в группе помощников.", show_alert=True)
            return
        try:
            req_id = int(data.split("_")[1])
        except Exception:
            await cb.answer("Неверные данные кнопки.", show_alert=True)
            return
        row = get_request(req_id)
        if not row:
            await cb.answer("Заявка не найдена или уже обработана.", show_alert=True)
            return
        # row: (id, user_id, goal, cost, monthly, contact, status, group_msg_id, created_at)
        req_user_id = row[1]
        helper_name = user.full_name
        helper_username = f"@{user.username}" if user.username else None
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S (UTC)")

        # Отправляем пользователю сообщение с контактом помощника
        if helper_username:
            helper_contact_url = f"https://t.me/{user.username}"
        else:
            helper_contact_url = f"tg://user?id={user.id}"

        kb_user = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"✉️ Написать помощнику {helper_name}", url=helper_contact_url)]
        ])
        try:
            await bot.send_message(chat_id=req_user_id,
                                   text=f"✅ Твоя заявка подтверждена помощником {helper_name}.\n⏰ {now}\n\n"
                                        "Нажми кнопку ниже, чтобы написать ему прямо в Telegram.",
                                   reply_markup=kb_user)
        except Exception as e:
            logging.exception("Не удалось отправить пользователю сообщение: %s", e)

        # Обновляем сообщение в группе: добавляем информацию о том, кто подтвердил
        new_text = cb.message.text + f"\n\n✅ Подтвержено {now} помощником {helper_name}"
        try:
            await cb.message.edit_text(new_text)
        except Exception as e:
            logging.exception("Не смог изменить сообщение в группе: %s", e)

        await cb.answer("Заявка подтверждена и пользователь уведомлён.")
        # можно также обновить статус в БД (не обязательно)
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("UPDATE requests SET status=? WHERE id=?", ("confirmed", req_id))
        conn.commit()
        conn.close()
        return

# ========== Универсальный fallback ==========
@dp.message()
async def all_other_messages(message: Message):
    # Если пользователь в середине воронки — обработка выше поймала бы.
    # Тут — универсальное приветствие / помощь
    await message.answer("Я тебя не совсем понял. Нажми '🚀 Начать' чтобы пройти быстрый расчёт или выбери из меню.", reply_markup=main_menu())

# ========== Запуск ==========
async def main():
    init_db()
    logging.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())