import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
import math

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

# --- Старый тест ---
test_questions = [
    {"q": "Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
     "options": ["Инструмент, способный анализировать огромные объемы данных.",
                 "Автоматический эксперт, который гарантированно предсказывает будущее."],
     "correct": "Инструмент, способный анализировать огромные объемы данных."},
    {"q": "Как ИИ может помочь в анализе рынка?",
     "options": ["Быстро обрабатывать новости, отчёты и данные, выявляя тренды.",
                 "Полностью заменить человека и принимать все решения."],
     "correct": "Быстро обрабатывать новости, отчёты и данные, выявляя тренды."},
    {"q": "Какую роль играет ИИ в автоматизации торговли?",
     "options": ["ИИ полностью устраняет необходимость в человеческом контроле, автоматически генерируя прибыль.",
                 "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."],
     "correct": "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."},
    {"q": "Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
     "options": ["Выявление мошеннических схем и предупреждение о потенциальных рисках.",
                 "Обеспечение полной гарантии прибыли, независимо от рыночной ситуации."],
     "correct": "Выявление мошеннических схем и предупреждение о потенциальных рисках."},
    {"q": "Что является ключевым фактором при использовании ИИ в инвестициях?",
     "options": [" Полностью довериться алгоритмам и не вмешиваться в процесс.",
                 "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."],
     "correct": "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."}
]

# --- Состояния пользователей ---
user_progress = {}       # для старого теста
user_state = {}          # для "Общей картины"
user_answers = {}        # для нового теста
user_scenario = {}       # выбранный путь: Машина / Дом / Пассивный доход

# --- Вопросы нового теста ---
scenario_questions = {
    "Машина": [
        {"q": "Какая стоимость машины?", "options": ["100 000₽", "500 000₽", "1 000 000₽"]},
        {"q": "Сколько вы готовы инвестировать в месяц?", "options": ["10 000₽", "20 000₽", "30 000₽"]}
    ],
    "Дом": [
        {"q": "Какая стоимость дома?", "options": ["3 000 000₽", "5 000 000₽", "15 000 000₽"]},
        {"q": "Сколько вы готовы инвестировать в месяц?", "options": ["10 000₽", "20 000₽", "30 000₽"]}
    ],
    "Пассивный доход": [
        {"q": "Сколько в месяц хотите получать?", "options": ["100 000₽", "500 000₽", "1 000 000₽"]},
        {"q": "Сколько вы готовы инвестировать в месяц?", "options": ["10 000₽", "20 000₽", "30 000₽"]}
    ]
}

# --- Главное меню ---
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- FAQ меню ---
def faq_menu():
    keyboard = [[KeyboardButton(text="⬅ Назад в меню")]]
    keyboard += [[KeyboardButton(text=q)] for q in faq_data.keys()]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню старого теста ---
def start_test_menu():
    keyboard = [
        [KeyboardButton(text="🚀 Начать тест")],
        [KeyboardButton(text="⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Отправка старого теста ---
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q["options"]] + [[KeyboardButton(text="⬅ Назад в меню")]],
        resize_keyboard=True
    )
    await message.answer(q["q"], reply_markup=keyboard)

# --- Отправка нового теста ---
async def send_scenario_question(message: types.Message, user_id: int, step: int):
    if step == 0:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Машина")],
                      [KeyboardButton(text="Дом")],
                      [KeyboardButton(text="Пассивный доход")],
                      [KeyboardButton(text="⬅ Назад в меню")]],
            resize_keyboard=True
        )
        await message.answer("Какова твоя цель?", reply_markup=keyboard)
    else:
        scenario = user_scenario.get(user_id)
        question = scenario_questions[scenario][step-1]
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=opt)] for opt in question["options"]] + [[KeyboardButton(text="⬅ Назад в меню")]],
            resize_keyboard=True
        )
        await message.answer(question["q"], reply_markup=keyboard)

# --- Inline кнопка ---
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- /start ---
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

# --- Обработка сообщений ---
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # --- Общая картина ---
    if message.text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text1 = ("Чтобы увидеть всю финансовую картину целиком и полностью, нужно смотреть не только глазами, "
                 "но и теми частями тела, которые выведут все необходимые цифры в таблицы, сделают сравнение "
                 "и конечно же сделают определенные выводы.\n\nИ так таблицы, которые подсвечивают реальное положение дел:")
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]], resize_keyboard=True)
        await message.answer(text1, reply_markup=keyboard)
    elif user_state.get(user_id) == "step1" and message.text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]], resize_keyboard=True)
        await message.answer_photo(photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE", reply_markup=keyboard)
    elif user_state.get(user_id) == "step2" and message.text == "Далее➡":
        del user_state[user_id]
        text2 = ("Стоит отметить что таблица сделана на примерных цифрах (сейчас именно такие), "
                 "потому как ежедневная торговля имеет разную доходность, но основная мысль думаю понятна:\n\n"
                 "— если ничего не делать будет один результат\n"
                 "— если делать, но частично будет другой результат\n"
                 "— и если использовать всё что имеем (искусственный интеллект + сложный процент), "
                 "получим то что нам надо (за короткий срок приличные результаты)\n\n"
                 "Вот почему так важно видеть всю картину целиком.")
        await message.answer(text2, reply_markup=main_menu())

    # --- Просмотр договора ---
    elif message.text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)

    # --- Готов инвестировать ---
    elif message.text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")

    # --- FAQ ---
    elif message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())
    elif message.text in faq_data:
        await message.answer(faq_data[message.text])

    # --- Старый тест ---
    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        instruction = ("📘 Инструкция:\n\nВыберите один правильный ответ на каждый вопрос.\nПомните, ИИ — это инструмент, а не волшебная палочка.")
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
                await message.answer("🎉 Тест завершён!", reply_markup=main_menu())
                del user_progress[user_id]
        elif message.text == "⬅ Назад в меню":
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            del user_progress[user_id]

    # --- Новый тест ---
    elif message.text == "📝 Пройти тест":
        user_scenario[user_id] = None
        user_answers[user_id] = []
        await send_scenario_question(message, user_id, step=0)
    elif user_id in user_answers:
        answers = user_answers[user_id]
        # шаг 0: выбор цели
        if len(answers) == 0:
            if message.text in ["Машина", "Дом", "Пассивный доход"]:
                user_scenario[user_id] = message.text
                answers.append(message.text)
                user_answers[user_id] = answers
                await send_scenario_question(message, user_id, step=1)
            elif message.text == "⬅ Назад в меню":
                del user_answers[user_id]
                await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        # шаги 1 и 2: вопросы по сценарию
        elif len(answers) == 3:  # все вопросы отвечены
            target = int(answers[1].replace("₽","").replace(" ",""))
            invest = int(answers[2].replace("₽","").replace(" ",""))
            annual_rate = 1.35  # 135% годовых
            monthly_rate = annual_rate / 12  # доходность в месяц

    # формула для сложного процента с ежемесячным взносом
    months_needed = math.ceil(math.log(1 + target * monthly_rate / invest) / math.log(1 + monthly_rate))

    # текст цели
    if scenario == "Машина":
        goal_text = "вы сможете приобрести вашу цель"
    elif scenario == "Дом":
        goal_text = "вы сможете приобрести выбранный дом"
    else:
        goal_text = "вы сможете достичь желаемого пассивного дохода"

    await message.answer(f"С помощью нашего ИИ-бота, при ваших инвестициях {invest} ₽ в месяц, {goal_text} через {months_needed} месяцев.")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="не готов")]],
        resize_keyboard=True
    )
    await message.answer("Что вы хотите сделать дальше?", reply_markup=keyboard)
                else:
                    await send_scenario_question(message, user_id, step=len(answers))
            elif message.text == "⬅ Назад в меню":
                del user_answers[user_id]
                await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        elif message.text == "готов инвестировать":
            await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-на-traiex")
            del user_answers[user_id]
        elif message.text == "не готов":
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            del user_answers[user_id]

    # --- Назад в меню ---
    elif message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        user_progress.pop(user_id, None)
        user_answers.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
