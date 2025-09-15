import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio

logging.basicConfig(level=logging.INFO)

# === Конфиг ===
BOT_TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
ADMIN_ID = -1003081706651  # твой групповой чат

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище состояния пользователей
user_data = {}


# === Старт ===
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_data[message.from_user.id] = {}  # обнуляем прогресс

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Хочу разобраться 💡")],
            [KeyboardButton(text="Неинтересно 🚫")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я — твой финансовый помощник Алексей Финансович. "
        "Моя цель — помочь тебе понять, как можно приумножить капитал 📈\n\n"
        "Скажи честно: инвестиции тебе интересны?",
        reply_markup=kb
    )


# === Обработка выбора интереса ===
@dp.message(F.text == "Хочу разобраться 💡")
async def handle_interested(message: Message):
    user_data[message.from_user.id]["interest"] = "Да"

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Дом 🏠"), KeyboardButton(text="Машина 🚗")],
            [KeyboardButton(text="Пассивный доход 💸")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Отлично 🙌 Рад, что тебе интересно!\n\n"
        "Скажи, какая цель для тебя важнее всего сейчас?",
        reply_markup=kb
    )


@dp.message(F.text == "Неинтересно 🚫")
async def handle_not_interested(message: Message):
    user_data[message.from_user.id]["interest"] = "Нет"

    await message.answer(
        "Понял тебя 🙂\n"
        "Если захочешь узнать больше о том, как люди достигают своих финансовых целей, "
        "можешь вернуться в любой момент — я всегда здесь."
    )


# === Цель ===
@dp.message(F.text.in_(["Дом 🏠", "Машина 🚗", "Пассивный доход 💸"]))
async def handle_goal(message: Message):
    user_data[message.from_user.id]["goal"] = message.text

    if message.text == "Дом 🏠":
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="3 000 000 ₽"), KeyboardButton(text="5 000 000 ₽")],
                [KeyboardButton(text="10 000 000 ₽")]
            ],
            resize_keyboard=True
        )
    elif message.text == "Машина 🚗":
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="1 000 000 ₽"), KeyboardButton(text="2 000 000 ₽")],
                [KeyboardButton(text="3 000 000 ₽")]
            ],
            resize_keyboard=True
        )
    else:  # Пассивный доход
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="50 000 ₽/мес"), KeyboardButton(text="100 000 ₽/мес")],
                [KeyboardButton(text="200 000 ₽/мес")]
            ],
            resize_keyboard=True
        )

    await message.answer(
        f"Хорошо 👍 Давай уточним.\n\n"
        f"Сколько денег тебе нужно, чтобы реализовать цель «{message.text}»?",
        reply_markup=kb
    )


# === Сумма ===
@dp.message(F.text.regexp(r"[0-9 ]+₽|₽/мес"))
async def handle_sum(message: Message):
    user_data[message.from_user.id]["sum"] = message.text

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Связаться с человеком 👨‍💼")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        f"Отлично 👌 С твоей целью и выбранной суммой это вполне реально.\n\n"
        "Я могу подсказать, как начать двигаться к этому результату 🚀\n\n"
        "Хочешь, я свяжу тебя с живым помощником, который объяснит детали?",
        reply_markup=kb
    )


# === Лид ===
@dp.message(F.text == "Связаться с человеком 👨‍💼")
async def handle_contact(message: Message):
    await message.answer(
        "Супер 🎉 Я передал твой запрос нашему консультанту. "
        "В ближайшее время он свяжется с тобой в этом чате 👨‍💻"
    )

    data = user_data.get(message.from_user.id, {})
    interest = data.get("interest", "—")
    goal = data.get("goal", "—")
    summ = data.get("sum", "—")

    # Уведомляем админ-чат
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔥 Новый лид!\n\n"
            f"👤 Пользователь: @{message.from_user.username}\n"
            f"Имя: {message.from_user.full_name}\n"
            f"ID: {message.from_user.id}\n\n"
            f"📌 Интерес: {interest}\n"
            f"🎯 Цель: {goal}\n"
            f"💰 Сумма: {summ}\n\n"
            f"✅ Хочет связаться с человеком 👨‍💼"
        )
    )


# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())