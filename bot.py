import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Токен бота
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

user_state = {}      # состояние пользователя
user_goal_data = {}  # данные для расчета

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton(text="📝 Пройти тест")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Расчет инвестиций с ежедневным сложным процентом и помесячным выводом
def calculate_investment_monthly(goal_amount, monthly_invest, annual_rate=135):
    days_in_month = 30
    daily_rate = (1 + annual_rate/100) ** (1/365) - 1  # ежедневный сложный процент
    total = 0
    months = 0
    history = []
    
    while total < goal_amount:
        # Добавляем взнос за месяц
        total += monthly_invest
        # Начисляем ежедневный сложный процент
        for day in range(days_in_month):
            total += total * daily_rate
        months += 1
        history.append((months, total))
    return months, history, daily_rate

# Обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # Стартовый выбор
    if message.text == "📝 Пройти тест":
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

    # Выбор цели
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

    # Выбор ежемесячной инвестиции
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

    # Финальный расчёт
    if user_state.get(user_id) == "monthly_invest":
        user_goal_data[user_id]["monthly_invest"] = int(message.text.replace(" ₽","").replace(" ",""))
        goal_amount = user_goal_data[user_id]["goal_amount"]
        monthly_invest = user_goal_data[user_id]["monthly_invest"]

        months, history, daily_rate = calculate_investment_monthly(goal_amount, monthly_invest)
        
        message_text = (
            f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly_invest} ₽ в месяц, "
            f"вы сможете купить {user_goal_data[user_id]['goal_type']} стоимостью {goal_amount} ₽ через {months} месяцев.\n\n"
            "📈 Расчёт производится с учетом ежедневного сложного процента!\n"
            f"Ежедневная ставка: {daily_rate*100:.4f}% (что очень важно для роста капитала)\n\n"
            "Помесячное накопление:\n"
        )

        for i, total in history[:12]:  # первые 12 месяцев
            message_text += f"Месяц {i}: {int(total)} ₽\n"
        if months > 12:
            message_text += "...\n"
            for i, total in history[-3:]:  # последние 3 месяца
                message_text += f"Месяц {i}: {int(total)} ₽\n"

        message_text += "\n💡 Объяснение расчёта:\n" \
                        "- Каждый месяц вы добавляете фиксированную сумму инвестиций.\n" \
                        "- Ежедневно на текущую сумму начисляется процент по сложной схеме.\n" \
                        "- Это позволяет капиталу расти быстрее, чем просто ежемесячное начисление.\n" \
                        "- В результате вы достигаете цели быстрее, чем при обычных инвестициях."

        await message.answer(message_text, reply_markup=main_menu())
        user_state.pop(user_id, None)
        user_goal_data.pop(user_id, None)
        return

    # Назад в меню
    if message.text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        user_goal_data.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        return

    # Любое другое сообщение
    await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
