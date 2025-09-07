import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Токен бота
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# Создаем бота с правильным parse_mode
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# FAQ с небольшими AI подсказками
faq_data = {
    "Безопасно ли пользоваться платформой?":
        "✅ Да, все операции защищены. 🤖 AI советует: всегда проверяйте ссылки и сертификаты!",
    "Что будет, если я потеряю доступ к аккаунту?":
        "🔑 Вы сможете восстановить доступ через e-mail или поддержку. AI напоминает: используйте сложный пароль!",
    "Нужно ли платить, чтобы начать?":
        "💸 Нет, регистрация бесплатная. AI советует: сначала изучите платформу!",
    "Есть ли скрытые комиссии?":
        "🧐 Нет, все комиссии прозрачные. AI рекомендует: читайте договор внимательно.",
    "Можно ли вывести деньги в любой момент?":
        "💰 Да, без заморозки. AI напоминает: всегда планируйте бюджет!",
    "А если я ничего не понимаю в инвестициях?":
        "😎 Всё просто! Есть инструкции, видеоуроки и поддержка. AI советует: учитесь постепенно.",
    "Что, если платформа перестанет работать?":
        "🛡️ Используем резервные сервера. AI рекомендует: не храните всё на одной платформе.",
    "Нужно ли тратить много времени?":
        "⏱️ Достаточно нескольких минут в день. AI напоминает: регулярность важнее объема.",
    "Есть ли гарантии?":
        "⚖️ Гарантия прозрачности и честной работы. AI советует: диверсифицируйте риски."
}

# Тестовые вопросы с шагами
test_questions = [
    {
        "q": "Что такое Искусственный Интеллект (ИИ) в инвестициях?",
        "options": [
            "📊 Инструмент для анализа данных",
            "🔮 Автоматический эксперт, предсказывающий будущее"
        ],
        "correct": "📊 Инструмент для анализа данных"
    },
    {
        "q": "Как ИИ помогает анализу рынка?",
        "options": [
            "⚡ Быстро обрабатывать новости и отчёты",
            "👤 Полностью заменить человека"
        ],
        "correct": "⚡ Быстро обрабатывать новости и отчёты"
    },
    {
        "q": "Роль ИИ в автоматизации торговли?",
        "options": [
            "🤖 Устраняет контроль человека и генерирует прибыль",
            "🚀 Автоматизирует стратегию по заданным параметрам"
        ],
        "correct": "🚀 Автоматизирует стратегию по заданным параметрам"
    },
    {
        "q": "Какие задачи ИИ выполняет эффективно?",
        "options": [
            "🔍 Выявление мошеннических схем",
            "💵 Обеспечение полной гарантии прибыли"
        ],
        "correct": "🔍 Выявление мошеннических схем"
    },
    {
        "q": "Ключевой фактор при использовании ИИ?",
        "options": [
            "🛑 Полностью довериться алгоритмам",
            "🎯 Постоянный контроль и корректировка стратегии"
        ],
        "correct": "🎯 Постоянный контроль и корректировка стратегии"
    }
]

user_progress = {}
user_state = {}

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton("📊 Общая картина"), KeyboardButton("📝 Пройти тест")],
        [KeyboardButton("💰 Готов инвестировать"), KeyboardButton("📄 Просмотр договора оферты")],
        [KeyboardButton("✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton("❓ Часто задаваемые вопросы")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Меню FAQ
def faq_menu():
    keyboard = [[KeyboardButton(q)] for q in faq_data.keys()]
    keyboard.append([KeyboardButton("⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Меню перед тестом
def start_test_menu():
    keyboard = [
        [KeyboardButton("🚀 Начать тест")],
        [KeyboardButton("⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Отправка вопроса с прогрессом
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    total = len(test_questions)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(opt)] for opt in q["options"]] + [[KeyboardButton("⬅ Назад в меню")]],
        resize_keyboard=True
    )
    step = f"🛸 Шаг {idx+1}/{total}"
    await message.answer(f"{step}\n\n{q['q']}", reply_markup=keyboard)

# Inline кнопка "В меню"
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton("В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Добро пожаловать в будущий мир инвестиций!\nВыберите действие:", reply_markup=main_menu())

# Обработка inline кнопки
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор 👇", reply_markup=main_menu())
        await callback.answer()

# Основная логика бота
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Общая картина
    if text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text1 = (
            "🌌 Чтобы увидеть всю финансовую картину, используем взгляд и интеллект AI.\n"
            "💡 Таблицы подсвечивают реальное положение дел:"
        )
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]], resize_keyboard=True)
        await message.answer(text1, reply_markup=keyboard)

    elif user_state.get(user_id) == "step1" and text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]], resize_keyboard=True)
        await message.answer_photo(
            photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
            reply_markup=keyboard
        )

    elif user_state.get(user_id) == "step2" and text == "Далее➡":
        del user_state[user_id]
        text2 = (
            "🚀 Таблица на примерных цифрах:\n"
            "— Если ничего не делать: один результат\n"
            "— Если делать частично: другой результат\n"
            "— Используя AI + сложный процент: быстрый рост капитала\n"
            "💎 Важно видеть всю картину целиком!"
        )
        await message.answer(text2, reply_markup=main_menu())

    # Просмотр договора
    elif text == "📄 Просмотр договора оферты":
        await message.answer_document("BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ")

    # Инвестировать
    elif text == "💰 Готов инвестировать":
        await message.answer("🌟 Начни свой путь здесь:\nhttps://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")

    # FAQ
    elif text == "❓ Часто задаваемые вопросы":
        await message.answer("Выберите вопрос:", reply_markup=faq_menu())
    elif text in faq_data:
        await message.answer(f"🤖 AI Подсказка: {faq_data[text]}")

    # Тест
    elif text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer("📘 Инструкция: Выберите правильный ответ на каждый вопрос.\nAI будет помогать.", reply_markup=start_test_menu())
    elif text == "🚀 Начать тест":
        user_progress[user_id] = 0
        await send_test_question(message, 0)
    elif user_id in user_progress:
        idx = user_progress[user_id]
        q = test_questions[idx]
        if text == q["correct"]:
            await message.answer("✅ Верно!")
            idx += 1
            if idx < len(test_questions):
                user_progress[user_id] = idx
                await send_test_question(message, idx)
            else:
                await message.answer("🎉 Тест завершён!", reply_markup=main_menu())
                del user_progress[user_id]
        elif text == "⬅ Назад в меню":
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            del user_progress[user_id]

    # Кнопка назад
    elif text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
