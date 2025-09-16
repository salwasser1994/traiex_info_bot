import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

logging.basicConfig(level=logging.INFO)

# === Конфиг ===
BOT_TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"
ADMIN_ID = -1003081706651  # групповой чат

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище состояния пользователей
user_data = {}


# === Старт ===
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_data[message.from_user.id] = {}  # обнуляем прогресс

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Хочу разобраться 💡", callback_data="interest_yes")],
        [InlineKeyboardButton(text="Неинтересно 🚫", callback_data="interest_no")]
    ])

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я — твой финансовый помощник Алексей Финансович. "
        "Моя цель — помочь тебе понять, как можно приумножить капитал 📈\n\n"
        "Скажи честно: инвестиции тебе интересны?",
        reply_markup=kb
    )


# === Интерес ===
@dp.callback_query(F.data == "interest_yes")
async def handle_interested(callback: CallbackQuery):
    user_data[callback.from_user.id]["interest"] = "Да"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дом 🏠", callback_data="goal_home"),
         InlineKeyboardButton(text="Машина 🚗", callback_data="goal_car")],
        [InlineKeyboardButton(text="Пассивный доход 💸", callback_data="goal_passive")]
    ])

    await callback.message.answer(
        "Отлично 🙌 Рад, что тебе интересно!\n\n"
        "Скажи, какая цель для тебя важнее всего сейчас?",
        reply_markup=kb
    )
    await callback.answer()


@dp.callback_query(F.data == "interest_no")
async def handle_not_interested(callback: CallbackQuery):
    user_data[callback.from_user.id]["interest"] = "Нет"

    await callback.message.answer(
        "Понял тебя 🙂\n"
        "Если захочешь узнать больше о том, как люди достигают своих финансовых целей, "
        "можешь вернуться в любой момент — я всегда здесь."
    )
    await callback.answer()


# === Цели ===
@dp.callback_query(F.data.startswith("goal_"))
async def handle_goal(callback: CallbackQuery):
    goal_map = {
        "goal_home": "Дом 🏠",
        "goal_car": "Машина 🚗",
        "goal_passive": "Пассивный доход 💸"
    }
    goal = goal_map[callback.data]
    user_data[callback.from_user.id]["goal"] = goal

    if goal == "Дом 🏠":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="3 000 000 ₽", callback_data="sum_3000000"),
             InlineKeyboardButton(text="5 000 000 ₽", callback_data="sum_5000000")],
            [InlineKeyboardButton(text="10 000 000 ₽", callback_data="sum_10000000")]
        ])
    elif goal == "Машина 🚗":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1 000 000 ₽", callback_data="sum_1000000"),
             InlineKeyboardButton(text="2 000 000 ₽", callback_data="sum_2000000")],
            [InlineKeyboardButton(text="3 000 000 ₽", callback_data="sum_3000000car")]
        ])
    else:  # Пассивный доход
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="50 000 ₽/мес", callback_data="sum_50000"),
             InlineKeyboardButton(text="100 000 ₽/мес", callback_data="sum_100000")],
            [InlineKeyboardButton(text="200 000 ₽/мес", callback_data="sum_200000")]
        ])

    await callback.message.answer(
        f"Хорошо 👍 Давай уточним.\n\n"
        f"Сколько денег тебе нужно, чтобы реализовать цель «{goal}»?",
        reply_markup=kb
    )
    await callback.answer()


# === Сумма ===
@dp.callback_query(F.data.startswith("sum_"))
async def handle_sum(callback: CallbackQuery):
    sums_map = {
        "sum_3000000": "3 000 000 ₽",
        "sum_5000000": "5 000 000 ₽",
        "sum_10000000": "10 000 000 ₽",
        "sum_1000000": "1 000 000 ₽",
        "sum_2000000": "2 000 000 ₽",
        "sum_3000000car": "3 000 000 ₽",
        "sum_50000": "50 000 ₽/мес",
        "sum_100000": "100 000 ₽/мес",
        "sum_200000": "200 000 ₽/мес"
    }

    user_data[callback.from_user.id]["sum"] = sums_map.get(callback.data, "—")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Связаться с человеком 👨‍💼", callback_data="contact")]
    ])

    await callback.message.answer(
        f"Отлично 👌 С твоей целью и выбранной суммой это вполне реально.\n\n"
        "Я могу подсказать, как начать двигаться к этому результату 🚀\n\n"
        "Хочешь, я свяжу тебя с живым помощником, который объяснит детали?",
        reply_markup=kb
    )
    await callback.answer()


# === Лид ===
@dp.callback_query(F.data == "contact")
async def handle_contact(callback: CallbackQuery):
    await callback.message.answer(
        "Супер 🎉 Я передал твой запрос нашему консультанту. "
        "В ближайшее время он свяжется с тобой в этом чате 👨‍💻"
    )

    data = user_data.get(callback.from_user.id, {})
    interest = data.get("interest", "—")
    goal = data.get("goal", "—")
    summ = data.get("sum", "—")

    # Уведомляем админ-чат
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔥 Новый лид!\n\n"
            f"👤 Пользователь: @{callback.from_user.username}\n"
            f"Имя: {callback.from_user.full_name}\n"
            f"ID: {callback.from_user.id}\n\n"
            f"📌 Интерес: {interest}\n"
            f"🎯 Цель: {goal}\n"
            f"💰 Сумма: {summ}\n\n"
            f"✅ Хочет связаться с человеком 👨‍💼"
        )
    )
    await callback.answer()


# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
