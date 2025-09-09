import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

user_state = {}
user_data = {}

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать")],
        [KeyboardButton(text="📄 Просмотр договора оферты")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Клавиатура после расчета
def post_calc_menu():
    keyboard = [
        [KeyboardButton(text="💰 Готов инвестировать")],
        [KeyboardButton(text="Не готов")],
        [KeyboardButton(text="Пройти тест заново")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Давай посчитаем, когда ты сможешь накопить на свою цель.", reply_markup=main_menu())

# Начало теста
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if text == "📝 Пройти тест" or text == "Пройти тест заново":
        user_state[user_id] = "choose_goal"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Машина"), KeyboardButton(text="Дом"), KeyboardButton(text="Пассивный доход")]
            ],
            resize_keyboard=True
        )
        await message.answer("Какова твоя цель?", reply_markup=keyboard)
        return

    if user_state.get(user_id) == "choose_goal":
        user_data[user_id] = {"goal": text}
        if text == "Машина":
            user_state[user_id] = "car_cost"
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="100 000 ₽"), KeyboardButton(text="500 000 ₽"), KeyboardButton(text="1 000 000 ₽")]
                ],
                resize_keyboard=True
            )
            await message.answer("Какая стоимость машины?", reply_markup=keyboard)
        elif text == "Дом":
            user_state[user_id] = "house_cost"
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="3 000 000 ₽"), KeyboardButton(text="5 000 000 ₽"), KeyboardButton(text="15 000 000 ₽")]
                ],
                resize_keyboard=True
            )
            await message.answer("Какая стоимость дома?", reply_markup=keyboard)
        else:
            await message.answer("Пока считаем только Машину или Дом.")
        return

    if user_state.get(user_id) in ["car_cost", "house_cost"]:
        try:
            amount = int(text.replace(" ₽", "").replace(" ", ""))
            user_data[user_id]["cost"] = amount
            user_state[user_id] = "monthly_invest"
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="10 000 ₽"), KeyboardButton(text="20 000 ₽"), KeyboardButton(text="30 000 ₽")]
                ],
                resize_keyboard=True
            )
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=keyboard)
        except ValueError:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    if user_state.get(user_id) == "monthly_invest":
        try:
            monthly = int(text.replace(" ₽", "").replace(" ", ""))
            user_data[user_id]["monthly"] = monthly
            # Расчет накоплений
            cost = user_data[user_id]["cost"]
            total = 0
            month = 0
            monthly_rate = 0.1125  # 11,25% в месяц
            monthly_list = []
            while total < cost:
                total = (total + monthly) * (1 + monthly_rate)
                month += 1
                monthly_list.append(total)
            # Формируем вывод
            msg = f"📈 Накопления по месяцам с учетом месячного сложного процента 11,25% (135% годовых):\n"
            for i, val in enumerate(monthly_list, start=1):
                msg += f"Месяц {i}: {int(val):,} ₽\n"
            msg += f"\nС вашей ежемесячной инвестицией {monthly:,} ₽ вы сможете накопить на {user_data[user_id]['goal']} стоимостью {cost:,} ₽ примерно через {month} месяцев.\n\n"
            msg += "Обратите внимание: расчет учитывает сложный процент, который начисляется каждый месяц. Это означает, что доход за каждый месяц добавляется к сумме вклада и также начинает приносить доход в следующем месяце. Это очень важно для ускорения роста капитала!"
            await message.answer(msg, reply_markup=post_calc_menu())
            user_state.pop(user_id)
        except ValueError:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    if text == "Не готов":
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu())

    if text == "💰 Готов инвестировать":
        await message.answer("Переход к регистрации/инвестициям...", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
