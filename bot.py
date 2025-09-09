import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
user_state = {}

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton(text="📝 Пройти тест")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Меню пост-калькуляции
def post_calc_menu():
    keyboard = [
        [KeyboardButton(text="💰 Готов инвестировать")],
        [KeyboardButton(text="Не готов")],
        [KeyboardButton(text="Пройти тест заново")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Вопросы по тесту
goal_options = ["Машина", "Дом", "Пассивный доход"]

# Варианты стоимости
cost_options = {
    "Машина": ["100 000 ₽", "500 000 ₽", "1 000 000 ₽"],
    "Дом": ["3 000 000 ₽", "5 000 000 ₽", "15 000 000 ₽"]
}

# Варианты ежемесячного взноса
monthly_options = ["10 000 ₽", "20 000 ₽", "30 000 ₽"]

# Варианты дохода для пассивного дохода
passive_income_options = ["100 000 ₽", "500 000 ₽", "1 000 000 ₽"]

# Кнопки с вариантом ответа + "⬅ Назад в меню"
def option_keyboard(options):
    kb = [[KeyboardButton(text=opt)] for opt in options]
    kb.append([KeyboardButton(text="⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Старт
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=main_menu())

# Обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Возврат в главное меню
    if text == "⬅ Назад в меню" or text == "Не готов":
        user_state.pop(user_id, None)
        user_data.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        return

    # Главная кнопка "📝 Пройти тест"
    if text == "📝 Пройти тест":
        user_state[user_id] = "choose_goal"
        await message.answer("Какова твоя цель?", reply_markup=option_keyboard(goal_options))
        return

    # Выбор цели
    if user_state.get(user_id) == "choose_goal":
        if text in goal_options:
            user_data[user_id] = {"goal": text}
            if text == "Пассивный доход":
                user_state[user_id] = "choose_passive_income"
                await message.answer("Сколько в месяц хотите получать пассивного дохода?", reply_markup=option_keyboard(passive_income_options))
            else:
                user_state[user_id] = "choose_cost"
                await message.answer(f"Какая стоимость {text.lower()}?", reply_markup=option_keyboard(cost_options[text]))
        else:
            await message.answer("Пожалуйста, выберите одну из предложенных целей.")
        return

    # Выбор стоимости (Машина / Дом)
    if user_state.get(user_id) == "choose_cost":
        goal = user_data[user_id]["goal"]
        if text in cost_options[goal]:
            cost = int(text.replace(" ₽", "").replace(" ", ""))
            user_data[user_id]["cost"] = cost
            user_state[user_id] = "choose_monthly"
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=option_keyboard(monthly_options))
        else:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    # Выбор ежемесячного взноса и расчет (Машина / Дом)
    if user_state.get(user_id) == "choose_monthly":
        try:
            monthly = int(text.replace(" ₽", "").replace(" ", ""))
            user_data[user_id]["monthly"] = monthly

            cost = user_data[user_id]["cost"]
            month = 0
            monthly_rate = 0.1125  # 11,25% в месяц
            total = 0
            monthly_totals = []

            while total < cost:
                month += 1
                total = (total + monthly) * (1 + monthly_rate)
                monthly_totals.append(total)

            msg = f"📈 Накопления по месяцам с учетом ежемесячного сложного процента 11,25%:\n\n"
            for i, val in enumerate(monthly_totals, start=1):
                if i <= 3 or i > len(monthly_totals) - 3:
                    msg += f"Месяц {i}: {int(val):,} ₽\n"
                elif i == 4:
                    msg += "...\n"

            msg += f"\nС вашей ежемесячной инвестицией {monthly:,} ₽ вы сможете накопить на {user_data[user_id]['goal'].lower()} стоимостью {cost:,} ₽ примерно через {month} месяцев.\n\n"
            msg += ("Важно: расчет учитывает сложный процент. Каждый месяц ваш капитал увеличивается на 11,25%, что ускоряет накопление по сравнению с обычным фиксированным вкладом. "
                    "Вы можете видеть помесячные начисления в примерах выше.")

            await message.answer(msg, reply_markup=post_calc_menu())
            user_state.pop(user_id)
        except ValueError:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    # Путь Пассивного дохода: выбор суммы дохода
    if user_state.get(user_id) == "choose_passive_income":
        if text in passive_income_options:
            target_income = int(text.replace(" ₽", "").replace(" ", ""))
            user_data[user_id]["target_income"] = target_income
            user_state[user_id] = "choose_monthly_passive"
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=option_keyboard(monthly_options))
        else:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    # Путь Пассивного дохода: выбор ежемесячного взноса и расчет
    if user_state.get(user_id) == "choose_monthly_passive":
        try:
            monthly = int(text.replace(" ₽", "").replace(" ", ""))
            target_income = user_data[user_id]["target_income"]
            monthly_rate = 0.1125
            month = 0
            capital = 0
            monthly_totals = []

            while True:
                month += 1
                capital = (capital + monthly) * (1 + monthly_rate)
                passive = capital * monthly_rate
                monthly_totals.append((capital, passive))
                if passive >= target_income:
                    break

            msg = f"📈 Капитал и пассивный доход по месяцам:\n\n"
            for i, (cap, pas) in enumerate(monthly_totals, start=1):
                if i <= 3 or i > len(monthly_totals) - 3:
                    msg += f"Месяц {i}: капитал {int(cap):,} ₽, пассивный доход {int(pas):,} ₽\n"
                elif i == 4:
                    msg += "...\n"

            msg += f"\nПри вашей ежемесячной инвестиции {monthly:,} ₽ вы сможете получать пассивный доход {target_income:,} ₽/мес примерно через {month} месяцев.\n"
            msg += ("Важно: расчет учитывает ежедневный сложный процент, начисляемый ежемесячно для упрощения демонстрации. "
                    "Вы видите капитал и доход на конец каждого месяца.")

            await message.answer(msg, reply_markup=post_calc_menu())
            user_state.pop(user_id)
        except ValueError:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    # Кнопка "Пройти тест заново"
    if text == "Пройти тест заново":
        user_state[user_id] = "choose_goal"
        await message.answer("Какова твоя цель?", reply_markup=option_keyboard(goal_options))
        return

    await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
