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

def main_menu():
    keyboard = [
        [KeyboardButton(text="📝 Пройти тест")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def post_calc_menu():
    keyboard = [
        [KeyboardButton(text="💰 Готов инвестировать")],
        [KeyboardButton(text="Не готов")],
        [KeyboardButton(text="Пройти тест заново")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def add_back_button(options):
    # Добавляем кнопку "⬅ Назад в меню" под вариантами
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in options] + [[KeyboardButton(text="⬅ Назад в меню")]],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Давай посчитаем, когда ты сможешь накопить на свою цель.", reply_markup=main_menu())

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if text == "📝 Пройти тест" or text == "Пройти тест заново":
        user_state[user_id] = "choose_goal"
        options = ["Машина", "Дом", "Пассивный доход"]
        await message.answer("Какова твоя цель?", reply_markup=add_back_button(options))
        return

    if user_state.get(user_id) == "choose_goal":
        user_data[user_id] = {"goal": text}
        if text == "Машина":
            user_state[user_id] = "car_cost"
            options = ["100 000 ₽", "500 000 ₽", "1 000 000 ₽"]
            await message.answer("Какая стоимость машины?", reply_markup=add_back_button(options))
        elif text == "Дом":
            user_state[user_id] = "house_cost"
            options = ["3 000 000 ₽", "5 000 000 ₽", "15 000 000 ₽"]
            await message.answer("Какая стоимость дома?", reply_markup=add_back_button(options))
        else:
            await message.answer("Пока считаем только Машину или Дом.", reply_markup=main_menu())
        return

    if user_state.get(user_id) in ["car_cost", "house_cost"]:
        try:
            amount = int(text.replace(" ₽", "").replace(" ", ""))
            user_data[user_id]["cost"] = amount
            user_state[user_id] = "monthly_invest"
            options = ["10 000 ₽", "20 000 ₽", "30 000 ₽"]
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=add_back_button(options))
        except ValueError:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    if user_state.get(user_id) == "monthly_invest":
        try:
            monthly = int(text.replace(" ₽", "").replace(" ", ""))
            user_data[user_id]["monthly"] = monthly

            cost = user_data[user_id]["cost"]
            month = 0
            monthly_rate = 0.1125
            total = 0
            monthly_totals = []

            while total < cost:
                month += 1
                total = total * (1 + monthly_rate) + monthly
                monthly_totals.append(total)

            msg = f"📈 Накопления по месяцам с учетом сложного процента 11,25% в месяц:\n\n"
            for i, val in enumerate(monthly_totals, start=1):
                if i <= 3 or i > len(monthly_totals) - 3:
                    msg += f"Месяц {i}: {int(val):,} ₽\n"
                elif i == 4:
                    msg += "...\n"

            msg += f"\nС вашей ежемесячной инвестицией {monthly:,} ₽ вы сможете накопить на {user_data[user_id]['goal']} стоимостью {cost:,} ₽ примерно через {month} месяцев.\n\n"
            msg += ("Важно: расчет учитывает сложный процент. "
                    "Каждый месяц ваш капитал увеличивается на 11,25%, что ускоряет накопление по сравнению с обычным фиксированным вкладом.")

            await message.answer(msg, reply_markup=post_calc_menu())
            user_state.pop(user_id)
        except ValueError:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    if text == "Не готов":
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu())

    if text == "💰 Готов инвестировать":
        await message.answer("Переход к регистрации/инвестициям...", reply_markup=main_menu())

    if text == "⬅ Назад в меню":
        user_state.pop(user_id, None)
        user_data.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
