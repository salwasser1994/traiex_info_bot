import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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

# Тест
test_questions = [
    {
        "question": "1. Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
        "options": ["А) Инструмент, способный анализировать огромные объемы данных...", 
                    "B) Автоматический эксперт, который гарантированно предсказывает будущее..."],
        "correct": "А) Инструмент, способный анализировать огромные объемы данных..."
    },
    {
        "question": "2. Как ИИ может помочь в анализе рынка?",
        "options": ["А) ИИ может быстро обрабатывать информацию о новостях, финансовых отчетах...", 
                    "B) ИИ способен заменить человеческий опыт и интуицию..."],
        "correct": "А) ИИ может быстро обрабатывать информацию о новостях, финансовых отчетах..."
    },
    {
        "question": "3. Какую роль играет ИИ в автоматизации торговли?",
        "options": ["A) ИИ полностью устраняет необходимость в человеческом контроле...", 
                    "B) ИИ может автоматизировать исполнение торговых стратегий..."],
        "correct": "B) ИИ может автоматизировать исполнение торговых стратегий..."
    },
    {
        "question": "4. Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
        "options": ["А) Выявление мошеннических схем и предупреждение о потенциальных рисках.", 
                    "B) Обеспечение полной гарантии прибыли..."],
        "correct": "А) Выявление мошеннических схем и предупреждение о потенциальных рисках."
    },
    {
        "question": "5. Что является ключевым фактором при использовании ИИ в инвестициях?",
        "options": ["A) Полностью довериться алгоритмам и не вмешиваться в процесс.", 
                    "B) Понимание ограничений ИИ, постоянный контроль..."],
        "correct": "B) Понимание ограничений ИИ, постоянный контроль..."
    },
    {
        "question": "6. Можно ли рассматривать ИИ как 'рычаг' в инвестициях?",
        "options": ["А) Да, ИИ может значительно усилить возможности инвестора...", 
                    "B) Нет, ИИ - это лишь сложная программа..."],
        "correct": "А) Да, ИИ может значительно усилить возможности инвестора..."
    }
]

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
    keyboard = [[KeyboardButton(text=q)] for q in faq_data.keys()]
    keyboard.append([KeyboardButton(text="🔙 Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Клавиатура для теста
def test_keyboard(options):
    keyboard = [[KeyboardButton(text=opt)] for opt in options]
    keyboard.append([KeyboardButton(text="🔙 Назад в меню")])  # кнопка всегда под вариантами
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Inline-кнопка "В меню"
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

# Обработка inline-кнопки "В меню"
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()

# Хранение состояния пользователя (текущий вопрос)
user_state = {}

# Обработка нажатий меню (ReplyKeyboard)
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if message.text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)

    elif message.text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")

    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        # Начало теста
        user_state[user_id] = 0  # первый вопрос
        await message.answer("Инструкция: Выберите один правильный ответ на каждый вопрос. Помните, ИИ - это инструмент, а не волшебная палочка.")
        options = test_questions[0]["options"]
        await message.answer(test_questions[0]["question"], reply_markup=test_keyboard(options))

    elif message.text in [opt for q in test_questions for opt in q["options"]]:
        current_index = user_state.get(user_id, 0)
        correct_answer = test_questions[current_index]["correct"]
        if message.text == correct_answer:
            # переход к следующему вопросу или конец
            user_state[user_id] += 1
            if user_state[user_id] < len(test_questions):
                next_q = test_questions[user_state[user_id]]
                await message.answer(next_q["question"], reply_markup=test_keyboard(next_q["options"]))
            else:
                await message.answer("Вы завершили тест! 🎉", reply_markup=main_menu())
                user_state[user_id] = 0
        else:
            # Пока ничего не делать при неправильном ответе
            pass

    elif message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())

    elif message.text in faq_data:
        await message.answer(faq_data[message.text], reply_markup=faq_menu())

    elif message.text == "🔙 Назад в меню":
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        user_state[user_id] = 0

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
