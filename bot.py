import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

user_state = {}
user_goal_data = {}

def main_menu():
    keyboard = [
        [KeyboardButton(text="📝 Пройти тест")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def result_options_menu():
    keyboard = [
        [KeyboardButton(text="💰 Готов инвестировать")],
        [KeyboardButton(text="Не готов")],
        [KeyboardButton(text="Пройти тест заново")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def calculate_investment_monthly(goal_amount, monthly_invest, annual_rate=135):
    days_in_month = 30
    daily_rate = (1 + annual_rate/100) ** (1/365) - 1
    total = 0
    months = 0
    history = []
    while total < goal_amount:
        total += monthly_invest
        for day in range(days_in_month):
            total += total * daily_rate
        months += 1
        history.append((months, total))
    return months, history, daily_rate

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if message.text == "📝 Пройти тест" or message.text == "Пройти тест заново":
        user_state[user_id] = "goal_choice"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Машина"), KeyboardButton(text="Дом"), KeyboardButton(text="Пассивный доход")],
                [KeyboardButton(text="⬅ Назад в меню")]
            ],
            resize_keyboard=True
        )
        await message.answer("Какова твоя цель?", reply_markup=keyboard)
        return

    if user_state.get(user_id) == "goal_choice":
        user_goal_data[user_id] = {"goal_type": message.text}
        if message.text == "Машина":
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="100 000 ₽"), KeyboardButton(text="500 000 ₽"), KeyboardButton(text="1 000 000 ₽")],
                    [KeyboardButton(text="⬅ Назад в меню")]
                ],
                resize_keyboard=True
            )
            user_state[user_id] = "goal_amount"
            await message.answer("Какая стоимость машины?", reply_markup=keyboard)
            return
        elif message.text == "Дом":
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="3 000 000 ₽"), KeyboardButton(text="5 000 000 ₽"), KeyboardButton(text="15 000 000 ₽")],
                    [KeyboardButton(text="⬅ Назад в меню")]
                ],
                resize_keyboard=True
            )
            user_state[user_id] = "goal_amount"
            await message.answer("Какая стоимость дома?", reply_markup=keyboard)
            return
        else:
            await message.answer("Пассивный доход пока не рассчитывается", reply_markup=main_menu())
            user_state.pop(user_id, None)
            return

    if user_state.get(user_id) == "goal_amount":
        user_goal_data[user_id]["goal_amount"] = int(message.text.replace(" ₽","").replace(" ",""))
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="10 000 ₽"), KeyboardButton(text="20 000 ₽"), KeyboardButton(text="30 000 ₽")],
                [KeyboardButton(text="⬅ Назад в меню")]
            ],
            resize_keyboard=True
        )
        user_state[user_id] = "monthly_invest"
        await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=keyboard)
        return

    if user_state.get(user_id) == "monthly_invest":
        user_goal_data[user_id]["monthly_invest"] = int(message.text.replace(" ₽","").replace(" ",""))
        goal_amount = user_goal_data[user_id]["goal_amount"]
        monthly_invest = user_goal_data[user_id]["monthly_invest"]

        months, history, daily_rate = calculate_investment_monthly(goal_amount, monthly_invest)
        
        message_text = (
            f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly_invest} ₽ в месяц, "
            f"вы сможете купить {user_goal_data[user_id]['goal_type']} стоимостью {goal_amount} ₽ через {months} месяцев.\n\n"
            "📈 Расчёт производится с учетом ежедневного сложного процента!\n"
            f"Ежедневная ставка: {daily_rate*100:.4f}%\n\n"
            "Помесячное накопление:\n"
        )

        for i, total in history[:12]:
            message_text += f"Месяц {i}: {int(total)} ₽\n"
        if months > 12:
            message_text += "...\n"
            for i, total in history[-3:]:
                message_text += f"Месяц {i}: {int(total)} ₽\n"

        message_text += "\n💡 Объяснение расчёта:\n" \
                        "- Каждый месяц вы добавляете фиксированную сумму.\n" \
                        "- Ежедневно на текущую сумму начисляется процент по сложной схеме.\n" \
                        "- Капитал растет быстрее, чем при обычных ежемесячных начислениях."

        await message.answer(message_text, reply_markup=result_options_menu())
        user_state.pop(user_id, None)
        user_goal_data.pop(user_id, None)
        return

    if message.text == "Не готов":
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        return

    if message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        user_goal_data.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        return

    await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
