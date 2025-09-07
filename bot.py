import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# --- FAQ с AI-подсказками ---
faq_data = {
    "Безопасно ли пользоваться платформой?": "Да, все операции защищены 🔒. Ваши данные и средства надежно охраняются 🤖.",
    "Что будет, если я потеряю доступ к аккаунту?": "Восстановление через e-mail или поддержку. Ваши активы под контролем 🛡️.",
    "Нужно ли платить, чтобы начать?": "Регистрация бесплатная 🚀. Попробуйте, убедитесь сами!",
    "Есть ли скрытые комиссии?": "Нет, все прозрачно 💎. Вы знаете, сколько и за что платите.",
    "Можно ли вывести деньги в любой момент?": "Да, средства доступны всегда 💰. Без заморозок и условий.",
    "А если я ничего не понимаю в инвестициях?": "Не переживайте 🙂. Есть инструкции, видеоуроки и поддержка AI 🤖.",
    "Что, если платформа перестанет работать?": "Резервные серверы и проверенные механизмы 🛰️. Деньги в безопасности.",
    "Нужно ли тратить много времени?": "Хватит нескольких минут в день ⏱️ для контроля и роста.",
    "Есть ли гарантии?": "Прозрачность, безопасность и честность 💎. Прибыль зависит от вашего участия."
}

# --- Тестовые вопросы ---
test_questions = [
    {
        "q": "Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
        "options": ["Инструмент, способный анализировать огромные объемы данных.", "Автоматический эксперт, который гарантированно предсказывает будущее."],
        "correct": "Инструмент, способный анализировать огромные объемы данных."
    },
    {
        "q": "Как ИИ может помочь в анализе рынка?",
        "options": ["Быстро обрабатывать новости, отчёты и данные, выявляя тренды.", "Полностью заменить человека и принимать все решения."],
        "correct": "Быстро обрабатывать новости, отчёты и данные, выявляя тренды."
    },
    {
        "q": "Какую роль играет ИИ в автоматизации торговли?",
        "options": ["ИИ полностью устраняет необходимость в человеческом контроле, автоматически генерируя прибыль.", "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."],
        "correct": "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."
    },
    {
        "q": "Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
        "options": ["Выявление мошеннических схем и предупреждение о потенциальных рисках.", "Обеспечение полной гарантии прибыли, независимо от рыночной ситуации."],
        "correct": "Выявление мошеннических схем и предупреждение о потенциальных рисках."
    },
    {
        "q": "Что является ключевым фактором при использовании ИИ в инвестициях?",
        "options": ["Полностью довериться алгоритмам и не вмешиваться в процесс.", "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."],
        "correct": "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
    }
]

user_progress = {}
user_state = {}

# --- Главное меню футуристическое ---
def main_menu():
    keyboard = [
        [KeyboardButton("📊 Общая картина"), KeyboardButton("📝 Пройти тест")],
        [KeyboardButton("💰 Готов инвестировать"), KeyboardButton("📄 Договор оферты")],
        [KeyboardButton("✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton("🤖 FAQ с AI-подсказками")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- FAQ меню ---
def faq_menu():
    keyboard = [[KeyboardButton(f"💡 {q}")] for q in faq_data.keys()]
    keyboard.append([KeyboardButton("⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню теста с футуристикой ---
def start_test_menu():
    keyboard = [
        [KeyboardButton("🚀 Начать тест")],
        [KeyboardButton("⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Отправка вопроса с прогрессом ---
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    progress = "⚡" * (idx + 1) + "·" * (len(test_questions) - idx - 1)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(opt)] for opt in q["options"]] + [[KeyboardButton("⬅ Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(f"🔹 {q['q']}\nПрогресс: {progress}", reply_markup=keyboard)

# --- Inline кнопка назад ---
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton("В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- /start ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👽 Добро пожаловать в будущее инвестиций! Выбирай действие ниже 👇", reply_markup=main_menu())

# --- Inline callback ---
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()

# --- Обработка сообщений ---
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # --- Общая картина ---
    if message.text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text1 = "🔹 Чтобы увидеть всю финансовую картину, смотри глазами и аналитикой AI 🤖:\n"
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]], resize_keyboard=True)
        await message.answer(text1, reply_markup=keyboard)

    elif user_state.get(user_id) == "step1" and message.text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]], resize_keyboard=True)
        await message.answer_photo(photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE", reply_markup=keyboard)

    elif user_state.get(user_id) == "step2" and message.text == "Далее➡":
        del user_state[user_id]
        text2 = "💎 Основные выводы:\n— Делай или ничего — выбор за тобой.\n— Используй AI + сложный процент, чтобы ускорить рост 💹."
        await message.answer(text2, reply_markup=main_menu())

    # --- FAQ ---
    elif message.text.startswith("💡") and message.text[2:] in faq_data:
        q = message.text[2:]
        await message.answer(f"🤖 AI подсказка:\n{faq_data[q]}")

    elif message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        user_progress.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())

    # --- Тест ---
    elif message.text == "🚀 Начать тест":
        user_progress[user_id] = 0
        await send_test_question(message, 0)

    elif user_id in user_progress:
        idx = user_progress[user_id]
        q = test_questions[idx]
        if message.text == q["correct"]:
            await message.answer("✅ Правильно! ⚡")
            idx += 1
            if idx < len(test_questions):
                user_progress[user_id] = idx
                await send_test_question(message, idx)
            else:
                await message.answer("🎉 Тест завершён! Добро пожаловать в мир инвестиций 🚀", reply_markup=main_menu())
                del user_progress[user_id]
        elif message.text == "⬅ Назад в меню":
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            del user_progress[user_id]
        else:
            await message.answer("❌ Неправильно. Попробуй снова 💡")

    # --- Другие кнопки ---
    elif message.text == "💰 Готов инвестировать":
        await message.answer("Начни прямо сейчас 👉 https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")

    elif message.text == "📄 Договор оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)

    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer("📘 Инструкция: Выберите один правильный ответ на каждый вопрос. AI поможет вам 🛠️", reply_markup=start_test_menu())

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
