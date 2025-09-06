import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# Токен бота
TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"

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
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Меню перед началом теста
def start_test_menu():
    keyboard = [
        [KeyboardButton(text="🚀 Начать тест")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Отправка вопроса
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]

    # 1. Вопрос
    await message.answer(q["q"])

    # 2. Варианты текста в одном ряду
    options_text = f"A) {q['options'][0]}    B) {q['options'][1]}"
    await message.answer(options_text)

    # 3. Inline-кнопки для выбора ответа
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="A", callback_data=f"{idx}_0"),
        InlineKeyboardButton(text="B", callback_data=f"{idx}_1")
    ]
    keyboard.add(*buttons)
    await message.answer("Выберите вариант:", reply_markup=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Добро пожаловать в тест по ИИ.", reply_markup=start_test_menu())

# Обработка inline-кнопок
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    data = callback.data
    idx_str, opt_str = data.split("_")
    idx = int(idx_str)
    opt = int(opt_str)
    q = test_questions[idx]
    selected_option = q["options"][opt]

    if selected_option == q["correct"]:
        await callback.message.answer("✅ Правильно!")
        idx += 1
        if idx < len(test_questions):
            user_progress[callback.from_user.id] = idx
            await send_test_question(callback.message, idx)
        else:
            await callback.message.answer("🎉 Тест завершён!", reply_markup=main_menu())
            user_progress.pop(callback.from_user.id, None)
    else:
        await callback.message.answer("❌ Неправильно, попробуйте ещё раз.")

    await callback.answer()

# Обработка нажатий меню (ReplyKeyboard)
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "📝 Пройти тест":
        user_progress[message.from_user.id] = 0
        await send_test_question(message, 0)
    elif message.text in faq_data:
        await message.answer(faq_data[message.text], reply_markup=faq_menu())
    elif message.text == "📄 Просмотр договора оферты":
        await message.answer("Ссылка на документ")
    elif message.text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")
    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer("Выберите тест ниже:", reply_markup=start_test_menu())
    elif message.text == "📊 Общая картина":
        await message.answer("Общая картина")
    elif message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите вопрос:", reply_markup=faq_menu())
    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
