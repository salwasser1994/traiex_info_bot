import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# Токен бота
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# Создаем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Вопросы и ответы FAQ
faq_data = {
    "Безопасно ли пользоваться платформой?":
        "Да, все операции проходят через защищённое соединение, ваши данные и средства надёжно защищены.",

    "Что будет, если я потеряю доступ к аккаунту?":
        "Вы сможете восстановить доступ через e-mail или поддержку — ваш аккаунт не пропадёт.",

    "Нужно ли платить, чтобы начать?":
        "Нет, регистрация бесплатная. Вы можете изучить все материалы и только потом принять решение о вложениях.",

    "Есть ли скрытые комиссии?":
        "Нет, все комиссии прозрачные и заранее указаны. Вы всегда знаете, сколько и за что платите.",

    "Можно ли вывести деньги в любой момент?":
        "Да, средства доступны для вывода по вашему желанию, без «заморозки» и обязательных сроков.",

    "А если я ничего не понимаю в инвестициях?":
        "Не страшно 🙂 Всё построено так, чтобы даже новичок мог разобраться. Есть инструкции, видеоуроки и поддержка.",

    "Что, если платформа перестанет работать?":
        "Мы используем резервные сервера и проверенные механизмы. Даже в случае сбоя деньги остаются у вас.",

    "Нужно ли тратить много времени?":
        "Нет, достаточно уделять несколько минут в день для проверки информации и управления своим счётом.",

    "Есть ли гарантии?":
        "Мы не обещаем «золотых гор», но гарантируем прозрачность, безопасность и честную работу платформы."
}

# --- Тестовые вопросы ---
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

user_progress = {}
user_state = {}

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Меню FAQ
def faq_menu():
    keyboard = [[KeyboardButton(text="⬅ Назад в меню")]]
    keyboard += [[KeyboardButton(text=q)] for q in faq_data.keys()]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Меню перед тестом
def start_test_menu():
    keyboard = [
        [KeyboardButton(text="🚀 Начать тест")],
        [KeyboardButton(text="⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Отправка вопроса (кнопки в столбик + назад внизу)
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q["options"]] + [[KeyboardButton(text="⬅ Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(q["q"], reply_markup=keyboard)

# Inline кнопка "В меню"
def inline_back_to_menu():
    keyboard = [
        [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Итог после теста
def test_result_menu():
    keyboard = [
        [KeyboardButton(text="💰 Готов инвестировать")],
        [KeyboardButton(text="🙅‍♂️ Не готов")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(
        video=file_id,
        reply_markup=inline_back_to_menu()
    )

# Callback обработчик
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()

# Обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if message.text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text1 = (
            "Чтобы увидеть всю финансовую картину целиком и полностью, нужно смотреть не только глазами, "
            "но и через таблицы, которые покажут все цифры.\n\n"
            "Итак, вот данные:"
        )
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню")], [KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        await message.answer(text1, reply_markup=keyboard)

    elif user_state.get(user_id) == "step1" and message.text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню")], [KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        await message.answer_photo(
            photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
            reply_markup=keyboard
        )

    elif user_state.get(user_id) == "step2" and message.text == "Далее➡":
        del user_state[user_id]
        text2 = (
            "Примерный прогноз роста капитала с использованием ИИ и сложного процента:\n\n"
            "📈 1-й год: +45%\n"
            "📈 2-й год: +120%\n"
            "📈 3-й год: +250%\n\n"
            "Эти цифры условные, но показывают суть: чем дольше вы работаете с системой, "
            "тем быстрее растёт капитал."
        )
        await message.answer(text2, reply_markup=main_menu())

    elif message.text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)

    elif message.text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")

    elif message.text == "🙅‍♂️ Не готов":
        await message.answer("Хорошо, возвращаю вас в главное меню 👇", reply_markup=main_menu())

    elif message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())

    elif message.text in faq_data:
        await message.answer(faq_data[message.text])

    elif message.text == "✨ Невозможное возможно благодаря рычагам" or message.text == "📝 Пройти тест":
        instruction = (
            "📘 Инструкция:\n\n"
            "Выберите один правильный ответ на каждый вопрос.\n"
            "Помните, ИИ — это инструмент, а не волшебная палочка."
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
                del user_progress[user_id]
                result_text = (
                    "🎉 Тест завершён!\n\n"
                    "Вот как это может выглядеть на практике:\n\n"
                    "📊 1-й год: +35%\n"
                    "📊 2-й год: +95%\n"
                    "📊 3-й год: +210%\n\n"
                    "Чем дольше используете систему, тем выше результат.\n\n"
                    "Готовы сделать шаг?"
                )
                await message.answer(result_text, reply_markup=test_result_menu())
        elif message.text == "⬅ Назад в меню":
            del user_progress[user_id]
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        else:
            await message.answer("❌ Неправильно, попробуйте ещё раз.")

    elif message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        user_progress.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
