import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# Создаем бота с правильным parse_mode
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# --- Данные FAQ ---
faq_data = {
    "Безопасно ли пользоваться платформой?": "🔹 Да, все операции через защищённое соединение, ваши данные и средства надежно защищены.",
    "Что будет, если я потеряю доступ к аккаунту?": "🔹 Вы сможете восстановить доступ через e-mail или поддержку — аккаунт не пропадёт.",
    "Нужно ли платить, чтобы начать?": "🔹 Регистрация бесплатная. Сначала изучаете материалы, потом принимаете решение.",
    "Есть ли скрытые комиссии?": "🔹 Все комиссии прозрачные и заранее указаны.",
    "Можно ли вывести деньги в любой момент?": "🔹 Средства доступны для вывода без заморозки.",
    "А если я ничего не понимаю в инвестициях?": "🔹 Не страшно 🙂 Есть инструкции, видеоуроки и поддержка.",
    "Что, если платформа перестанет работать?": "🔹 Используем резервные сервера. Деньги остаются у вас.",
    "Нужно ли тратить много времени?": "🔹 Достаточно несколько минут в день для контроля.",
    "Есть ли гарантии?": "🔹 Прозрачность, безопасность и честная работа платформы гарантированы."
}

# --- Тестовые вопросы ---
test_questions = [
    {
        "q": "🤖 Что такое Искусственный Интеллект (ИИ) в инвестициях?",
        "options": ["📈 Инструмент для анализа данных", "🔮 Автоматический эксперт, который предсказывает будущее"],
        "correct": "📈 Инструмент для анализа данных"
    },
    {
        "q": "📊 Как ИИ помогает анализу рынка?",
        "options": ["⚡ Быстро обрабатывать данные и выявлять тренды", "❌ Полностью заменяет человека"],
        "correct": "⚡ Быстро обрабатывать данные и выявлять тренды"
    },
    {
        "q": "🤝 Роль ИИ в автоматизации торговли?",
        "options": ["❌ Полностью убирает контроль человека", "✅ Автоматизирует стратегии с корректным исполнением"],
        "correct": "✅ Автоматизирует стратегии с корректным исполнением"
    },
    {
        "q": "🔎 Что ИИ эффективно делает в инвестициях?",
        "options": ["⚠️ Выявляет мошеннические схемы", "💰 Гарантирует прибыль всегда"],
        "correct": "⚠️ Выявляет мошеннические схемы"
    },
    {
        "q": "🎯 Ключевой фактор при использовании ИИ?",
        "options": ["🌀 Полностью довериться алгоритмам", "✅ Контроль и корректировка стратегии человеком"],
        "correct": "✅ Контроль и корректировка стратегии человеком"
    }
]

user_progress = {}
user_state = {}  # для шагов общей картины

# --- Главное меню ---
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Возможности ИИ"), KeyboardButton(text="❓ FAQ AI")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню FAQ ---
def faq_menu():
    keyboard = [[KeyboardButton(text=q)] for q in faq_data.keys()]
    keyboard.append([KeyboardButton(text="⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню теста ---
def start_test_menu():
    keyboard = [
        [KeyboardButton(text="🚀 Начать тест")],
        [KeyboardButton(text="⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Отправка вопроса ---
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q["options"]] + [[KeyboardButton(text="⬅ Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(f"Шаг {idx+1}/{len(test_questions)}\n{q['q']}", reply_markup=keyboard)

# --- Inline кнопка "В меню" ---
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton(text="🏠 В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- Команда /start ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = "🚀 Приветствую! Добро пожаловать в мир инвестиционного AI.\nВыбирай путь 👇"
    await message.answer(text, reply_markup=main_menu())

# --- Обработка inline кнопок ---
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("🏁 Главное меню:", reply_markup=main_menu())
        await callback.answer()

# --- Обработка меню ---
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # --- Общая картина ---
    if text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text1 = (
            "📊 Чтобы увидеть финансовую картину полностью, "
            "нужно смотреть глазами и разумом AI. Вот таблицы, которые подсвечивают реальное положение дел:"
        )
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]],
            resize_keyboard=True
        )
        await message.answer(text1, reply_markup=keyboard)

    elif user_state.get(user_id) == "step1" and text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("⬅ Назад в меню"), KeyboardButton("Далее➡")]],
            resize_keyboard=True
        )
        # Фото таблицы
        await message.answer_photo(photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
                                 reply_markup=keyboard)

    elif user_state.get(user_id) == "step2" and text == "Далее➡":
        del user_state[user_id]
        text2 = (
            "💡 Таблица примерная, но смысл ясен:\n"
            "— ничего не делать → результат минимальный\n"
            "— делать частично → результат средний\n"
            "— использовать AI + сложный процент → результат максимальный за короткий срок\n"
            "🌟 Видеть всю картину целиком крайне важно!"
        )
        await message.answer(text2, reply_markup=main_menu())

    # --- Просмотр оферты ---
    elif text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)

    # --- Готов инвестировать ---
    elif text == "💰 Готов инвестировать":
        await message.answer("🌐 Ссылка на регистрацию: https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")

    # --- FAQ ---
    elif text == "❓ FAQ AI":
        await message.answer("Выберите вопрос:", reply_markup=faq_menu())
    elif text in faq_data:
        # Подсказка AI для мотивации
        hint = "💡 AI совет: понимание рисков и возможностей повышает успех инвестиций."
        await message.answer(f"{faq_data[text]}\n\n{hint}")

    # --- Тест ---
    elif text == "✨ Возможности ИИ":
        await message.answer("📘 Выберите правильный ответ на каждый вопрос:", reply_markup=start_test_menu())
    elif text == "🚀 Начать тест":
        user_progress[user_id] = 0
        await send_test_question(message, 0)

    elif user_id in user_progress:
        idx = user_progress[user_id]
        q = test_questions[idx]
        if text == q["correct"]:
            await message.answer("✅ Правильно!")
            idx += 1
            if idx < len(test_questions):
                user_progress[user_id] = idx
                await send_test_question(message, idx)
            else:
                await message.answer("🎉 Тест завершён!", reply_markup=main_menu())
                del user_progress[user_id]
        elif text == "⬅ Назад в меню":
            await message.answer("🏁 Главное меню:", reply_markup=main_menu())
            del user_progress[user_id]
        else:
            await message.answer("❌ Неправильный ответ, попробуй снова.")

    elif text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        await message.answer("🏁 Главное меню:", reply_markup=main_menu())

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
