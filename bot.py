import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

TOKEN = "8473772441:AAHpXfxOxR-OL6e3GSfh4xvgiDdykQhgTus"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# FAQ
faq_data = {
    "Безопасно ли пользоваться платформой?": "Да, все операции проходят через защищённое соединение...",
    "Что будет, если я потеряю доступ к аккаунту?": "Вы сможете восстановить доступ через e-mail или поддержку...",
    "Нужно ли платить, чтобы начать?": "Нет, регистрация бесплатная...",
    "Есть ли скрытые комиссии?": "Нет, все комиссии прозрачные...",
    "Можно ли вывести деньги в любой момент?": "Да, средства доступны для вывода...",
    "А если я ничего не понимаю в инвестициях?": "Не страшно 🙂 Всё построено так, чтобы даже новичок мог разобраться...",
    "Что, если платформа перестанет работать?": "Мы используем резервные сервера и проверенные механизмы...",
    "Нужно ли тратить много времени?": "Нет, достаточно уделять несколько минут в день...",
    "Есть ли гарантии?": "Мы не обещаем «золотых гор», но гарантируем прозрачность, безопасность и честную работу платформы."
}

# --- Тестовые вопросы ---
test_questions = [
    {"q": "Что такое Искусственный Интеллект (ИИ) в контексте инвестиций?",
     "options": ["Инструмент, способный анализировать огромные объемы данных.",
                 "Автоматический эксперт, который гарантированно предсказывает будущее."],
     "correct": "Инструмент, способный анализировать огромные объемы данных."},
    {"q": "Как ИИ может помочь в анализе рынка?",
     "options": ["Быстро обрабатывать новости, отчёты и данные, выявляя тренды.",
                 "Полностью заменить человека и принимать все решения."],
     "correct": "Быстро обрабатывать новости, отчёты и данные, выявляя тренды."},
    {"q": "Какую роль играет ИИ в автоматизации торговли?",
     "options": ["ИИ полностью устраняет необходимость в человеческом контроле, автоматически генерируя прибыль.",
                 "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."],
     "correct": "ИИ может автоматизировать исполнение торговых стратегий, основанных на заданных параметрах, обеспечивая более быструю и точную торговлю."},
    {"q": "Какую из этих задач ИИ выполняет эффективно в сфере инвестиций?",
     "options": ["Выявление мошеннических схем и предупреждение о потенциальных рисках.",
                 "Обеспечение полной гарантии прибыли, независимо от рыночной ситуации."],
     "correct": "Выявление мошеннических схем и предупреждение о потенциальных рисках."},
    {"q": "Что является ключевым фактором при использовании ИИ в инвестициях?",
     "options": ["Полностью довериться алгоритмам и не вмешиваться в процесс.",
                 "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."],
     "correct": "Постоянный контроль и корректировка стратегии на основе человеческого анализа и опыта."}
]

user_progress = {}
user_state = {}
user_data = {}

goal_options = ["Машина", "Дом", "Пассивный доход"]
cost_options = {
    "Машина": ["100 000 ₽", "500 000 ₽", "1 000 000 ₽"],
    "Дом": ["3 000 000 ₽", "5 000 000 ₽", "15 000 000 ₽"]
}
monthly_options = ["10 000 ₽", "20 000 ₽", "30 000 ₽"]

def main_menu():
    keyboard = [
        [KeyboardButton(text="📊 Общая картина"), KeyboardButton(text="📝 Пройти тест")],
        [KeyboardButton(text="💰 Готов инвестировать"), KeyboardButton(text="📄 Просмотр договора оферты")],
        [KeyboardButton(text="✨ Невозможное возможно благодаря рычагам")],
        [KeyboardButton(text="Часто задаваемые вопросы❓")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def faq_menu():
    keyboard = [[KeyboardButton(text="⬅ Назад в меню")]] + [[KeyboardButton(text=q)] for q in faq_data.keys()]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def start_test_menu():
    keyboard = [[KeyboardButton(text="🚀 Начать тест")],[KeyboardButton(text="⬅ Назад в меню")]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def option_keyboard(options):
    kb = [[KeyboardButton(text=opt)] for opt in options]
    kb.append([KeyboardButton(text="⬅ Назад в меню")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def post_calc_menu():
    keyboard = [
        [KeyboardButton(text="💰 Готов инвестировать")],
        [KeyboardButton(text="Не готов")],
        [KeyboardButton(text="Пройти тест заново")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def send_test_question(message: types.Message, idx: int):
    q = test_questions[idx]
    keyboard = option_keyboard(q["options"])
    await message.answer(q["q"], reply_markup=keyboard)

def inline_back_to_menu():
    keyboard = [[InlineKeyboardButton(text="В меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    file_id = "BAACAgQAAxkDAAIEgGi5kTsunsNKCxSgT62lGkOro6iLAAI8KgACIJ7QUfgrP_Y9_DJKNgQ"
    await message.answer_video(video=file_id, reply_markup=inline_back_to_menu())

@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if text == "⬅ Назад в меню" or text == "Не готов":
        user_state.pop(user_id, None)
        user_data.pop(user_id, None)
        user_progress.pop(user_id, None)
        await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
        return

    # Общая картина
    if text == "📊 Общая картина":
        user_state[user_id] = "step1"
        await message.answer("Финансовая картина...", reply_markup=option_keyboard(["⬅ Назад в меню","Далее➡"]))
        return
    elif user_state.get(user_id) == "step1" and text == "Далее➡":
        user_state[user_id] = "step2"
        await message.answer_photo(photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
                                 reply_markup=option_keyboard(["⬅ Назад в меню","Далее➡"]))
        return
    elif user_state.get(user_id) == "step2" and text == "Далее➡":
        del user_state[user_id]
        await message.answer("Описание итогов...", reply_markup=main_menu())
        return

    elif text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)
        return
    elif text == "💰 Готов инвестировать":
        await message.answer("https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex",
        reply_markup=main_menu())
        return
    elif text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())
        return
    elif text in faq_data:
        await message.answer(faq_data[text])
        return
    elif text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer("📘 Инструкция...", reply_markup=start_test_menu())
        return
    elif text == "🚀 Начать тест":
        user_progress[user_id] = 0
        await send_test_question(message, 0)
        return

    # --- Тест / инвестиции / пассивный доход ---
    if text == "📝 Пройти тест":
        user_state[user_id] = "choose_goal"
        await message.answer("Какова твоя цель?", reply_markup=option_keyboard(goal_options))
        return

    # Выбор цели
    if user_state.get(user_id) == "choose_goal":
        if text in ["Машина", "Дом"]:
            user_data[user_id] = {"goal": text}
            user_state[user_id] = "choose_cost"
            await message.answer(f"Какая стоимость {text.lower()}?", reply_markup=option_keyboard(cost_options[text]))
        elif text == "Пассивный доход":
            user_data[user_id] = {"goal": text}
            user_state[user_id] = "choose_target_income"
            await message.answer("Сколько в месяц вы хотите получать?", reply_markup=option_keyboard(["100 000 ₽","500 000 ₽","1 000 000 ₽"]))
        else:
            await message.answer("Пожалуйста, выберите одну из предложенных целей.")
        return

    # Машина / Дом — выбор стоимости
    if user_state.get(user_id) == "choose_cost":
        goal = user_data[user_id]["goal"]
        if text in cost_options[goal]:
            cost = int(text.replace(" ₽","").replace(" ",""))
            user_data[user_id]["cost"] = cost
            user_state[user_id] = "choose_monthly"
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=option_keyboard(monthly_options))
        else:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    # Машина / Дом — расчет накоплений
    if user_state.get(user_id) == "choose_monthly":
        try:
            monthly = int(text.replace(" ₽","").replace(" ",""))
            user_data[user_id]["monthly"] = monthly
            cost = user_data[user_id]["cost"]
            total = 0
            month = 0
            monthly_rate = 0.1125
            monthly_totals = []

            while total < cost:
                month += 1
                total = (total + monthly)*(1+monthly_rate)
                monthly_totals.append(total)

            msg = "📈 Накопления по месяцам с учетом ежемесячного сложного процента 11,25%:\n\n"
            for i,val in enumerate(monthly_totals,start=1):
                if i<=3 or i>len(monthly_totals)-3:
                    msg+=f"Месяц {i}: {int(val):,} ₽\n"
                elif i==4:
                    msg+="...\n"

            msg+=f"\nС вашей ежемесячной инвестицией {monthly:,} ₽ вы сможете накопить на {user_data[user_id]['goal'].lower()} стоимостью {cost:,} ₽ примерно через {month} месяцев.\n"
            msg+="Важно: расчет учитывает сложный процент."

            await message.answer(msg, reply_markup=post_calc_menu())
            user_state.pop(user_id)
        except:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    # Пассивный доход — выбор желаемого дохода
    if user_state.get(user_id) == "choose_target_income":
        if text in ["100 000 ₽","500 000 ₽","1 000 000 ₽"]:
            target_income = int(text.replace(" ₽","").replace(" ",""))
            user_data[user_id]["target_income"] = target_income
            user_state[user_id] = "choose_monthly_passive"
            await message.answer("Сколько вы готовы инвестировать в месяц?", reply_markup=option_keyboard(monthly_options))
        else:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    # Пассивный доход — расчет
    if user_state.get(user_id) == "choose_monthly_passive":
        try:
            monthly = int(text.replace(" ₽","").replace(" ",""))
            user_data[user_id]["monthly"] = monthly
            target_income = user_data[user_id]["target_income"]
            monthly_rate = 0.1125
            month = 0
            capital = 0
            monthly_totals = []

            while True:
                month += 1
                capital = (capital + monthly)*(1+monthly_rate)
                passive = capital*monthly_rate
                monthly_totals.append(passive)
                if passive>=target_income:
                    break

            msg = "📈 Пассивный доход по месяцам:\n\n"
            for i,pas in enumerate(monthly_totals,start=1):
                if i<=3 or i>len(monthly_totals)-3:
                    msg+=f"Месяц {i}: {int(pas):,} ₽\n"
                elif i==4:
                    msg+="...\n"

            msg+=f"\nПри вашей ежемесячной инвестиции {monthly:,} ₽ вы сможете получать пассивный доход {target_income:,} ₽/мес примерно через {month} месяцев.\n"
            msg+="Важно: расчет учитывает сложный процент."

            await message.answer(msg, reply_markup=post_calc_menu())
            user_state.pop(user_id)
        except:
            await message.answer("Пожалуйста, выберите одну из предложенных сумм.")
        return

    # Пройти тест заново
    if text == "Пройти тест заново":
        user_state[user_id] = "choose_goal"
        await message.answer("Какова твоя цель?", reply_markup=option_keyboard(goal_options))
        return

    # Тест на ИИ
    if user_id in user_progress:
        idx = user_progress[user_id]
        q = test_questions[idx]
        if text == q["correct"]:
            await message.answer("✅ Правильно!")
            idx+=1
            if idx<len(test_questions):
                user_progress[user_id]=idx
                await send_test_question(message, idx)
            else:
                await message.answer("🎉 Тест завершён!", reply_markup=main_menu())
                del user_progress[user_id]
        elif text=="⬅ Назад в меню":
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            del user_progress[user_id]
        return

    await message.answer("Выберите действие из меню 👇", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
