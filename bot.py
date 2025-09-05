import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command

# Токен бота
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# ID группы для поддержки
SUPPORT_CHAT_ID = -1002395205551

# Создаем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Словарь для отслеживания пользователей, которые пишут в поддержку
support_users = set()

# Главное меню
def main_menu():
    keyboard = [
        [types.KeyboardButton("📊 Общая картина"), types.KeyboardButton("📝 Пройти тест")],
        [types.KeyboardButton("💰 Готов инвестировать"), types.KeyboardButton("📄 Просмотр договора оферты")],
        [types.KeyboardButton("✨ Невозможное возможно благодаря рычагам")],
        [types.KeyboardButton("Дополнительные вопросы❓"), types.KeyboardButton("Написать в поддержку")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_menu())

# Обработка кнопок меню
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "Написать в поддержку":
        support_users.add(message.from_user.id)
        await message.answer("Опишите свою проблему")
    elif message.text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)
    elif message.text == "💰 Готов инвестировать":
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton(
                    text="Открыть инструкцию",
                    url="https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex"
                )
            ]]
        )
        await message.answer("Нажмите кнопку ниже:", reply_markup=keyboard)
    else:
        # Проверяем, пишет ли пользователь в поддержку
        if message.from_user.id in support_users:
            await bot.send_message(
                SUPPORT_CHAT_ID,
                f"Сообщение от @{message.from_user.username or message.from_user.full_name}:\n{message.text}"
            )
            support_users.remove(message.from_user.id)
            await message.answer("Ваше сообщение отправлено в поддержку!")
        else:
            await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
