import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ======================
# Мотивационный FAQ с AI подсказками
# ======================
faq_data = {
    "Безопасно ли пользоваться платформой?":
        ("✅ Да! Все операции защищены.\n\n"
         "<i>AI совет:</i> Безопасность — твой первый шаг к успеху! 🚀"),
    "Что будет, если я потеряю доступ к аккаунту?":
        ("📧 Восстановление через e-mail или поддержку.\n\n"
         "<i>AI совет:</i> Никогда не теряй контроль, это твой щит! 🛡️"),
    "Нужно ли платить, чтобы начать?":
        ("💎 Начни бесплатно!\n\n"
         "<i>AI совет:</i> Первый шаг к богатству не требует вложений, только твоё внимание."),
    "Есть ли скрытые комиссии?":
        ("🔹 Нет! Всё прозрачно.\n\n"
         "<i>AI совет:</i> Прозрачность — ключ к ясным решениям."),
    "Можно ли вывести деньги в любой момент?":
        ("💰 Абсолютная свобода!\n\n"
         "<i>AI совет:</i> Управляй капиталом, когда хочешь — это сила!"),
    "А если я ничего не понимаю в инвестициях?":
        ("🤖 Не страшно! Мы обучим тебя шаг за шагом.\n\n"
         "<i>AI совет:</i> Новичок сегодня — эксперт завтра!"),
    "Что, если платформа перестанет работать?":
        ("🛡️ Всё под контролем!\n\n"
         "<i>AI совет:</i> Резервные серверы защищают твой путь к успеху."),
    "Нужно ли тратить много времени?":
        ("⏱️ Всего несколько минут в день.\n\n"
         "<i>AI совет:</i> Капитал растет, когда ты действуешь ежедневно!"),
    "Есть ли гарантии?":
        ("⚡ Мы гарантируем честность и прозрачность.\n\n"
         "<i>AI совет:</i> Честность = доверие + рост.")
}

# ======================
# Тест с анимацией прогресса
# ======================
test_questions = [
    {
        "q": "Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
        "options": [
            "💻 Инструмент для анализа огромных данных",
            "❌ Автоматический эксперт, который предсказывает будущее"
        ],
        "correct": "💻 Инструмент для анализа огромных данных"
    },
    {
        "q": "Как ИИ может помочь в анализе рынка?",
        "options": [
            "📈 Быстро выявлять тренды",
            "❌ Полностью заменить человека"
        ],
        "correct": "📈 Быстро выявлять тренды"
    },
    {
        "q": "Какую роль играет ИИ в автоматизации торговли?",
        "options": [
            "❌ Полностью убирает контроль человека",
            "⚡ Автоматизирует стратегию и ускоряет торговлю"
        ],
        "correct": "⚡ Автоматизирует стратегию и ускоряет торговлю"
    },
    {
        "q": "Какую задачу ИИ выполняет эффективно?",
        "options": [
            "✅ Выявление мошеннических схем",
            "❌ Гарантия прибыли"
        ],
        "correct": "✅ Выявление мошеннических схем"
    },
    {
        "q": "Ключевой фактор инвестирования с ИИ?",
        "options": [
            "❌ Полностью довериться алгоритмам",
            "💡 Контроль и корректировка на основе опыта"
        ],
        "correct": "💡 Контроль и корректировка на основе опыта"
    }
]

user_progress = {}
user_state = {}

# ======================
# Меню бота с футуристическим стилем
# ======================
def main_menu():
    keyboard = [
        [KeyboardButton("🤖 Общая картина"), KeyboardButton("📝 Пройти тест")],
        [KeyboardButton("💰 Готов инвестировать"), KeyboardButton("📄 Договор оферты")],
        [KeyboardButton("🔮 Моя инвестиционная сила")],
        [KeyboardButton("❓ FAQ")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def faq_menu():
    keyboard = [[KeyboardButton(text=q)] for q in faq_data.keys()]
    keyboard.append([KeyboardButton("⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def start_test_menu():
    keyboard = [[KeyboardButton("🚀 Начать тест")], [KeyboardButton("⬅ Назад в меню")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ======================
# Прогресс теста с эмодзи
# ======================
def progress_bar(idx, total):
    bar = "⚪" * total
    bar = bar[:idx] + "🟢" + bar[idx+1:]
    return bar

async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    total = len(test_questions)
    progress = progress_bar(idx, total)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q["options"]] + [[KeyboardButton("⬅ Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(f"<b>{progress}</b>\n\n{q['q']}", reply_markup=keyboard)

def inline_back_to_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("В меню", callback_data="back_to_menu")]])

# ======================
# /start
# ======================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer_video(
        video="BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ",
        caption="🤖 Добро пожаловать в будущее твоих инвестиций! Выбери действие ниже:",
        reply_markup=inline_back_to_menu()
    )

# ======================
# Inline кнопка
# ======================
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("⚡ Сделай свой выбор ⚡", reply_markup=main_menu())
        await callback.answer()

# ======================
# Основная логика
# ======================
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # Общая картина
    if message.text == "🤖 Общая картина":
        user_state[user_id] = "step1"
        text1 = (
            "🚀 <b>Активируем сенсоры финансового успеха...</b>\n\n"
            "Каждая цифра в таблице — это твой потенциал. Видишь картину — управляешь будущим!"
        )
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]], resize_keyboard=True)
        await message.answer(text1, reply_markup=keyboard)

    elif user_state.get(user_id) == "step1" and message.text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup([[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]], resize_keyboard=True)
        await message.answer_photo(
            photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
            caption="🖥️ Таблица твоих достижений — видишь потенциал?",
            reply_markup=keyboard
        )

    elif user_state.get(user_id) == "step2" and message.text == "Далее➡":
        del user_state[user_id]
        text2 = (
            "💡 Малые шаги создают большие результаты!\n\n"
            "— Не действовать — теряешь шанс\n"
            "— Частично действовать — результат есть\n"
            "— Использовать всё (ИИ + стратегия) — максимальный рост! ⚡\n\n"
            "<b>Твоя инвестиционная сила растёт с каждым действием!</b>"
        )
        await message.answer(text2, reply_markup=main_menu())

    # FAQ
    elif message.text == "❓ FAQ":
        await message.answer("Выбери вопрос и прокачай свои знания:", reply_markup=faq_menu())
    elif message.text in faq_data:
        await message.answer(faq_data[message.text])

    # Тест
    elif message.text == "🔮 Моя инвестиционная сила":
        await message.answer("📘 Выбери правильный ответ и почувствуй уверенность! 🤖", reply_markup=start_test_menu())
    elif message.text == "🚀 Начать тест":
        user_progress[user_id] = 0
        await send_test_question(message, 0)

    elif user_id in user_progress:
        idx = user_progress[user_id]
        q = test_questions[idx]
        if message.text == q["correct"]:
            await message.answer("✅ Отлично! Ты растёшь как инвестор!")
            idx += 1
            if idx < len(test_questions):
                user_progress[user_id] = idx
                await send_test_question(message, idx)
            else:
                await message.answer("🎉 Тест завершён! Твоя инвестиционная сила увеличена ⚡", reply_markup=main_menu())
                del user_progress[user_id]
        elif message.text == "⬅ Назад в меню":
            await message.answer("Ты вернулся в главное меню 👇", reply_markup=main_menu())
            del user_progress[user_id]
        else:
            await message.answer("❌ Неудачно, попробуй ещё раз! Твой успех близко ⚡")

    elif message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        await message.answer("Ты вернулся в главное меню 👇", reply_markup=main_menu())

    # Готов инвестировать
    elif message.text == "💰 Готов инвестировать":
        await message.answer("🚀 [Начать инвестировать сейчас!](https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex)")

    elif message.text == "📄 Договор оферты":
        await message.answer_document("BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ")

    else:
        await message.answer("Выбери действие из меню 👇", reply_markup=main_menu())

# ======================
# Запуск
# ======================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
