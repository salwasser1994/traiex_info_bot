import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = "ТОКЕН_ТВОЕГО_БОТА"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранение данных пользователей
user_data = {}

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пройти тест")]],
    resize_keyboard=True
)

# ========== ОБРАБОТЧИКИ ==========

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Привет! Нажми 'Пройти тест', чтобы начать 🚀", reply_markup=main_menu)


@dp.message(F.text == "Пройти тест")
async def start_test(message: types.Message):
    user_data[message.from_user.id] = {}
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Машина"), KeyboardButton(text="Дом")],
            [KeyboardButton(text="Пассивный доход")]
        ],
        resize_keyboard=True
    )
    await message.answer("Какова твоя цель?", reply_markup=kb)


@dp.message(F.text.in_(["Машина", "Дом", "Пассивный доход"]))
async def choose_path(message: types.Message):
    uid = message.from_user.id
    user_data[uid]["path"] = message.text

    if message.text == "Машина":
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="100000"), KeyboardButton(text="500000"), KeyboardButton(text="1000000")]],
            resize_keyboard=True
        )
        await message.answer("Какая стоимость машины?", reply_markup=kb)

    elif message.text == "Дом":
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="3000000"), KeyboardButton(text="5000000"), KeyboardButton(text="15000000")]],
            resize_keyboard=True
        )
        await message.answer("Какая стоимость дома?", reply_markup=kb)

    elif message.text == "Пассивный доход":
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="100000"), KeyboardButton(text="500000"), KeyboardButton(text="1000000")]],
            resize_keyboard=True
        )
        await message.answer("Какой пассивный доход в месяц ты хочешь получать?", reply_markup=kb)


@dp.message(F.text.regexp(r"^\d+$"))
async def numeric_answer(message: types.Message):
    uid = message.from_user.id
    data = user_data.get(uid, {})

    # Первый ответ (цель)
    if "first" not in data:
        user_data[uid]["first"] = int(message.text)
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="10000"), KeyboardButton(text="20000"), KeyboardButton(text="30000")]],
            resize_keyboard=True
        )
        await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=kb)
        return

    # Второй ответ (инвестиции)
    if "second" not in data:
        user_data[uid]["second"] = int(message.text)

        path = user_data[uid]["path"]
        first = user_data[uid]["first"]
        monthly = user_data[uid]["second"]

        # Средняя доходность 135% годовых
        annual_rate = 1.35
        monthly_rate = (1 + annual_rate) ** (1/12) - 1

        months = 0
        balance = 0
        target = 0

        # ===== Ветвь "Пассивный доход" =====
        if path == "Пассивный доход":
            target_income = first
            balance = 1
            while balance * monthly_rate < target_income:
                balance += monthly
                balance *= (1 + monthly_rate)
                months += 1
            years = months // 12
            months = months % 12
            await message.answer(
                f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly}₽ "
                f"вы сможете получать пассивный доход {target_income}₽/мес "
                f"через {years} лет и {months} мес."
            )
            return

        # ===== Ветви "Машина" и "Дом" =====
        target = first
        while balance < target:
            balance += monthly
            balance *= (1 + monthly_rate)
            months += 1

        years = months // 12
        months = months % 12

        await message.answer(
            f"С помощью нашего ИИ-бота, при ваших инвестициях {monthly}₽ "
            f"вы сможете купить {path.lower()} стоимостью {target}₽ "
            f"через {years} лет и {months} мес."
        )


# ========== ЗАПУСК ==========
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
