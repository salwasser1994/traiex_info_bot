import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# --- Токен бота ---
TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

# --- Создаем бота ---
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# --- Функция печатающегося текста с защитой от пустого сообщения ---
async def typewriter_effect(message: types.Message, text: str, delay: float = 0.05):
    """
    Эффект печатания текста ИИ по буквам.
    Защита от пустого текста с использованием невидимого символа U+2800.
    """
    if not text or text.isspace():  # если текст пустой или только пробелы
        text = "⠀"  # невидимый символ Braille blank
    
    sent_msg = await message.answer("⠀")  # первое сообщение с невидимым символом
    
    displayed_text = ""
    for char in text:
        displayed_text += char
        try:
            # Никогда не передаём пустую строку
            await sent_msg.edit_text(displayed_text or "⠀")
        except:
            pass
        await asyncio.sleep(delay)

# --- Данные FAQ ---
faq_data = {
    "Безопасно ли пользоваться платформой?": 
        "🛡️ Доступ к вашей цифровой сущности полностью защищён передовыми протоколами будущего. "
        "Ваши средства и данные хранятся в квантовой сети.",
    "Что будет, если я потеряю доступ к аккаунту?":
        "🔑 Даже при потере доступа ваша цифровая идентичность сохраняется. Восстановление через e-mail или поддержку гарантировано.",
    "Нужно ли платить, чтобы начать?":
        "💸 Регистрация бесплатна. Изучите возможности сети, прежде чем инвестировать.",
    "Есть ли скрытые комиссии?":
        "🛰️ Нет. Все операции прозрачны и отслеживаются алгоритмами мониторинга.",
    "Можно ли вывести деньги в любой момент?":
        "🚀 Средства доступны мгновенно, без заморозки и ограничений.",
    "А если я ничего не понимаю в инвестициях?":
        "🤖 Не страшно! Наш ИИ проведёт вас по маршруту и покажет оптимальные шаги.",
    "Что, если платформа перестанет работать?":
        "⚡ Система использует резервные серверы и защиту от сбоев. Ваши средства сохраняются.",
    "Нужно ли тратить много времени?":
        "⏱️ Достаточно нескольких минут в день для контроля цифровой матрицы.",
    "Есть ли гарантии?":
        "🛡️ Гарантируем прозрачность работы и защиту активов. Магических «золотых гор» нет, но система честна."
}

# --- Тестовые вопросы ---
test_questions = [
    {
        "q": "Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
        "options": [
            "Инструмент, способный анализировать огромные объемы данных.",
            "Автоматический эксперт, который гарантированно предсказывает будущее."
        ],
        "correct": "Инструмент, способный анализировать огромные объемы данных."
    },
    {
        "q": "Как ИИ может помочь в анализе рынка?",
        "options": [
            "Быстро обрабатывать новости, отчёты и данные, выявляя тренды.",
            "Полностью заменить человека и принимать все решения."
        ],
        "correct": "Быстро обрабатывать новости, отчёты и данные, выявляя тренды."
    },
    {
        "q": "Какую роль играет ИИ в автоматизации торговли?",
        "options": [
            "ИИ полностью устраняет необходимость в человеческом контроле, автоматически генерируя прибыль.",
            "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."
        ],
        "correct": "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."
    },
    {
        "q": "Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
        "options": [
            "Выявление мошеннических схем и предупреждение о потенциальных рисках.",
            "Обеспечение полной гарантии прибыли, независимо от рыночной ситуации."
        ],
        "correct": "Выявление мошеннических схем и предупреждение о потенциальных рисках."
    },
    {
        "q": "Что является ключевым фактором при использовании ИИ в инвестициях?",
        "options": [
            "Полностью довериться алгоритмам и не вмешиваться в процесс.",
            "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
        ],
        "correct": "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."
    }
]

# --- Состояния пользователей ---
user_progress = {}
user_state = {}

# --- Главное меню футуристическое ---
def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Финансовая матрица ⚡"), KeyboardButton(text="📝 Пройти тест 🤖")],
        [KeyboardButton(text="💰 Подключиться к инвестиционной сети 🛸"), KeyboardButton(text="📄 Договор оферты 📡")],
        [KeyboardButton(text="✨ Использовать рычаги будущего 🔮")],
        [KeyboardButton(text="❓ Часто задаваемые вопросы AI")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню FAQ ---
def faq_menu():
    keyboard = [[KeyboardButton(text=q)] for q in faq_data.keys()]
    keyboard.append([KeyboardButton(text="⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Меню перед тестом ---
def start_test_menu():
    keyboard = [
        [KeyboardButton(text="🚀 Начать тест")],
        [KeyboardButton(text="⬅ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Inline кнопка «В меню» ---
def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- Отправка вопроса с прогресс-баром и эффектом печатания ---
async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    progress = int((idx + 1) / len(test_questions) * 10)
    bar = "▓" * progress + "░" * (10 - progress)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=opt)] for opt in q["options"]] + [[KeyboardButton(text="⬅ Назад в меню")]],
        resize_keyboard=True
    )
    text_to_display = f"🤖 Вопрос {idx + 1}/{len(test_questions)} {bar}\n\n{q['q']}"
    await typewriter_effect(message, text_to_display, delay=0.03)

# --- Команда /start ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

# --- Inline callback ---
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Выберите действие из меню 👇", reply_markup=main_menu())
        await callback.answer()

# --- Обработка сообщений ---
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # --- Общая картина ---
    if message.text == "📊 Финансовая матрица ⚡":
        user_state[user_id] = "step1"
        text1 = (
            "🤖 ИИ активирован. Анализ финансовой матрицы:\n\n"
            "Для полного видения ситуации используем данные, таблицы и прогнозы.\n"
            "🔹 Таблицы, подсвечивающие реальное положение дел:"
        )
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        await typewriter_effect(message, text1, delay=0.04)
