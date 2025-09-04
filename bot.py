import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# Токен из переменных окружения
TOKEN = os.getenv("API_Token")
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Кнопка "Показать меню" под текстом
def show_menu_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Показать меню", callback_data="show_menu")]
        ]
    )

# Главное меню (ReplyKeyboard, снизу)
def reply_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Пройти тест")],
            [KeyboardButton(text="💰 Готов инвестировать")],
            [KeyboardButton(text="📄 Просмотр договора оферты")],
            [KeyboardButton(text="🤖 Что такое бот на ИИ")],
            [KeyboardButton(text="❓ Дополнительные вопросы")]
        ],
        resize_keyboard=True
    )

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    start_text = (
        "Старт\n"
        "Итак давай начнем с осмотра всей картины целиком и полностью.\n"
        "Для чего нам нужно увидеть всю картину, да потому что только так можно увидеть все минусы и плюсы и откоректировать их так как мы этого хотим а не так как нам диктуют 'обстоятельства'.\n"
        "Так как разговор про финансы общая картинк такова, что у нас есть только один источник дохода (найм), то при не сложном подсчёте мы понимаем, что если мы хотим иметь квартиру, машину, образование детям, отдых раз в год, нам нужно около ... суммы денег.\n"
        "Если взять калькулятор и подсчитать, выходит нужно около ... лет жизни при средней заработной плате, чтобы получить желаемое.\n"
        "Очень плачевная ситуация.\n"
        "Но если добавить к сохраненной части денег ещё такой инструмент как бот на ИИ, то нам хватает (подсчет нарисовать) такое-то количество времени.\n"
        "Теперь выбор за вами.\n"
        "Хотите ли использовать новые инструменты: а именно искусственный интеллект + ежедневный сложный процент.\n"
        "Или останетесь с одним источником дохода?"
    )

    # Отправляем стартовый текст
    await message.answer(start_text)

    # Отправляем кнопку "Показать меню"
    await message.answer(
        "Нажмите кнопку, чтобы открыть главное меню:",
        reply_markup=show_menu_button()
    )

# Обработка кнопки "Показать меню"
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "show_menu":
        await callback.message.answer(
            text="Выберите пункт меню:",
            reply_markup=reply_main_menu()
        )
        await callback.answer()  # закрывает "часики" на кнопке

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
