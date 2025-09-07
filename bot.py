import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# -------------------- Настройка бота --------------------
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

# -------------------- FAQ --------------------
faq_data = {
    "Безопасно ли пользоваться платформой?":
        "Да, все операции проходят через защищённое соединение. 🔒 Ваши данные и средства защищены.",
    "Что будет, если я потеряю доступ к аккаунту?":
        "Вы сможете восстановить доступ через e-mail или поддержку — ваш аккаунт не пропадёт.",
    "Нужно ли платить, чтобы начать?":
        "Нет, регистрация бесплатная. 🚀 Можно изучить материалы и только потом решать.",
    "Есть ли скрытые комиссии?":
        "Нет, все комиссии прозрачные и заранее указаны. 💰",
    "Можно ли вывести деньги в любой момент?":
        "Да, средства доступны для вывода без заморозки и обязательных сроков.",
    "А если я ничего не понимаю в инвестициях?":
        "Не страшно 🙂 Всё сделано, чтобы даже новичок смог разобраться.",
    "Что, если платформа перестанет работать?":
        "Используем резервные сервера и проверенные механизмы. Деньги остаются у вас.",
    "Нужно ли тратить много времени?":
        "Достаточно уделять несколько минут в день для проверки и управления счетом.",
    "Есть ли гарантии?":
        "Прозрачность, безопасность и честная работа гарантированы."
}

# -------------------- Тестовые вопросы --------------------
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
            "ИИ может автоматизировать исполнение торговых стратегий, обеспечивая быструю и точную торговлю."
        ],
        "correct": "ИИ может автоматизировать исполнение торговых стратегий, обеспечивая быструю и точную торговлю."
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
            "Полностью довериться алгоритмам и не вмешиваться.",
            "Постоянный контроль и корректировка стратегии на основе опыта."
        ],
        "correct": "Постоянный контроль и корректировка стратегии на основе опыта."
    }
]

# -------------------- Пользовательский прогресс --------------------
user_progress = {}
user_state = {}

# -------------------- Клавиатуры --------------------
def main_menu():
    keyboard = [
        [KeyboardButton("📊 Общая картина"), KeyboardButton("📝 Пройти тест")],
        [KeyboardButton("💰 Готов инвестировать"), KeyboardButton("📄 Просмотр договора оферты")],
        [KeyboardButton("✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton("Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def faq_menu():
    keyboard = [[KeyboardButton(text=q)] for q in faq_data.keys()]
    keyboard.append([KeyboardButton("⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def start_test_menu():
    keyboard = [
        [KeyboardButton("🚀 Начать тест")],
        [KeyboardButton("⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def send_test_question_keyboard(q):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(opt)] for opt in q["options"]] + [[KeyboardButton("⬅ Назад в меню")]],
        resize_keyboard=True
    )
    return keyboard

def inline_back_to_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton("В меню", callback_data="back_to_menu")]]
    )
    return keyboard

# -------------------- /start --------------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🤖 Привет! Добро пожаловать в будущее инвестиций! 💎\n\n"
        "Выбирай опции ниже и исследуй возможности AI и финансовых инструментов.",
        reply_markup=main_menu()
    )

# -------------------- Inline callback --------------------
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор 👇", reply_markup=main_menu())
        await callback.answer()

# -------------------- Обработка сообщений --------------------
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # Общая картина
    if message.text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text = (
            "📈 Чтобы увидеть финансовую картину целиком:\n\n"
            "Каждая цифра имеет значение. AI поможет выделить тренды и показать потенциал роста."
        )
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]],
            resize_keyboard=True
        )
        await message.answer(text, reply_markup=keyboard)

    elif user_state.get(user_id) == "step1" and message.text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]],
            resize_keyboard=True
        )
        await message.answer_photo(
            photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
            reply_markup=keyboard
        )

    elif user_state.get(user_id) == "step2" and message.text == "Далее➡":
        del user_state[user_id]
        text = (
            "✨ Видишь потенциал? Использование AI + сложного процента даёт реальные результаты.\n\n"
            "Начни действовать сегодня, чтобы завтра твой капитал рос быстрее!"
        )
        await message.answer(text, reply_markup=main_menu())

    # Просмотр договора
    elif message.text == "📄 Просмотр договора оферты":
        await message.answer_document("BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ")

    # Готов инвестировать
    elif message.text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")

    # FAQ
    elif message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())

    elif message.text in faq_data:
        await message.answer(f"💡 AI подсказка:\n{faq_data[message.text]}")

    # Тест
    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer(
            "📘 Выбери правильный ответ на каждый вопрос. AI всегда рядом с тобой!",
            reply_markup=start_test_menu()
        )

    elif message.text == "🚀 Начать тест":
        user_progress[user_id] = 0
        await message.answer(
            test_questions[0]["q"],
            reply_markup=send_test_question_keyboard(test_questions[0])
        )

    elif user_id in user_progress:
        idx = user_progress[user_id]
        q = test_questions[idx]
        if message.text == q["correct"]:
            await message.answer("✅ Правильно! 🚀")
            idx += 1
            if idx < len(test_questions):
                user_progress[user_id] = idx
                await message.answer(
                    test_questions[idx]["q"],
                    reply_markup=send_test_question_keyboard(test_questions[idx])
                )
            else:
                await message.answer("🎉 Тест завершён!", reply_markup=main_menu())
                del user_progress[user_id]
        elif message.text == "⬅ Назад в меню":
            await message.answer("Возврат в главное меню 👇", reply_markup=main_menu())
            del user_progress[user_id]

    # Назад в меню
    elif message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# -------------------- Запуск бота --------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
