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
            "Инструмент, способный анализировать огромные объемы данных, выявлять закономерности и помогать принимать более обоснованные инвестиционные решения.",
            "Автоматический эксперт, который гарантированно предсказывает будущее и обеспечивает прибыль без усилий со стороны инвестора."
        ],
        "correct": "Инструмент, способный анализировать огромные объемы данных, выявлять закономерности и помогать принимать более обоснованные инвестиционные решения."
    },
    {
        "q": "Как ИИ может помочь в анализе рынка?",
        "options": [
            "ИИ может быстро обрабатывать информацию о новостях, финансовых отчетах и исторических данных, чтобы выявить тренды и оценить риски.",
            "ИИ способен заменить человеческий опыт и интуицию, принимая все инвестиционные решения за инвестора."
        ],
        "correct": "ИИ может быстро обрабатывать информацию о новостях, финансовых отчетах и исторических данных, чтобы выявить тренды и оценить риски."
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
            "Понимание ограничений ИИ, постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
        ],
        "correct": "Понимание ограничений ИИ, постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
    },
    {
        "q": "Можно ли рассматривать ИИ как 'рычаг' в инвестициях?",
        "options": [
            "Да, ИИ может значительно усилить возможности инвестора, позволяя ему эффективнее анализировать данные, принимать решения и управлять рисками.",
            "Нет, ИИ - это лишь сложная программа, не имеющая реального влияния на результаты инвестиций."
        ],
        "correct": "Да, ИИ может значительно усилить возможности инвестора, позволяя ему эффективнее анализировать данные, принимать решения и управлять рисками."
    }
]
user_progress = {}

# Главное меню (ReplyKeyboard)
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

# Меню перед началом теста
def start_test_menu():
    keyboard = [
        [KeyboardButton(text="🚀 Начать тест")],
        [KeyboardButton(text="🔙 Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Отправка вопроса
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q["options"]] + [[KeyboardButton(text="🔙 Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(q["q"], reply_markup=keyboard)

# Inline-кнопка "В меню"
def inline_back_to_menu():
    keyboard = [
        [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(
        video=file_id,
        reply_markup=inline_back_to_menu()
    )

# Обработка inline-кнопки "В меню"
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()

# Обработка нажатий меню (ReplyKeyboard)
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)

    elif message.text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")

    elif message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())

    elif message.text in faq_data:
        await message.answer(faq_data[message.text], reply_markup=faq_menu())

    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        instruction = (
            "📘 Инструкция:\n\n"
            "Выберите один правильный ответ на каждый вопрос.\n"
            "Помните, ИИ — это инструмент, а не волшебная палочка."
        )
        await message.answer(instruction, reply_markup=start_test_menu())

    elif message.text == "🚀 Начать тест":
        user_progress[message.from_user.id] = 0
        await send_test_question(message, 0)

    elif message.from_user.id in user_progress:
        idx = user_progress[message.from_user.id]
        q = test_questions[idx]
        if message.text == q["correct"]:
            await message.answer("✅ Правильно!")
            idx += 1
            if idx < len(test_questions):
                user_progress[message.from_user.id] = idx
                await send_test_question(message, idx)
            else:
                await message.answer("🎉 Тест завершён!", reply_markup=main_menu())
                del user_progress[message.from_user.id]
        elif message.text == "🔙 Назад в меню":
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            del user_progress[message.from_user.id]
        else:
            # неправильный ответ — молчим
            pass

    elif message.text == "🔙 Назад в меню":
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
