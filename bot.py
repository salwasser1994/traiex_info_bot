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

# --- FAQ ---
faq_data = {
    "Безопасно ли пользоваться платформой?": "Да, все операции проходят через защищённое соединение, ваши данные и средства надёжно защищены.",
    "Что будет, если я потеряю доступ к аккаунту?": "Вы сможете восстановить доступ через e-mail или поддержку — ваш аккаунт не пропадёт.",
    "Нужно ли платить, чтобы начать?": "Нет, регистрация бесплатная. Вы можете изучить все материалы и только потом принять решение о вложениях.",
    "Есть ли скрытые комиссии?": "Нет, все комиссии прозрачные и заранее указаны. Вы всегда знаете, сколько и за что платите.",
    "Можно ли вывести деньги в любой момент?": "Да, средства доступны для вывода по вашему желанию, без «заморозки» и обязательных сроков.",
    "А если я ничего не понимаю в инвестициях?": "Не страшно 🙂 Всё построено так, чтобы даже новичок мог разобраться. Есть инструкции, видеоуроки и поддержка.",
    "Что, если платформа перестанет работать?": "Мы используем резервные сервера и проверенные механизмы. Даже в случае сбоя деньги остаются у вас.",
    "Нужно ли тратить много времени?": "Нет, достаточно уделять несколько минут в день для проверки информации и управления своим счётом.",
    "Есть ли гарантии?": "Мы не обещаем «золотых гор», но гарантируем прозрачность, безопасность и честную работу платформы."
}

# --- ИИ-Тест ---
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
            " Полностью довериться алгоритмам и не вмешиваться в процесс.",
            "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
        ],
        "correct": "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
    }
]

# --- Пользовательские данные ---
user_progress = {}  # для ИИ-теста
user_state = {}     # для "Общей картины"
user_answers = {}   # для теста с тремя путями

# --- Главное меню ---
def main_menu():
    keyboard = [
        [KeyboardButton("📊 Общая картина"), KeyboardButton("📝 Пройти тест")],
        [KeyboardButton("💰 Готов инвестировать"), KeyboardButton("📄 Просмотр договора оферты")],
        [KeyboardButton("✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton("Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- FAQ меню ---
def faq_menu():
    keyboard = [[KeyboardButton("⬅ Назад в меню")]] + [[KeyboardButton(q)] for q in faq_data.keys()]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню перед ИИ-тестом ---
def start_test_menu():
    keyboard = [
        [KeyboardButton("🚀 Начать тест")],
        [KeyboardButton("⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Отправка вопроса ИИ-теста ---
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(opt)] for opt in q["options"]] + [[KeyboardButton("⬅ Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(q["q"], reply_markup=keyboard)

# --- Inline кнопка "В меню" ---
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton("В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- Команда /start ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

# --- Inline callback ---
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()

# --- Основной обработчик ---
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # --- Кнопка "📝 Пройти тест" (три пути) ---
    if text == "📝 Пройти тест":
        user_answers[user_id] = {}
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("Машина"), KeyboardButton("Дом"), KeyboardButton("Пассивный доход")],
                [KeyboardButton("⬅ Назад в меню")]
            ],
            resize_keyboard=True
        )
        await message.answer("Какова твоя цель?", reply_markup=keyboard)
        return

    # --- Если пользователь в трёхшаговом тесте ---
    if user_id in user_answers:
        answers = user_answers[user_id]

        # Шаг 1: выбор цели
        if "goal" not in answers:
            if text == "⬅ Назад в меню":
                del user_answers[user_id]
                await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
                return
            answers["goal"] = text
            if text == "Машина":
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton("100 000р"), KeyboardButton("500 000р"), KeyboardButton("1 000 000р")],
                              [KeyboardButton("⬅ Назад в меню")]], resize_keyboard=True
                )
                await message.answer("Какая стоимость машины?", reply_markup=keyboard)
            elif text == "Дом":
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton("3 000 000р"), KeyboardButton("5 000 000р"), KeyboardButton("15 000 000р")],
                              [KeyboardButton("⬅ Назад в меню")]], resize_keyboard=True
                )
                await message.answer("Какая стоимость дома?", reply_markup=keyboard)
            elif text == "Пассивный доход":
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton("100 000р"), KeyboardButton("500 000р"), KeyboardButton("1 000 000р")],
                              [KeyboardButton("⬅ Назад в меню")]], resize_keyboard=True
                )
                await message.answer("Сколько в месяц хотите получать?", reply_markup=keyboard)
            return

        # Шаг 2: стоимость цели / желаемый доход
        if "goal_value" not in answers:
            if text == "⬅ Назад в меню":
                del user_answers[user_id]
                await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
                return
            answers["goal_value"] = text
            keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton("10 000р"), KeyboardButton("20 000р"), KeyboardButton("30 000р")],
                          [KeyboardButton("⬅ Назад в меню")]], resize_keyboard=True
            )
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=keyboard)
            return

        # Шаг 3: расчет
        if "monthly_invest" not in answers:
            if text == "⬅ Назад в меню":
                del user_answers[user_id]
                await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
                return
            answers["monthly_invest"] = text

            goal_value = int(answers["goal_value"].replace("р", "").replace(" ", ""))
            monthly = int(answers["monthly_invest"].replace("р", "").replace(" ", ""))
            annual_return = 1.35
            total = 0
            months = 0
            while total < goal_value:
                total = (total + monthly) * (annual_return ** (1/12))
                months += 1
            years = months // 12
            remaining_months = months % 12

            if answers["goal"] == "Пассивный доход":
                result_text = f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly}₽/мес, вы сможете получать пассивный доход {goal_value}₽ в месяц примерно через {years} лет и {remaining_months} месяцев."
            elif answers["goal"] == "Машина":
                result_text = f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly}₽/мес, вы сможете купить машину стоимостью {goal_value}₽ примерно через {years} лет и {remaining_months} месяцев."
            else:  # Дом
                result_text = f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly}₽/мес, вы сможете купить дом стоимостью {goal_value}₽ примерно через {years} лет и {remaining_months} месяцев."

            await message.answer(result_text, reply_markup=main_menu())
            del user_answers[user_id]
            return

    # --- Кнопка "✨ Невозможное возможно благодаря рычагам" (ИИ-тест) ---
    if text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer("📘 Инструкция:\nВыберите один правильный ответ на каждый вопрос.\nПомните, ИИ — это инструмент, а не волшебная палочка.", reply_markup=start_test_menu())
        return

    if text == "🚀 Начать тест" and user_id not in user_answers:
        user_progress[user_id] = 0
        await send_test_question(message, 0)
        return

    # --- Обработка ИИ-теста ---
    if user_id in user_progress:
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
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            del user_progress[user_id]
        else:
            await message.answer("❌ Неправильно. Попробуйте ещё раз.", reply_markup=ReplyKeyboardMarkup([[KeyboardButton(opt) for opt in q["options"]], [KeyboardButton("⬅ Назад в меню")]], resize_keyboard=True))
        return

    # --- FAQ ---
    if text in faq_data:
        await message.answer(faq_data[text])
        return

    # --- Общая картина ---
    if text == "📊 Общая картина":
        user_state[user_id] = "step1"
        await message.answer("Чтобы увидеть всю финансовую картину, начнем с таблиц...", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Далее➡"), KeyboardButton("⬅ Назад в меню")]], resize_keyboard=True))
        return
    elif user_state.get(user_id) == "step1" and text == "Далее➡":
        user_state[user_id] = "step2"
        await message.answer_photo(photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
                                 reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Далее➡"), KeyboardButton("⬅ Назад в меню")]], resize_keyboard=True))
        return
    elif user_state.get(user_id) == "step2" and text == "Далее➡":
        del user_state[user_id]
        await message.answer("Вот почему так важно видеть всю картину целиком.", reply_markup=main_menu())
        return

    # --- Документы ---
    if text == "📄 Просмотр договора оферты":
        await message.answer_document("BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ")
        return
    if text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-на-traiex")
        return

    # --- FAQ меню ---
    if text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())
        return

    # --- Назад в меню ---
    if text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        user_answers.pop(user_id, None)
        user_progress.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        return

    # --- По умолчанию ---
    await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
