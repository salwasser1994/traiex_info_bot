import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# Токен из переменных окружения (Render -> Environment)
TOKEN = os.getenv("API_Token")
if not TOKEN:
    raise ValueError("API_Token не найден в переменных окружения!")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ---- НАСТРОЙКИ ----
WELCOME_VIDEO_ID = "BAACAgQAAxkDAAIC12i4SwjQT7gKv_ccxLe2dV5GAYreAAIqIQACIJ7IUZCFvYLU5H0KNgQ"

# ---- INLINE МЕНЮ ----
def inline_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📝 Пройти тест", callback_data="test")],
        [InlineKeyboardButton(text="💰 Готов инвестировать", callback_data="invest")],
        [InlineKeyboardButton(text="📄 Просмотр договора оферты", callback_data="agreement")],
        [InlineKeyboardButton(text="🤖 Что такое бот на ИИ", callback_data="ai_bot")],
        [InlineKeyboardButton(text="❓ Дополнительные вопросы", callback_data="faq")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# ---- REPLY КЛАВИАТУРА ----
def reply_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Пройти тест"), KeyboardButton(text="💰 Готов инвестировать")],
            [KeyboardButton(text="📄 Просмотр договора оферты"), KeyboardButton(text="🤖 Что такое бот на ИИ")],
            [KeyboardButton(text="❓ Дополнительные вопросы")]
        ],
        resize_keyboard=True,
        input_field_placeholder="любой текст…"
    )

# ---- START ----
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Отправляем приветственное видео + кнопку показать меню
    show_menu_btn = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📊 Показать меню", callback_data="show_menu")]]
    )
    await message.answer_video(
        video=WELCOME_VIDEO_ID,
        caption="любой текст",
        reply_markup=show_menu_btn
    )

# ---- CALLBACKS ----
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    data = callback.data

    if data == "show_menu":
        # 1) Сообщение с inline-меню
        await callback.message.answer("📊 Главное меню:", reply_markup=inline_main_menu())
        # 2) Включаем Reply-клавиатуру со всеми пунктами
        await callback.message.answer("Клавиатура открыта 👇", reply_markup=reply_menu())
        await callback.answer()
        return

    # Заглушки для остальных пунктов (inline)
    mapping = {
        "test": "📝 Пройти тест",
        "invest": "💰 Готов инвестировать",
        "agreement": "📄 Просмотр договора оферты",
        "ai_bot": "🤖 Что такое бот на ИИ",
        "faq": "❓ Дополнительные вопросы"
    }
    if data in mapping:
        await callback.answer()
        await callback.message.answer(f"Вы выбрали: {mapping[data]} (действие пока не реализовано) ✅")
        return

    await callback.answer()

# ---- ОБРАБОТКА REPLY-КНОПОК (текста) ----
@dp.message(F.text.in_({
    "📝 Пройти тест",
    "💰 Готов инвестировать",
    "📄 Просмотр договора оферты",
    "🤖 Что такое бот на ИИ",
    "❓ Дополнительные вопросы"
}))
async def handle_reply_buttons(message: types.Message):
    await message.answer(f"Вы нажали: {message.text} (действие пока не реализовано) ✅")

# ---- RUN ----
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
