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

# --- Состояния пользователей ---
user_progress = {}
user_state = {}  # для "Общей картины"
user_test_path = {}  # путь теста: "машина", "дом", "пассивный доход"
user_test_answers = {}  # хранение ответов на вопросы теста

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
    keyboard = [[KeyboardButton(text="⬅ Назад в меню")]]
    keyboard += [[KeyboardButton(text=q)] for q in faq_data.keys()]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню теста ---
def test_start_menu():
    keyboard = [
        [KeyboardButton(text="Машина"), KeyboardButton(text="Дом"), KeyboardButton(text="Пассивный доход")],
        [KeyboardButton(text="⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def test_question_menu(options):
    keyboard = [[KeyboardButton(text=opt)] for opt in options]
    keyboard.append([KeyboardButton(text="⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Функции теста ---
async def start_test(message: types.Message):
    await message.answer("Выберите вашу цель:", reply_markup=test_start_menu())

async def handle_test_answer(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Назад в меню
    if text == "⬅ Назад в меню":
        user_test_path.pop(user_id, None)
        user_test_answers.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        return

    # Первый выбор пути
    if user_id not in user_test_path:
        if text.lower() == "машина":
            user_test_path[user_id] = "машина"
            user_test_answers[user_id] = {}
            options = ["100 000₽", "500 000₽", "1 000 000₽"]
            await message.answer("Какая стоимость машины?", reply_markup=test_question_menu(options))
        elif text.lower() == "дом":
            user_test_path[user_id] = "дом"
            user_test_answers[user_id] = {}
            options = ["3 000 000₽", "5 000 000₽", "15 000 000₽"]
            await message.answer("Какая стоимость дома?", reply_markup=test_question_menu(options))
        elif text.lower() == "пассивный доход":
            user_test_path[user_id] = "пассивный доход"
            user_test_answers[user_id] = {}
            options = ["100 000₽", "500 000₽", "1 000 000₽"]
            await message.answer("Сколько в месяц хотите получать?", reply_markup=test_question_menu(options))
        return

    # Обработка второго вопроса
    path = user_test_path[user_id]
    answers = user_test_answers[user_id]

    if path == "машина":
        if "стоимость" not in answers:
            answers["стоимость"] = text
            options = ["10 000₽", "20 000₽", "30 000₽"]
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=test_question_menu(options))
        else:
            answers["инвест"] = text
            await calculate_result(message, path, answers)
            user_test_path.pop(user_id)
            user_test_answers.pop(user_id)

    elif path == "дом":
        if "стоимость" not in answers:
            answers["стоимость"] = text
            options = ["10 000₽", "20 000₽", "30 000₽"]
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=test_question_menu(options))
        else:
            answers["инвест"] = text
            await calculate_result(message, path, answers)
            user_test_path.pop(user_id)
            user_test_answers.pop(user_id)

    elif path == "пассивный доход":
        if "доход" not in answers:
            answers["доход"] = text
            options = ["10 000₽", "20 000₽", "30 000₽"]
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=test_question_menu(options))
        else:
            answers["инвест"] = text
            await calculate_result(message, path, answers)
            user_test_path.pop(user_id)
            user_test_answers.pop(user_id)

# --- Расчет результата ---
async def calculate_result(message: types.Message, path, answers):
    # конвертация текста в числа
    def parse_rub(text):
        return int(text.replace("₽", "").replace(" ", "").replace(",", ""))

    invest = parse_rub(answers["инвест"])
    rate = 1.35  # 135% годовых

    if path == "машина":
        price = parse_rub(answers["стоимость"])
        months = 0
        total = 0
        while total < price:
            total += invest
            total *= rate ** (1/12)
            months += 1
        await message.answer(f"С помощью нашего ИИ-бота, при ваших инвестициях {invest}₽ в месяц, "
                             f"вы сможете купить машину стоимостью {price}₽ через {months} месяцев.", reply_markup=main_menu())

    elif path == "дом":
        price = parse_rub(answers["стоимость"])
        months = 0
        total = 0
        while total < price:
            total += invest
            total *= rate ** (1/12)
            months += 1
        await message.answer(f"С помощью нашего ИИ-бота, при ваших инвестициях {invest}₽ в месяц, "
                             f"вы сможете купить дом стоимостью {price}₽ через {months} месяцев.", reply_markup=main_menu())

    elif path == "пассивный доход":
        target = parse_rub(answers["доход"])
        # расчет необходимого капитала, чтобы получать target * 12 / годовой доход
        capital = target * 12 / rate
        months = 0
        total = 0
        while total < capital:
            total += invest
            total *= rate ** (1/12)
            months += 1
        await message.answer(f"С помощью нашего ИИ-бота, при ваших инвестициях {invest}₽ в месяц, "
                             f"вы сможете получать {target}₽ в месяц пассивного дохода через {months} месяцев.", reply_markup=main_menu())

# --- Inline-кнопка "В меню" ---
def inline_back_to_menu():
    keyboard = [
        [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]
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

# --- Обработка сообщений ---
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # --- Общая картина ---
    if message.text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text1 = (
            "Чтобы увидеть всю финансовую картину целиком и полностью, нужно смотреть не только глазами, "
            "но и теми частями тела, которые выведут все необходимые цифры в таблицы, сделают сравнение "
            "и конечно же сделают определенные выводы.\n\n"
            "И так таблицы, которые подсвечивают реальное положение дел:"
        )
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        await message.answer(text1, reply_markup=keyboard)
        return

    elif user_state.get(user_id) == "step1" and message.text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        await message.answer_photo(
            photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
            reply_markup=keyboard
        )
        return

    elif user_state.get(user_id) == "step2" and message.text == "Далее➡":
        del user_state[user_id]
        text2 = (
            "Стоит отметить что таблица сделана на примерных цифрах (сейчас именно такие), "
            "потому как ежедневная торговля имеет разную доходность, но основная мысль думаю понятна:\n\n"
            "— если ничего не делать будет один результат\n"
            "— если делать, но частично будет другой результат\n"
            "— и если использовать всё что имеем (искусственный интеллект + сложный процент), "
            "получим то что нам надо (за короткий срок приличные результаты)\n\n"
            "Вот почему так важно видеть всю картину целиком."
        )
        await message.answer(text2, reply_markup=main_menu())
        return

    # --- Просмотр договора ---
    elif message.text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)
        return

    # --- Готов инвестировать ---
    elif message.text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")
        return

    # --- FAQ ---
    elif message.text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())
        return

    elif message.text in faq_data:
        await message.answer(faq_data[message.text])
        return

    # --- Тест ---
    elif message.text == "📝 Пройти тест" or user_id in user_test_path:
        if message.text == "📝 Пройти тест":
            await start_test(message)
        else:
            await handle_test_answer(message)
        return

    # --- Невозможное возможно ---
    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        instruction = (
            "📘 Инструкция:\n\n"
            "Выберите один правильный ответ на каждый вопрос.\n"
            "Помните, ИИ — это инструмент, а не волшебная палочка."
        )
        await message.answer(instruction, reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🚀 Начать тест")],[KeyboardButton(text="⬅ Назад в меню")]],
            resize_keyboard=True
        ))
        return

    # --- Назад в меню ---
    elif message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        user_progress.pop(user_id, None)
        user_test_path.pop(user_id, None)
        user_test_answers.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        return

    # --- По умолчанию ---
    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())


# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
