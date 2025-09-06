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

# Хранилище активных чатов поддержки
support_users = set()
# Соответствие сообщений в группе ↔ пользователи
support_messages = {}

# Главное меню (ReplyKeyboard)
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓"), KeyboardButton(text="Написать в поддержку")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Inline-кнопка "В меню"
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Inline-кнопка "Завершить чат"
def inline_end_chat():
    keyboard = [[InlineKeyboardButton(text="❌ Завершить чат", callback_data="end_chat")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

# Обработка inline-кнопок
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()
    elif callback.data == "end_chat":
        user_id = callback.from_user.id
        if user_id in support_users:
            support_users.remove(user_id)
            await callback.message.answer("Чат поддержки завершён ✅", reply_markup=main_menu())
            await bot.send_message(
                SUPPORT_CHAT_ID,
                f"Чат с пользователем @{callback.from_user.username or callback.from_user.full_name} завершён ❌"
            )
        await callback.answer("Чат завершён")

# Универсальный обработчик сообщений
@dp.message()
async def handle_all_messages(message: types.Message):
    # 1️⃣ Ответы поддержки из группы
    if message.chat.id == SUPPORT_CHAT_ID:
        if message.reply_to_message and message.reply_to_message.message_id in support_messages:
            user_id = support_messages[message.reply_to_message.message_id]
            await bot.send_message(user_id, f"Ответ поддержки:\n{message.text}")
        return

    # 2️⃣ Проверка: выбрал ли пользователь пункт меню → закрываем чат
    menu_buttons = [
        "📄 Просмотр договора оферты",
        "💰 Готов инвестировать",
        "📊 Общая картина",
        "📝 Пройти тест",
        "✨ Невозможное возможно благодаря рычагам",
        "Часто задаваемые вопросы❓"
    ]
    if message.text in menu_buttons:
        if message.from_user.id in support_users:
            support_users.remove(message.from_user.id)
            await bot.send_message(
                SUPPORT_CHAT_ID,
                f"Чат с пользователем @{message.from_user.username or message.from_user.full_name} завершён ❌"
            )

    # 3️⃣ Сообщение пользователя в поддержку
    if message.from_user.id in support_users:
        sent = await bot.send_message(
            SUPPORT_CHAT_ID,
            f"Сообщение от @{message.from_user.username or message.from_user.full_name}:\n{message.text}"
        )
        support_messages[sent.message_id] = message.from_user.id
        return

    # 4️⃣ Обработка кнопок меню
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
        await message.answer(
            "Вы подключены к чату с поддержкой 👨‍💻\n"
            "Напишите свой вопрос.\n"
        )

    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
