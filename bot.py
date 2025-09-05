from aiogram import Bot, Dispatcher, types
import asyncio

TOKEN = "ВАШ_ТОКЕН_БОТА"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def get_chat_id(message: types.Message):
    await message.answer(f"Chat ID этого чата: `{message.chat.id}`", parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
