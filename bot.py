import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Токен бота
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# Создаем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# FAQ вопросы и ответы
faq_dict = {
    "Безопасно ли пользоваться платформой?": "Да, все операции проходят через защищённое соединение, ваши данные и средства надёжно защищены.",
    "Что будет, если я потеряю доступ к аккаунту?": "Вы сможете восстановить доступ через e-mail или поддержку — ваш аккаунт не пропадёт.",
    "Нужно ли платить, чтобы начать?": "Нет, регистрация бесплатная. Вы можете изучить все материалы и только потом принять решение о вложениях.",
    "Есть ли скрытые комиссии?": "Нет, все комиссии прозрачные и заранее указаны. Вы всегда знаете, сколько и за что платите.",
    "Можно ли вывести деньги в любой момент?": "Да, средства доступны для вывода по вашему желанию, без «заморозки» и обязательных сроков.",
    "А если я ничего не понимаю в инвестициях?": "Не страшно 🙂 Всё построено так, чтобы даже новичок мог разобраться. Есть инструкции, видеоуроки и поддержка.",
    "Что, если платформа перестанет работать?": "Мы используем резервные сервера и проверенные механизмы. Даже в случае сбоя деньги остаются у вас.",
    "Нужно ли тратить много времени?": "Нет, достаточно уделять несколько минут в день для проверки информации и управления своим счётом.",
    "Есть ли гарантии?": "Мы не обещаем «золотых гор», но гарантируем прозрачность, безопасность и честную работу платформы.",
    "Что такое договор оферты?": "Это договор, который вы подписываете (а значит соглашаетесь с написанным) установив галочку в центре квадратика."
}

# Хранилище текущего открытого вопроса для каждого пользователя
user_current_faq = {}

# Главное меню
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Inline кнопка "В меню"
def inline_back_to_menu():
    keyboard = [
        [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

# Inline кнопка "В меню"
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()

# Обработка меню и FAQ
@dp.message()
async def handle_message(message: types.Message):
    text = message.text

    # Если пользователь выбрал FAQ
    if text == "Часто задаваемые вопросы❓":
        keyboard_buttons = [[KeyboardButton(q)] for q in faq_dict.keys()]
        await message.answer("Выберите вопрос:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))
        return

    # Если пользователь нажал на вопрос из FAQ
    if text in faq_dict:
        user_id = message.from_user.id
        current = user_current_faq.get(user_id)

        # Если повторное нажатие того же вопроса → закрыть
        if current == text:
            user_current_faq[user_id] = None
            keyboard_buttons = [[KeyboardButton(q)] for q in faq_dict.keys()]
            await message.answer("❌ Ответ скрыт", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))
        else:
            # Показать ответ под выбранным вопросом
            user_current_faq[user_id] = text
            keyboard_buttons = []
            for q in faq_dict.keys():
                keyboard_buttons.append([KeyboardButton(q)])
                if q == text:
                    keyboard_buttons.append([KeyboardButton(f"➤ {faq_dict[q]}")])
            await message.answer("✅ Ответ:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True))
        return

    # Остальное меню
    if text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)
    elif text == "💰 Готов инвестировать":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="Открыть инструкцию",
                url="https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex"
            )
        ]])
        await message.answer("Нажми на кнопку ниже, чтобы открыть инструкцию:", reply_markup=keyboard)
    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
