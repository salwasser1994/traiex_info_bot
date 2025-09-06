import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Токен бота
TOKEN = "ТВОЙ_ТОКЕН_ЗДЕСЬ"

# Создаем бота
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

# Тестовые вопросы
test_questions = [
    {
        "q": "Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
        "options": [
            "Инструмент, способный анализировать данные",
            "Автоматический эксперт, который предсказывает будущее"
        ],
        "correct": "Инструмент, способный анализировать данные"
    },
    {
        "q": "Как ИИ может помочь в анализе рынка?",
        "options": [
            "Быстро обрабатывать новости, отчёты и данные",
            "Полностью заменить человека и принимать все решения"
        ],
        "correct": "Быстро обрабатывать новости, отчёты и данные"
    },
    {
        "q": "Какую роль играет ИИ в автоматизации торговли?",
        "options": [
            "ИИ полностью устраняет человеческий контроль",
            "ИИ может автоматизировать исполнение стратегий"
        ],
        "correct": "ИИ может автоматизировать исполнение стратегий"
    },
    {
        "q": "Какую из этих задач ИИ выполняет эффективно в инвестициях?",
        "options": [
            "Выявление мошеннических схем и предупреждение о рисках",
            "Обеспечение полной гарантии прибыли"
        ],
        "correct": "Выявление мошеннических схем и предупреждение о рисках"
    },
    {
        "q": "Что является ключевым фактором при использовании ИИ в инвестициях?",
        "options": [
            "Полностью довериться алгоритмам",
            "Понимание ограничений ИИ и контроль стратегии"
        ],
        "correct": "Понимание ограничений ИИ и контроль стратегии"
    }
]

user_progress = {}

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def faq_menu():
    keyboard = [[KeyboardButton(text=q)] for q in faq_data.keys()]
    keyboard.append([KeyboardButton(text="🔙 Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Отправка вопроса с inline-кнопками
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    text = f"{q['q']}\n\n{q['options'][0]}   {q['options'][1]}"
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text=q['options'][0], callback_data=f"{idx}_0"),
        InlineKeyboardButton(text=q['options'][1], callback_data=f"{idx}_1")
    )
    await message.answer(text, reply_markup=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Сделай выбор:", reply_markup=main_menu())

# Обработка нажатий меню
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "📄 Просмотр договора оферты":
        await message.answer("Документ оферты")
    elif message.text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")
    elif message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите вопрос:", reply_markup=faq_menu())
    elif message.text in faq_data:
        await message.answer(faq_data[message.text], reply_markup=faq_menu())
    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer(
            "📘 Инструкция:\nВыберите один правильный ответ на каждый вопрос.\nИИ — это инструмент, а не волшебная палочка.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="🚀 Начать тест")]], resize_keyboard=True
            )
        )
    elif message.text == "🚀 Начать тест":
        user_progress[message.from_user.id] = 0
        await send_test_question(message, 0)
    elif message.text == "🔙 Назад в меню":
        await message.answer("Главное меню:", reply_markup=main_menu())
    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Обработка inline-кнопок для теста
@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_progress:
        await callback.answer()
        return
    idx = user_progress[user_id]
    q = test_questions[idx]
    choice = int(callback.data.split("_")[1])
    selected = q["options"][choice]

    if selected == q["correct"]:
        await callback.message.answer("✅ Правильно!")
        idx += 1
        if idx < len(test_questions):
            user_progress[user_id] = idx
            await send_test_question(callback.message, idx)
        else:
            await callback.message.answer("🎉 Тест завершён!", reply_markup=main_menu())
            del user_progress[user_id]
    # неправильный ответ — молчим
    await callback.answer()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
