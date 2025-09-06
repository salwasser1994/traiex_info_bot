import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    Message, CallbackQuery
)
from aiogram.filters import Command, Text

# ----------------------
# Настройки бота
# ----------------------
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ----------------------
# Главное меню
# ----------------------
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ----------------------
# Inline кнопка "В меню"
# ----------------------
def inline_back_to_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
        ]
    )
    return keyboard

# ----------------------
# FAQ вопросы и ответы
# ----------------------
FAQ = {
    "Безопасно ли пользоваться платформой?": "Да, все операции проходят через защищённое соединение, ваши данные и средства надёжно защищены.",
    "Что будет, если я потеряю доступ к аккаунту?": "Вы сможете восстановить доступ через e-mail или поддержку — ваш аккаунт не пропадёт.",
    "Нужно ли платить, чтобы начать?": "Нет, регистрация бесплатная. Вы можете изучить все материалы и только потом принять решение о вложениях.",
    "Есть ли скрытые комиссии?": "Нет, все комиссии прозрачные и заранее указаны.",
    "Можно ли вывести деньги в любой момент?": "Да, средства доступны для вывода по вашему желанию.",
    "А если я ничего не понимаю в инвестициях?": "Не страшно 🙂 Есть инструкции, видеоуроки и поддержка.",
    "Что, если платформа перестанет работать?": "Мы используем резервные сервера и проверенные механизмы.",
    "Нужно ли тратить много времени?": "Нет, достаточно уделять несколько минут в день.",
    "Есть ли гарантии?": "Мы гарантируем прозрачность, безопасность и честную работу платформы.",
    "Что такое договор оферты?": "Это договор который вы подписываете, установив галочку в центре квадратика."
}

# ----------------------
# /start команда
# ----------------------
@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer("Привет! Выберите действие из меню 👇", reply_markup=main_menu())

# ----------------------
# Обработка кнопки "В меню"
# ----------------------
@dp.callback_query(Text(text="back_to_menu"))
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text("Сделай свой выбор", reply_markup=None)
    await callback.message.answer("Выберите действие из меню 👇", reply_markup=main_menu())
    await callback.answer()

# ----------------------
# Обработка нажатий меню
# ----------------------
@dp.message()
async def handle_menu(message: Message):
    if message.text == "Часто задаваемые вопросы❓":
        # Показываем FAQ в виде ReplyKeyboard
        keyboard = [[KeyboardButton(text=q)] for q in FAQ.keys()]
        keyboard.append([KeyboardButton(text="В меню")])
        await message.answer("Выберите вопрос:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    elif message.text in FAQ:
        # Показать ответ под вопросом
        text = FAQ[message.text]
        keyboard = [[KeyboardButton(text=q)] for q in FAQ.keys() if q != message.text]
        keyboard.append([KeyboardButton(text="В меню")])
        await message.answer(f"❓ {message.text}\n\n💬 {text}", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True))
    elif message.text == "В меню":
        await message.answer("Вы вернулись в меню", reply_markup=main_menu())
    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# ----------------------
# Запуск бота
# ----------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
