import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

# вставь сюда токен своего бота
API_TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['getid'])
async def send_chat_id(message: Message):
    chat_id = message.chat.id
    await message.reply(f"Chat ID: {chat_id}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)