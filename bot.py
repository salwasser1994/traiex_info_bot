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
    await message.answer("Приветики! Выбирай нужный пункт меню:", reply_markup=main_menu())

# Команда /upload — отправка видео себе и вывод file_id
@dp.message(Command("upload"))
async def upload_video(message: types.Message):
    video_path = "video1.mp4"
    if not os.path.exists(video_path):
        await message.answer("❌ Видео не найдено на сервере.")
        return
    sent_video = await message.answer_video(video=video_path, caption="Тестовое видео")
    await message.answer(f"✅ File ID этого видео: {sent_video.video.file_id}")

# Обработка нажатий кнопок
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "overview":
        # После получения file_id замените эту строку на ваш file_id
        file_id = "ВАШ_FILE_ID_ЗДЕСЬ"
        await callback.message.answer_video(
            video=file_id,
            caption="Вот видео с общей картиной 📊"
        )
    else:
        await callback.answer()  # подтверждение нажатия для остальных кнопок

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
