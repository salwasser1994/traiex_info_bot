import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ======================
# Токен бота
# ======================
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# ======================
# Создаем бота
# ======================
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ======================
# FAQ данные
# ======================
faq_data = {
    "Безопасно ли пользоваться платформой?":
        "✅ Да, все операции проходят через защищённое соединение, ваши данные и средства надёжно защищены.",
    "Что будет, если я потеряю доступ к аккаунту?":
        "📧 Вы сможете восстановить доступ через e-mail или поддержку — ваш аккаунт не пропадёт.",
    "Нужно ли платить, чтобы начать?":
        "💎 Нет, регистрация бесплатная. Сначала изучи материалы, потом решай о вложениях.",
    "Есть ли скрытые комиссии?":
        "🔹 Нет, все комиссии прозрачные и заранее указаны.",
    "Можно ли вывести деньги в любой момент?":
        "💰 Да, средства доступны без «заморозки» и обязательных сроков.",
    "А если я ничего не понимаю в инвестициях?":
        "🤖 Не страшно 🙂 Всё построено для новичков: инструкции, видеоуроки, поддержка.",
    "Что, если платформа перестанет работать?":
        "🛡️ Используем резервные сервера. Даже при сбое деньги остаются у вас.",
    "Нужно ли тратить много времени?":
        "⏱️ Достаточно нескольких минут в день для проверки информации.",
    "Есть ли гарантии?":
        "⚡ Мы гарантируем прозрачность, безопасность и честную работу платформы."
}

# ======================
# Тестовые вопросы
# ======================
test_questions = [
    {
        "q": "Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
        "options": [
            "Инструмент, способный анализировать огромные объемы данных.",
            "Автоматический эксперт, который гарантированно предсказывает будущее."
        ],
        "correct": "Инструмент, способный анализировать огромные объемы данных."
    },
    {
        "q": "Как ИИ может помочь в анализе рынка?",
        "options": [
            "Быстро обрабатывать новости, отчёты и данные, выявляя тренды.",
            "Полностью заменить человека и принимать все решения."
        ],
        "correct": "Быстро обрабатывать новости, отчёты и данные, выявляя тренды."
    },
    {
        "q": "Какую роль играет ИИ в автоматизации торговли?",
        "options": [
            "ИИ полностью устраняет необходимость в человеческом контроле, автоматически генерируя прибыль.",
            "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."
        ],
        "correct": "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."
    },
    {
        "q": "Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
        "options": [
            "Выявление мошеннических схем и предупреждение о потенциальных рисках.",
            "Обеспечение полной гарантии прибыли, независимо от рыночной ситуации."
        ],
        "correct": "Выявление мошеннических схем и предупреждение о потенциальных рисках."
    },
    {
        "q": "Что является ключевым фактором при использовании ИИ в инвестициях?",
        "options": [
            "Полностью довериться алгоритмам и не вмешиваться в процесс.",
            "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
        ],
        "correct": "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
    }
]

# ======================
# Пользовательские состояния
# ======================
user_progress = {}
user_state = {}

# ======================
# Главное меню
# ======================
def main_menu():
    keyboard = [
        [KeyboardButton(text="🤖 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Договор оферты")],
        [KeyboardButton(text="🔮 Невозможное возможно")],
        [KeyboardButton(text="❓ FAQ")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ======================
# FAQ меню
# ======================
def faq_menu():
    keyboard = [[KeyboardButton(text=q)] for q in faq_data.keys()]
    keyboard.append([KeyboardButton(text="⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ======================
# Меню теста
# ======================
def start_test_menu():
    keyboard = [
        [KeyboardButton(text="🚀 Начать тест")],
        [KeyboardButton(text="⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ======================
# Отправка тестового вопроса с прогрессом
# ======================
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    total = len(test_questions)
    progress = f"Вопрос {idx+1}/{total} 🔹" + "⚪"*(total-idx-1)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q["options"]] + [[KeyboardButton(text="⬅ Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(f"<b>{progress}</b>\n\n{q['q']}", reply_markup=keyboard)

# ======================
# Inline кнопка «В меню»
# ======================
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# ======================
# Старт /start
# ======================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer_video(
        video="BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ",
        caption="🤖 Добро пожаловать! Выберите действие ниже:",
        reply_markup=inline_back_to_menu()
    )

# ======================
# Обработка inline кнопки
# ======================
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор ⚡", reply_markup=main_menu())
        await callback.answer()

# ======================
# Основная логика меню
# ======================
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # -------- Общая картина --------
    if message.text == "🤖 Общая картина":
        user_state[user_id] = "step1"
        text1 = (
            "⚡ <b>Сканирование финансовой матрицы...</b> ⚡\n\n"
            "Чтобы увидеть всю картину полностью, подключаем все сенсоры и выводим данные в таблицы для анализа."
        )
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        await message.answer(text1, reply_markup=keyboard)

    elif user_state.get(user_id) == "step1" and message.text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        # Фото таблицы
        await message.answer_photo(
            photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
            caption="🖥️ Таблица показывает реальное положение дел",
            reply_markup=keyboard
        )

    elif user_state.get(user_id) == "step2" and message.text == "Далее➡":
        del user_state[user_id]
        text2 = (
            "🔹 Таблица сделана на примерных цифрах.\n\n"
            "— если ничего не делать — один результат\n"
            "— если действовать частично — другой результат\n"
            "— если использовать всё (ИИ + сложный процент) — результат оптимальный ⚡\n\n"
            "<b>Важно видеть всю картину целиком!</b>"
        )
        await message.answer(text2, reply_markup=main_menu())

    # -------- Договор оферты --------
    elif message.text == "📄 Договор оферты":
        await message.answer_document("BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ")

    # -------- Готов инвестировать --------
    elif message.text == "💰 Готов инвестировать":
        await message.answer("🚀 [Регистрация на платформе](https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex)")

    # -------- FAQ --------
    elif message.text == "❓ FAQ":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())

    elif message.text in faq_data:
        await message.answer(faq_data[message.text])

    # -------- Тест --------
    elif message.text == "🔮 Невозможное возможно":
        instruction = (
            "📘 Инструкция:\n\n"
            "Выберите один правильный ответ на каждый вопрос.\n"
            "ИИ — это инструмент, а не волшебная палочка 🤖."
        )
        await message.answer(instruction, reply_markup=start_test_menu())

    elif message.text == "🚀 Начать тест":
        user_progress[user_id] = 0
        await send_test_question(message, 0)

    elif user_id in user_progress:
        idx = user_progress[user_id]
        q = test_questions[idx]
        if message.text == q["correct"]:
            await message.answer("✅ Правильно!")
            idx += 1
            if idx < len(test_questions):
                user_progress[user_id] = idx
                await send_test_question(message, idx)
            else:
                await message.answer("🎉 Тест завершён!", reply_markup=main_menu())
                del user_progress[user_id]
        elif message.text == "⬅ Назад в меню":
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            del user_progress[user_id]
        else:
            await message.answer("❌ Неправильно. Попробуй ещё раз.")

    # -------- Назад в меню --------
    elif message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# ======================
# Запуск бота
# ======================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
