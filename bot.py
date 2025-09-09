import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "ВАШ_ТОКЕН_БОТА"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

user_state = {}
user_data = {}

# Главное меню
def main_menu():
    keyboard = [[KeyboardButton(text="📝 Пройти тест")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Меню после расчета
def post_calculation_menu():
    keyboard = [
        [KeyboardButton(text="💰 Готов инвестировать")],
        [KeyboardButton(text="Не готов")],
        [KeyboardButton(text="Пройти тест заново")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Кнопки для выбора цели
def choose_goal_menu():
    keyboard = [
        [KeyboardButton(text="Машина"), KeyboardButton(text="Дом"), KeyboardButton(text="Пассивный доход")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Кнопки для выбора стоимости
def choose_cost_menu(goal):
    if goal == "Машина":
        options = ["100000", "500000", "1000000"]
    elif goal == "Дом":
        options = ["3000000", "5000000", "15000000"]
    else:
        options = ["100000", "500000", "1000000"]
    keyboard = [[KeyboardButton(text=opt)] for opt in options]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Кнопки для выбора вклада
def choose_monthly_invest_menu():
    keyboard = [
        [KeyboardButton(text="10000"), KeyboardButton(text="20000"), KeyboardButton(text="30000")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Функция расчета помесячного накопления с ежедневным сложным процентом
def calculate_investment_monthly(goal_amount, monthly_invest, annual_rate=135):
    daily_rate = (1 + annual_rate / 100) ** (1 / 365) - 1
    total = 0
    months = 0
    history = []

    while total < goal_amount:
        total += monthly_invest  # вклад в начале месяца
        for day in range(30):  # начисление ежедневно
            total += total * daily_rate
        months += 1
        history.append((months, total))
    return months, history, daily_rate

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_state[message.from_user.id] = "choose_goal"
    await message.answer("Какова твоя цель?", reply_markup=choose_goal_menu())

# Обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Выбор цели
    if user_state.get(user_id) == "choose_goal":
        if text in ["Машина", "Дом", "Пассивный доход"]:
            user_data[user_id] = {"goal": text}
            user_state[user_id] = "choose_cost"
            await message.answer(f"Вы выбрали: {text}. Какая стоимость?", reply_markup=choose_cost_menu(text))
        return

    # Выбор стоимости
    if user_state.get(user_id) == "choose_cost":
        if text.isdigit():
            user_data[user_id]["cost"] = int(text)
            user_state[user_id] = "choose_monthly_invest"
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=choose_monthly_invest_menu())
        return

    # Выбор вклада
    if user_state.get(user_id) == "choose_monthly_invest":
        if text.isdigit():
            user_data[user_id]["monthly_invest"] = int(text)
            # Расчет
            cost = user_data[user_id]["cost"]
            monthly_invest = user_data[user_id]["monthly_invest"]
            months, history, daily_rate = calculate_investment_monthly(cost, monthly_invest)
            
            msg = f"💡 Расчет для цели: {user_data[user_id]['goal']}\n"
            msg += f"Стоимость: {cost:,} ₽\nВклад в месяц: {monthly_invest:,} ₽\nГодовая доходность: 135%\n\n"
            msg += "📈 Накопления по месяцам с учетом ежедневного сложного процента:\n"
            for m, total in history:
                msg += f"Месяц {m}: {int(total):,} ₽\n"
            msg += f"\n🎯 Вы достигнете цели примерно через {months} месяцев (~{months//12} лет и {months%12} месяцев).\n"
            msg += "Каждый месяц капитал увеличивается не только за счет ваших вкладов, но и за счет ежедневного начисления процентов, что очень важно для ускорения накоплений."
            
            await message.answer(msg, reply_markup=post_calculation_menu())
            user_state[user_id] = "post_calculation"
        return

    # Пострасчетное меню
    if user_state.get(user_id) == "post_calculation":
        if text == "💰 Готов инвестировать":
            await message.answer("Ссылка на регистрацию/инвестиции")
        elif text == "Не готов":
            user_state[user_id] = "choose_goal"
            await message.answer("Возвращаемся в главное меню.", reply_markup=choose_goal_menu())
        elif text == "Пройти тест заново":
            user_state[user_id] = "choose_goal"
            await message.answer("Начнем заново. Какова твоя цель?", reply_markup=choose_goal_menu())
        return

    # Любое другое сообщение
    await message.answer("Выберите действие из меню.", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
