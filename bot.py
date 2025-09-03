import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Берём токен из Environment Variables Render
TOKEN = os.getenv("API_Token")
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

# Создаем бота с default properties
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Главное меню
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

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Приветик! Выбирай нужный пункт меню:", reply_markup=main_menu())

# Обработка нажатий кнопок
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "overview":
        video_path = "video1.mp4"  # локальный файл на сервере
        if os.path.exists(video_path):
            # Просто передаём путь к файлу
            await callback.message.answer_video(
                video=video_path,
                caption="Вот видео с общей картиной 📊",
                supports_streaming=True  # сразу можно стримить
            )
        else:
            await callback.message.answer("Видео не найдено на сервере.")
    else:
        await callback.answer("Кнопка нажата!")  # подтверждение для других кнопок

# Запуск бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
