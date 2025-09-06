import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# Токен бота
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# ID группы для поддержки
SUPPORT_CHAT_ID = -1003081706651

# Создаем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Хранилище пользователей, которые пишут в поддержку
support_users = set()

# Хранилище сообщений бота в группе для ответа пользователю
support_messages = {}

# Главное меню (ReplyKeyboard)
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Дополнительные вопросы❓"), KeyboardButton(text="Написать в поддержку")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Inline-кнопка "В меню"
def inline_back_to_menu():
    keyboard = [
        [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(
        video=file_id,
        reply_markup=inline_back_to_menu()
    )

# Обработка inline-кнопки "В меню"
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()  # закрыть "часики"

# Универсальный обработчик сообщений
@dp.message()
async def handle_all_messages(message: types.Message):
    # 1️⃣ Если сообщение из группы поддержки (ответ на сообщение бота)
    if message.chat.id == SUPPORT_CHAT_ID:
        if message.reply_to_message and message.reply_to_message.message_id in support_messages:
            user_id = support_messages[message.reply_to_message.message_id]
            await bot.send_message(user_id, f"Ответ поддержки:\n{message.text}")
        return  # не обрабатываем дальше

    # 2️⃣ Если пользователь пишет в поддержку
    if message.from_user.id in support_users:
        sent = await bot.send_message(
            SUPPORT_CHAT_ID,
            f"Сообщение от @{message.from_user.username or message.from_user.full_name}:\n{message.text}"
        )
        support_messages[sent.message_id] = message.from_user.id
        support_users.remove(message.from_user.id)
        await message.answer("Ваше сообщение отправлено в поддержку!")
        return

    # 3️⃣ Работа с кнопками
    if message.text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)

    elif message.text == "💰 Готов инвестировать":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="Открыть инструкцию",
                    url="https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex"
                )
            ]]
        )
        await message.answer("Нажми на кнопку ниже, чтобы открыть инструкцию:", reply_markup=keyboard)

    elif message.text == "Написать в поддержку":
        support_users.add(message.from_user.id)
        await message.answer("Опишите свою проблему")

    else:
        # Остальные кнопки пока без действия
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
