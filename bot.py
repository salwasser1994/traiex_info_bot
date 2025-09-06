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

# FAQ
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

# Inline-кнопка "В меню"
def inline_back_to_menu():
    keyboard = [
        [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Тест
test_questions = [
    {
        "question": "1. Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
        "answers": [
            "А) Инструмент, способный анализировать огромные объемы данных, выявлять закономерности и помогать принимать более обоснованные инвестиционные решения.",
            "Б) Автоматический эксперт, который гарантированно предсказывает будущее и обеспечивает прибыль без усилий со стороны инвестора."
        ],
        "correct": 0
    },
    {
        "question": "2. Как ИИ может помочь в анализе рынка?",
        "answers": [
            "А) ИИ может быстро обрабатывать информацию о новостях, финансовых отчетах и исторических данных, чтобы выявить тренды и оценить риски.",
            "Б) ИИ способен заменить человеческий опыт и интуицию, принимая все инвестиционные решения за инвестора."
        ],
        "correct": 0
    },
    {
        "question": "3. Какую роль играет ИИ в автоматизации торговли?",
        "answers": [
            "А) ИИ полностью устраняет необходимость в человеческом контроле, автоматически генерируя прибыль.",
            "Б) ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."
        ],
        "correct": 1
    },
    {
        "question": "4. Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
        "answers": [
            "А) Выявление мошеннических схем и предупреждение о потенциальных рисках.",
            "Б) Обеспечение полной гарантии прибыли, независимо от рыночной ситуации."
        ],
        "correct": 0
    },
    {
        "question": "5. Что является ключевым фактором при использовании ИИ в инвестициях?",
        "answers": [
            "А) Полностью довериться алгоритмам и не вмешиваться в процесс.",
            "Б) Понимание ограничений ИИ, постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
        ],
        "correct": 1
    },
    {
        "question": "6. Можно ли рассматривать ИИ как \"рычаг\" в инвестициях?",
        "answers": [
            "А) Да, ИИ может значительно усилить возможности инвестора, позволяя ему эффективнее анализировать данные, принимать решения и управлять рисками.",
            "Б) Нет, ИИ - это лишь сложная программа, не имеющая реального влияния на результаты инвестиций."
        ],
        "correct": 0
    }
]

# Старт /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

# Inline-кнопки
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    data = callback.data
    if data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()
    elif data.startswith("test_"):
        # формат: test_<index>_<answer_index>
        parts = data.split("_")
        q_index = int(parts[1])
        a_index = int(parts[2])
        if a_index == test_questions[q_index]["correct"]:
            # правильный ответ
            next_q = q_index + 1
            if next_q < len(test_questions):
                await send_test_question(callback.message, next_q)
            else:
                # конец теста
                await callback.message.answer("Тест завершён! 🔚", reply_markup=main_menu())
        await callback.answer()  # закрываем часики

# Отправка вопроса
async def send_test_question(message: types.Message, q_index: int):
    q = test_questions[q_index]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=a, callback_data=f"test_{q_index}_{i}")] for i, a in enumerate(q["answers"])
    ])
    await message.answer(q["question"], reply_markup=keyboard)

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
        # Инструкция перед тестом
        instruction = ("Инструкция: Выберите один правильный ответ на каждый вопрос. "
                       "Помните, ИИ - это инструмент, а не волшебная палочка.\n\n---")
        await message.answer(instruction)
        await send_test_question(message, 0)

    elif message.text == "🔙 Назад в меню":
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
