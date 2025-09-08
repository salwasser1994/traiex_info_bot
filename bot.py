import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Inline кнопка "В меню"
def inline_back_to_menu():
    keyboard = [
        [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Словарь для хранения ответов пользователей
user_answers = {}

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

# Обработка inline кнопки "В меню"
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()

# Обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # --- Кнопка "📝 Пройти тест" ---
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

    # --- Если пользователь уже в тесте ---
    if user_id in user_answers:
        answers = user_answers[user_id]

        # --- Шаг 1: выбор цели ---
        if "goal" not in answers:
            if text == "⬅ Назад в меню":
                del user_answers[user_id]
                await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
                return
            answers["goal"] = text

            if text == "Машина":
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton("100 000р"), KeyboardButton("500 000р"), KeyboardButton("1 000 000р")],
                        [KeyboardButton("⬅ Назад в меню")]
                    ],
                    resize_keyboard=True
                )
                await message.answer("Какая стоимость машины?", reply_markup=keyboard)
            elif text == "Дом":
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton("3 000 000р"), KeyboardButton("5 000 000р"), KeyboardButton("15 000 000р")],
                        [KeyboardButton("⬅ Назад в меню")]
                    ],
                    resize_keyboard=True
                )
                await message.answer("Какая стоимость дома?", reply_markup=keyboard)
            elif text == "Пассивный доход":
                keyboard = ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton("100 000р"), KeyboardButton("500 000р"), KeyboardButton("1 000 000р")],
                        [KeyboardButton("⬅ Назад в меню")]
                    ],
                    resize_keyboard=True
                )
                await message.answer("Сколько в месяц хотите получать?", reply_markup=keyboard)
            return

        # --- Шаг 2: стоимость машины/дома или желаемый доход ---
        if "goal_value" not in answers:
            if text == "⬅ Назад в меню":
                del user_answers[user_id]
                await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
                return
            answers["goal_value"] = text

            # Вопрос про ежемесячные инвестиции
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton("10 000р"), KeyboardButton("20 000р"), KeyboardButton("30 000р")],
                    [KeyboardButton("⬅ Назад в меню")]
                ],
                resize_keyboard=True
            )
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=keyboard)
            return

        # --- Шаг 3: месячные инвестиции и расчет ---
        if "monthly_invest" not in answers:
            if text == "⬅ Назад в меню":
                del user_answers[user_id]
                await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
                return
            answers["monthly_invest"] = text

            # Преобразование значений
            goal_value = int(answers["goal_value"].replace("р", "").replace(" ", ""))
            monthly = int(answers["monthly_invest"].replace("р", "").replace(" ", ""))
            annual_return = 1.35  # 135% годовых

            # Расчет месяцев до достижения цели с учетом сложного процента
            total = 0
            months = 0
            while total < goal_value:
                total = (total + monthly) * (annual_return ** (1/12))
                months += 1

            years = months // 12
            remaining_months = months % 12

            # Формируем сообщение в зависимости от цели
            if answers["goal"] == "Пассивный доход":
                result_text = (
                    f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly}₽/мес, "
                    f"вы сможете получать пассивный доход {goal_value}₽ в месяц примерно через {years} лет и {remaining_months} месяцев."
                )
            elif answers["goal"] == "Машина":
                result_text = (
                    f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly}₽/мес, "
                    f"вы сможете купить машину стоимостью {goal_value}₽ примерно через {years} лет и {remaining_months} месяцев."
                )
            elif answers["goal"] == "Дом":
                result_text = (
                    f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly}₽/мес, "
                    f"вы сможете купить дом стоимостью {goal_value}₽ примерно через {years} лет и {remaining_months} месяцев."
                )

            await message.answer(result_text, reply_markup=main_menu())
            del user_answers[user_id]
            return

    # --- Другие кнопки главного меню ---
    if text == "📊 Общая картина":
        await message.answer("Раздел 'Общая картина' пока не реализован.", reply_markup=main_menu())
    elif text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex", reply_markup=main_menu())
    elif text == "📄 Просмотр договора оферты":
        await message.answer("Документ оферты пока не реализован.", reply_markup=main_menu())
    elif text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer("Инструкция пока не реализована.", reply_markup=main_menu())
    elif text == "Часто задаваемые вопросы❓":
        await message.answer("FAQ пока не реализован.", reply_markup=main_menu())
    elif text == "⬅ Назад в меню":
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
