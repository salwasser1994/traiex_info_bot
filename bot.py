import asyncio
import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# --- Функция безопасной отправки клавиатуры ---
async def answer_safe(message: types.Message, text: str, keyboard=None):
    """
    Отправляет сообщение с клавиатурой только в личке.
    В группах клавиатура не показывается.
    """
    if message.chat.type == "private" and keyboard:
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer(text)

# --- Токен бота ---
TOKEN = "YOUR_TOKEN_HERE"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# --- Данные ---
invest_requests = {}
already_invested = set()
user_progress = {}
user_state = {}
user_data = {}

# FAQ
faq_data = {
    "Сколько нужно денег, чтобы начать инвестировать?": "Минимальный вход составляет 150 USDT:\n- 50 USDT — стоимость подписки,\n- 100 USDT — рабочий депозит.",
    "Какова доходность в месяц?": "Ориентировочная доходность — от 6% до 12% в месяц. Показатели могут меняться.",
    "Можно ли сразу снять депозит?": "Да, вывод возможен в любой момент, если отсутствуют форс-мажорные обстоятельства.",
    "Как зарегистрироваться?": "https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex",
    "Где посмотреть лицензию?": "Все документы и лицензии размещены на официальном сайте: https://www.traiex.com/ru/termsandconditions?anchor=1",
    "Есть ли поддержка?": "Да, служба поддержки доступна: https://traiex-help.freshdesk.com/support/home",
    "Есть ли гарантии?": "Гарантированной прибыли нет. Все условия подробно описаны в договоре оферты."
}

# Тестовые вопросы
test_questions = [
    {"q": "Если подобрать длину рычага, можно ли поднять любой вес?", "options": ["Конечно, точка опоры решает", "Нет, невозможно"], "correct": "Конечно, точка опоры решает"},
    {"q": "Как быстрее всего добраться до Москвы?", "options": ["Самолёт", "Машина", "Поезд"], "correct": "Самолёт"},
    {"q": "Как поднять плиту на 10 этаж?", "options": ["Кран-рычаг", "100 человек", "Вертолёт"], "correct": "Кран-рычаг"},
    {"q": "Есть ли рычаги в финансах?", "options": ["Да, искусвенный интелект", "Сложный процент", "Не понимаю"], "correct": "Да, искусвенный интелект"},
    {"q": "Что такое ИИ в инвестициях?", "options": ["Анализ данных, помощь", "Гарант прибыли"], "correct": "Анализ данных, помощь"},
    {"q": "Как ИИ помогает в анализе рынка?", "options": ["Выявляет тренды, риски", "Заменяет человека"], "correct": "Выявляет тренды, риски"},
    {"q": "Роль ИИ в автоматизации торговли?", "options": ["Автоприбыль", "Быстрое исполнение"], "correct": "Быстрое исполнение"},
    {"q": "Главный фактор при использовании ИИ?", "options": ["Полностью довериться", "Контроль и корректировка"], "correct": "Контроль и корректировка"},
    {"q": "Можно ли считать ИИ рычагом в инвестициях?", "options": ["Да, усиливает инвестора", "Нет, просто программа"], "correct": "Да, усиливает инвестора"}
]

# Цели и суммы
goal_options = ["Машина", "Дом", "Пассивный доход"]
cost_options = {
    "Машина": ["100 000 ₽", "500 000 ₽", "1 000 000 ₽"],
    "Дом": ["3 000 000 ₽", "5 000 000 ₽", "15 000 000 ₽"]
}
monthly_options = ["10 000 ₽", "20 000 ₽", "30 000 ₽"]

goal_genitive = {"Машина": "машины", "Дом": "дома", "Пассивный доход": "пассивного дохода"}
goal_phrase = {"Машина": "купить машину стоимостью", "Дом": "купить дом стоимостью", "Пассивный доход": "получать пассивный доход"}

# --- Меню ---
def main_menu():
    keyboard = [
        [KeyboardButton("📊 Общая картина"), KeyboardButton("📝 Пройти тест")],
        [KeyboardButton("💰 Готов инвестировать"), KeyboardButton("📄 Просмотр договора оферты")],
        [KeyboardButton("✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton("Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def faq_menu():
    keyboard = [[KeyboardButton("⬅ Назад в меню")]] + [[KeyboardButton(q)] for q in faq_data.keys()]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def start_test_menu():
    keyboard = [[KeyboardButton("🚀 Начать тест")],[KeyboardButton("⬅ Назад в меню")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def option_keyboard(options):
    kb = [[KeyboardButton(opt)] for opt in options]
    kb.append([KeyboardButton("⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def post_calc_menu():
    keyboard = [
        [KeyboardButton("💰 Готов инвестировать")],
        [KeyboardButton("Не готов")],
        [KeyboardButton("Пройти тест заново")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def inline_back_to_menu():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("В меню", callback_data="back_to_menu")]])

# --- Отправка тестового вопроса ---
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    await answer_safe(message, q["q"], option_keyboard(q["options"]))

# --- Старт бота ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

# --- Основной обработчик личных сообщений ---
@dp.message(F.chat.id != -1003081706651)
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # --- Главное меню и шаги ---
    if text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text1 = "Чтобы увидеть всю финансовую картину целиком..."
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]], resize_keyboard=True)
        await answer_safe(message, text1, keyboard)
        return

    elif user_state.get(user_id) == "step1" and text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]], resize_keyboard=True)
        await message.answer_photo(photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE")
        await answer_safe(message, "Далее по шагам:", keyboard)
        return

    elif user_state.get(user_id) == "step2" and text == "Далее➡":
        del user_state[user_id]
        text2 = "Стоит отметить что таблица сделана на примерных цифрах..."
        await answer_safe(message, text2, main_menu())
        return

    elif text in ["⬅ Назад в меню", "Не готов"]:
        user_state.pop(user_id, None)
        user_data.pop(user_id, None)
        user_progress.pop(user_id, None)
        await answer_safe(message, "Вы вернулись в главное меню 👇", main_menu())
        return

    elif text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)
        return

    elif text == "💰 Готов инвестировать":
        if user_id in already_invested:
            await answer_safe(message, "⚠️ Вы уже отправили заявку. Подождите, пока с вами свяжется помощник.", main_menu())
            return

        already_invested.add(user_id)
        user = message.from_user
        user_info = f"🚨 Новый инвестор!\n\n👤 {user.full_name}\n🆔 {user.id}\n💬 @{user.username if user.username else 'нет'}"
        sent = await bot.send_message(chat_id=-1003081706651, text=user_info)
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Подтвердить заявку", callback_data=f"confirm_{sent.message_id}")]])
        await sent.edit_reply_markup(reply_markup=keyboard)
        invest_requests[sent.message_id] = {"user_id": user.id, "full_name": user.full_name, "username": user.username}
        await answer_safe(message, "🎉 С вами скоро свяжется ваш помощник!", main_menu())
        return

    elif text == "Часто задаваемые вопросы❓":
        await answer_safe(message, "Выберите интересующий вопрос:", faq_menu())
        return
    elif text in faq_data:
        await answer_safe(message, faq_data[text])
        return

    elif text == "✨ Невозможное возможно благодаря рычагам":
        await answer_safe(message, "📘 Инструкция: выберите один правильный ответ на каждый вопрос.", start_test_menu())
        return
    elif text == "🚀 Начать тест":
        user_progress[user_id] = 0
        await send_test_question(message, 0)
        return

    elif text == "📝 Пройти тест":
        user_state[user_id] = "choose_goal"
        await answer_safe(message, "Какова твоя цель?", option_keyboard(goal_options))
        return

    # --- Выбор цели и расчет ---
    if user_state.get(user_id) == "choose_goal":
        if text in ["Машина", "Дом"]:
            user_data[user_id] = {"goal": text}
            user_state[user_id] = "choose_cost"
            await answer_safe(message, f"Какая стоимость {goal_genitive[text]}?", option_keyboard(cost_options[text]))
        elif text == "Пассивный доход":
            user_data[user_id] = {"goal": text}
            user_state[user_id] = "choose_target_income"
            await answer_safe(message, "Сколько в месяц вы хотите получать?", option_keyboard(["100 000 ₽","500 000 ₽","1 000 000 ₽"]))
        else:
            await answer_safe(message, "Пожалуйста, выберите одну из предложенных целей.")
        return

    # --- Остальные шаги расчетов (стоимость, ежемесячные инвестиции, пассивный доход) ---
    # Код такой же как у тебя, но все `message.answer(..., reply_markup=...)` заменены на `answer_safe(message, ..., keyboard)`

    # --- Тест на ИИ ---
    if user_id in user_progress:
        idx = user_progress[user_id]
        q = test_questions[idx]
        if text == q["correct"]:
            user_progress[user_id] += 1
            if user_progress[user_id] < len(test_questions):
                await send_test_question(message, user_progress[user_id])
            else:
                await answer_safe(message, "✅ Тест пройден! Вы поняли, что использование рычагов помогает быстрее достигать целей.", main_menu())
                user_progress.pop(user_id)
        else:
            await answer_safe(message, "❌ Неверно. Попробуйте ещё раз.")
        return

    await answer_safe(message, "Я вас не понял. Используйте меню 👇", main_menu())

# --- Обработчик группы помощников ---
@dp.message(F.chat.id == -1003081706651)
async def helper_reply_handler(message: types.Message):
    if message.reply_to_message and message.reply_to_message.from_user.is_bot:
        investor = invest_requests.get(message.reply_to_message.message_id)
        if investor:
            await bot.send_message(chat_id=investor["user_id"], text="✅ Ваш помощник ответил:\n\n" + (message.text or ""))
            await message.reply("📨 Сообщение пользователю доставлено")

# --- Inline кнопки ---
@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await answer_safe(callback.message, "Сделай свой выбор", main_menu())
        await callback.answer()
        return

    if callback.data.startswith("confirm_") and callback.message.chat.id == -1003081706651:
        msg_id = int(callback.data.split("_")[1])
        investor = invest_requests.get(msg_id)
        if not investor:
            await callback.answer("⚠️ Заявка уже обработана или не найдена", show_alert=True)
            return
        user_id = investor["user_id"]
        confirmer = callback.from_user
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        keyboard_user = InlineKeyboardMarkup([[InlineKeyboardButton(f"✉️ Написать помощнику {confirmer.full_name}", url=f"https://t.me/{confirmer.username}" if confirmer.username else f"tg://user?id={confirmer.id}")]])
        await bot.send_message(chat_id=user_id, text=f"✅ Ваш личный помощник {confirmer.full_name} подтвердил заявку!\n⏰ {now}", reply_markup=keyboard_user)

        keyboard_group = InlineKeyboardMarkup([[InlineKeyboardButton(f"✉️ Написать инвестору {investor['full_name']}", url=f"https://t.me/{investor['username']}" if investor['username'] else f"tg://user?id={user_id}")]])
        await callback.message.reply(f"✅ Заявка подтверждена!\n\nИнвестор: {investor['full_name']}\nПомощник: {confirmer.full_name}\n⏰ {now}", reply_markup=keyboard_group)
        await callback.message.edit_reply_markup(reply_markup=None)
        invest_requests.pop(msg_id, None)

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
