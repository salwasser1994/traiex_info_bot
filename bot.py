import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

API_TOKEN = os.getenv("API_TOKEN")  # Токен от BotFather

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Вопросы и варианты ---
questions = [
    {
        "question": "Считаете ли вы, что понимаете свой мир целиком, как это делают богатые и успешные люди?",
        "options": ["Да, я всё вижу и понимаю", "Нет, о чём вы говорите?", "Мой вариант ответа"]
    },
    {
        "question": "Согласны ли вы с такой картиной жизни?",
        "options": ["Не согласен", "Согласен", "Мой вариант ответа"]
    }
]

# --- Пользовательский прогресс ---
user_progress = {}
awaiting_text = {}  # словарь для отслеживания, кто пишет свой вариант

def create_keyboard(options):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=opt, callback_data=f"vote_{i}")] for i, opt in enumerate(options)]
    )

# --- /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    user_progress[message.from_user.id] = 0  # первый вопрос
    q_data = questions[0]
    await message.answer("Привет! Давай проведем опрос:")
    await message.answer(q_data["question"], reply_markup=create_keyboard(q_data["options"]))

# --- Обработка голосов ---
@dp.callback_query()
async def handle_vote(callback: CallbackQuery):
    user_id = callback.from_user.id
    index = int(callback.data.split("_")[1])
    current_q = user_progress.get(user_id, 0)
    selected_option = questions[current_q]["options"][index]

    await callback.answer()  # не показываем всплывающее окно

    if selected_option == "Мой вариант ответа":
        # Ожидаем текст от пользователя
        awaiting_text[user_id] = current_q
        await callback.message.answer("Напишите свой вариант ответа:")
        return

    if current_q == 0:
        if index == 0:  # Да, я всё вижу и понимаю
            user_progress[user_id] = 1
            next_q = questions[1]
            await callback.message.answer(next_q["question"], reply_markup=create_keyboard(next_q["options"]))
        else:
            await callback.message.answer("Спасибо за участие в опросе! ✅")
            user_progress[user_id] = 0
    else:
        await callback.message.answer("Спасибо за участие в опросе! ✅")
        user_progress[user_id] = 0

# --- Обработка текстовых ответов для "Мой вариант ответа" ---
@dp.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if user_id in awaiting_text:
        # Пользователь прислал свой вариант
        await message.answer("Хороший ответ! ✅")
        current_q = awaiting_text.pop(user_id)
        # Переходим к следующему вопросу
        next_q_index = current_q + 1
        if next_q_index < len(questions):
            user_progress[user_id] = next_q_index
            next_q = questions[next_q_index]
            await message.answer(next_q["question"], reply_markup=create_keyboard(next_q["options"]))
        else:
            user_progress[user_id] = 0
            await message.answer("Спасибо за участие в опросе! ✅")

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
