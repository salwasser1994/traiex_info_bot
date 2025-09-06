import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

TOKEN = "ВАШ_ТОКЕН"

bot = Bot(token=TOKEN, parse_mode="HTML")
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
            "ИИ полностью устраняет необходимость в человеческом контроле",
            "ИИ может автоматизировать исполнение торговых стратегий"
        ],
        "correct": "ИИ может автоматизировать исполнение торговых стратегий"
    },
    {
        "q": "Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
        "options": [
            "Выявление мошеннических схем и предупреждение о рисках",
            "Обеспечение полной гарантии прибыли"
        ],
        "correct": "Выявление мошеннических схем и предупреждение о рисках"
    },
    {
        "q": "Что является ключевым фактором при использовании ИИ в инвестициях?",
        "options": [
            "Полностью довериться алгоритмам и не вмешиваться",
            "Постоянный контроль и корректировка стратегии на основе анализа"
        ],
        "correct": "Постоянный контроль и корректировка стратегии на основе анализа"
    },
    {
        "q": "Можно ли рассматривать ИИ как 'рычаг' в инвестициях?",
        "options": [
            "Да, ИИ усиливает возможности инвестора",
            "Нет, ИИ не влияет на результаты"
        ],
        "correct": "Да, ИИ усиливает возможности инвестора"
    }
]

user_progress = {}

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton("📊 Общая картина"), KeyboardButton("📝 Пройти тест")],
        [KeyboardButton("💰 Готов инвестировать"), KeyboardButton("📄 Просмотр договора оферты")],
        [KeyboardButton("✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton("Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# FAQ меню
def faq_menu():
    keyboard = [[KeyboardButton(q)] for q in faq_data.keys()]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Отправка вопроса с inline-кнопками в один ряд
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    await message.answer(q["q"])
    keyboard = InlineKeyboardMarkup(row_width=2)
    for opt in q["options"]:
        keyboard.add(InlineKeyboardButton(text=opt, callback_data=f"{idx}|{opt}"))
    await message.answer("Выберите вариант:", reply_markup=keyboard)

# /start
@dp.message(Command(commands=["start"]))
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать!", reply_markup=main_menu())

# Обработка кнопок меню
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите вопрос:", reply_markup=faq_menu())
    elif message.text in faq_data:
        await message.answer(faq_data[message.text])
    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer(
            "Инструкция:\nВыберите один правильный ответ на каждый вопрос.\nИИ — это инструмент, а не волшебная палочка."
        )
    elif message.text == "📝 Пройти тест" or message.text == "✨ Невозможное возможно благодаря рычагам":
        user_progress[message.from_user.id] = 0
        await send_test_question(message, 0)

# Обработка inline-кнопок теста
@dp.callback_query()
async def handle_test_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    idx_str, answer = callback.data.split("|")
    idx = int(idx_str)
    correct = test_questions[idx]["correct"]
    
    if answer == correct:
        await callback.message.answer("✅ Правильно!")
        idx += 1
        if idx < len(test_questions):
            user_progress[user_id] = idx
            await send_test_question(callback.message, idx)
        else:
            await callback.message.answer("🎉 Тест завершён!", reply_markup=main_menu())
            del user_progress[user_id]
    else:
        await callback.message.answer("❌ Неверно. Попробуйте следующий вопрос.")
        idx += 1
        if idx < len(test_questions):
            user_progress[user_id] = idx
            await send_test_question(callback.message, idx)
        else:
            await callback.message.answer("🎉 Тест завершён!", reply_markup=main_menu())
            del user_progress[user_id]
    await callback.answer()

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
