import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# Токен бота
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# Создаем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Главное меню (ReplyKeyboard)
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Inline-кнопка "В меню"
def inline_back_to_menu():
    keyboard = [
        [InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Тест вопросы
test_questions = [
    {
        "question": "Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
        "answers": [
            "А) Инструмент, способный анализировать огромные объемы данных, выявлять закономерности и помогать принимать более обоснованные инвестиционные решения.",
            "Б) Автоматический эксперт, который гарантированно предсказывает будущее и обеспечивает прибыль без усилий со стороны инвестора."
        ],
        "correct": 0
    },
    {
        "question": "Как ИИ может помочь в анализе рынка?",
        "answers": [
            "А) ИИ может быстро обрабатывать информацию о новостях, финансовых отчетах и исторических данных, чтобы выявить тренды и оценить риски.",
            "Б) ИИ способен заменить человеческий опыт и интуицию, принимая все инвестиционные решения за инвестора."
        ],
        "correct": 0
    },
    {
        "question": "Какую роль играет ИИ в автоматизации торговли?",
        "answers": [
            "А) ИИ полностью устраняет необходимость в человеческом контроле, автоматически генерируя прибыль.",
            "Б) ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."
        ],
        "correct": 1
    },
    {
        "question": "Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
        "answers": [
            "А) Выявление мошеннических схем и предупреждение о потенциальных рисках.",
            "Б) Обеспечение полной гарантии прибыли, независимо от рыночной ситуации."
        ],
        "correct": 0
    },
    {
        "question": "Что является ключевым фактором при использовании ИИ в инвестициях?",
        "answers": [
            "А) Полностью довериться алгоритмам и не вмешиваться в процесс.",
            "Б) Понимание ограничений ИИ, постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
        ],
        "correct": 1
    },
    {
        "question": "Можно ли рассматривать ИИ как \"рычаг\" в инвестициях?",
        "answers": [
            "А) Да, ИИ может значительно усилить возможности инвестора, позволяя ему эффективнее анализировать данные, принимать решения и управлять рисками.",
            "Б) Нет, ИИ - это лишь сложная программа, не имеющая реального влияния на результаты инвестиций."
        ],
        "correct": 0
    }
]

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(
        video=file_id,
        reply_markup=inline_back_to_menu()
    )

# Обработка inline-кнопки "В меню"
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()
    elif callback.data.startswith("test_q"):
        index = int(callback.data.replace("test_q", ""))
        question = test_questions[index]
        keyboard = InlineKeyboardMarkup()
        for i, ans in enumerate(question["answers"]):
            keyboard.add(InlineKeyboardButton(text=ans, callback_data=f"answer_{index}_{i}"))
        await callback.message.edit_text(question["question"], reply_markup=keyboard)
        await callback.answer()
    elif callback.data.startswith("answer_"):
        _, q_index, selected = callback.data.split("_")
        q_index, selected = int(q_index), int(selected)
        correct = test_questions[q_index]["correct"]
        if selected == correct:
            # Следующий вопрос или завершение
            if q_index + 1 < len(test_questions):
                question = test_questions[q_index + 1]
                keyboard = InlineKeyboardMarkup()
                for i, ans in enumerate(question["answers"]):
                    keyboard.add(InlineKeyboardButton(text=ans, callback_data=f"answer_{q_index + 1}_{i}"))
                await callback.message.edit_text(question["question"], reply_markup=keyboard)
            else:
                await callback.message.edit_text("Тест завершён! 🎉", reply_markup=inline_back_to_menu())
        else:
            # Неправильный ответ — просто оставляем вопрос и кнопки без изменений
            pass
        await callback.answer()

# Обработка нажатий меню (ReplyKeyboard)
@dp.message()
async def handle_message(message: types.Message):
    if message.text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)
    elif message.text == "💰 Готов инвестировать":
        # Просто ссылка без кнопки
        await message.answer("Инструкция: https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex")
    elif message.text == "✨ Невозможное возможно благодаря рычагам":
        instruction = ("Инструкция: Выберите один правильный ответ на каждый вопрос. "
                       "Помните, ИИ - это инструмент, а не волшебная палочка.\n\n")
        keyboard = InlineKeyboardMarkup()
        for i, ans in enumerate(test_questions[0]["answers"]):
            keyboard.add(InlineKeyboardButton(text=ans, callback_data=f"answer_0_{i}"))
        await message.answer(instruction + test_questions[0]["question"], reply_markup=keyboard)
    else:
        await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
