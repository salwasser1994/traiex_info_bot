import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Укажи свой токен бота
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Главное меню с кнопками без действия
def main_menu():
    keyboard = [
        [InlineKeyboardButton(text="📊 Общая картина", callback_data="overview")],
        [InlineKeyboardButton(text="📝 Пройти тест", callback_data="test")],
        [InlineKeyboardButton(text="💰 Готов инвестировать", callback_data="invest")],
        [InlineKeyboardButton(text="📄 Просмотр договора оферты", callback_data="agreement")],
        [InlineKeyboardButton(text="🤖 Что такое бот на ИИ", callback_data="ai_bot")],
        [InlineKeyboardButton(text="❓ Дополнительные вопросы", callback_data="faq")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Хэндлер для /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Выбирай нужный пункт меню:", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
