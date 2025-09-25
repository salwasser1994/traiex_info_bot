import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# --- Читаем токен из переменной окружения Railway ---
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Добавь его в Variables на Railway.")

# --- Создаём бота и диспетчер ---
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


invest_requests = {}
already_invested = set()


# FAQ
faq_data = {
    "Сколько нужно денег, чтобы начать инвестировать?": """Минимальный вход составляет 150 USDT:
- 50 USDT — стоимость подписки,
- 100 USDT — рабочий депозит.""",

    "Какова доходность в месяц?": """Ориентировочная доходность — от 6% до 12% в месяц. 
Показатели могут меняться в зависимости от результатов торговли.""",

    "Можно ли сразу снять депозит?": """Да, вывод возможен в любой момент, если отсутствуют форс-мажорные обстоятельства. 
Перед началом работы рекомендуется ознакомиться с договором оферты.""",

    "Как зарегистрироваться?": "https://traiex.gitbook.io/user-guides/ru/kak-zaregistrirovatsya-na-traiex",

    "Где посмотреть лицензию?": """Все документы и лицензии размещены на официальном сайте биржи: 
https://www.traiex.com/ru/termsandconditions?anchor=1""",

    "Есть ли поддержка?": """Да, служба поддержки доступна и готова помочь: 
https://traiex-help.freshdesk.com/support/home""",

    "Есть ли гарантии?": """Гарантированной прибыли нет. Если кто-то обещает стопроцентные гарантии, это должно вызвать вопросы. 
Все условия подробно описаны в договоре оферты."""
}

# --- Тестовые вопросы ---
test_questions = [
    {"q": "Если подобрать длину рычага, можно ли поднять любой вес?",
     "options": ["Конечно, точка опоры решает", "Нет, невозможно"],
     "correct": "Конечно, точка опоры решает"},

    {"q": "Как быстрее всего добраться от Владивостока до Москвы?",
     "options": ["Самолёт", "Машина", "Поезд"],
     "correct": "Самолёт"},

    {"q": "Как поднять плиту на 10 этаж?",
     "options": ["Кран-рычаг", "100 человек", "Вертолёт"],
     "correct": "Кран-рычаг"},

    {"q": "Есть ли рычаги в финансах?",
     "options": ["Да, искусвенный интелект", "Сложный процент", "Не понимаю"],
     "correct": "Да, искусвенный интелект"},

    {"q": "Что такое ИИ в инвестициях?",
     "options": ["Анализ данных, помощь", "Гарант прибыли"],
     "correct": "Анализ данных, помощь"},

    {"q": "Как ИИ помогает в анализе рынка?",
     "options": ["Выявляет тренды, риски", "Заменяет человека"],
     "correct": "Выявляет тренды, риски"},

    {"q": "Роль ИИ в автоматизации торговли?",
     "options": ["Автоприбыль", "Быстрое исполнение"],
     "correct": "Быстрое исполнение"},

    {"q": "Главный фактор при использовании ИИ?",
     "options": ["Полностью довериться", "Контроль и корректировка"],
     "correct": "Контроль и корректировка"},

    {"q": "Можно ли считать ИИ рычагом в инвестициях?",
     "options": ["Да, усиливает инвестора", "Нет, просто программа"],
     "correct": "Да, усиливает инвестора"}
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

from aiogram import F

# --- Все сообщения от пользователей в личке ---
@dp.message(F.chat.id != -1003081706651)
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # словари для родительного падежа и итоговой формулировки
    goal_genitive = {
        "Машина": "машины",
        "Дом": "дома",
        "Пассивный доход": "пассивного дохода"
    }

    goal_phrase = {
        "Машина": "купить машину стоимостью",
        "Дом": "купить дом стоимостью",
        "Пассивный доход": "получать пассивный доход"
    }

    # --- Сначала обрабатываем конкретные команды меню ---
    if text == "📊 Общая картина":
        user_state[user_id] = "step1"
        text1 = (
            "Чтобы увидеть всю финансовую картину целиком и полностью, нужно смотреть не только глазами, "
            "но и теми частями тела, которые выведут все необходимые цифры в таблицы, сделают сравнение "
            "и конечно же сделают определенные выводы.\n\n"
            "И так таблицы, которые подсвечивают реальное положение дел:"
        )
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        await message.answer(text1, reply_markup=keyboard)
        return

    elif user_state.get(user_id) == "step1" and text == "Далее➡":
        user_state[user_id] = "step2"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="⬅ Назад в меню"), KeyboardButton(text="Далее➡")]],
            resize_keyboard=True
        )
        await message.answer_photo(
            photo="AgACAgQAAxkBAAIM0Gi9LaXmP4pct66F2FEKUu0WAAF84gACqMoxG5bI6VHDQO5xqprkdwEAAwIAA3kAAzYE",
            reply_markup=keyboard
        )
        return

    elif user_state.get(user_id) == "step2" and text == "Далее➡":
        del user_state[user_id]
        text2 = (
            "Стоит отметить что таблица сделана на примерных цифрах (сейчас именно такие), "
            "потому как ежедневная торговля имеет разную доходность, но основная мысль думаю понятна:\n\n"
            "— если ничего не делать будет один результат\n"
            "— если делать, но частично будет другой результат\n"
            "— и если использовать всё что имеем (искусственный интеллект + сложный процент), "
            "получим то что нам надо (за короткий срок приличные результаты)\n\n"
            "Вот почему так важно видеть всю картину целиком."
        )
        await message.answer(text2, reply_markup=main_menu())
        return

    elif text in ["⬅ Назад в меню", "Не готов"]:
        if user_state.get(user_id) not in ["step1", "step2"]:
            user_state.pop(user_id, None)
            user_data.pop(user_id, None)
            user_progress.pop(user_id, None)
            await message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())
            return

    elif text == "📄 Просмотр договора оферты":
        file_id = "BQACAgQAAxkBAAIFOGi6vNHLzH9IyJt0q7_V4y73FcdrAAKXGwACeDjZUSdnK1dqaQoPNgQ"
        await message.answer_document(file_id)
        return

    # список разработчиков, для которых нет ограничения
    DEV_IDS = [5205381793, 454141239, 1623272928] 

    # --- НОВЫЙ КОД: кнопка "Готов инвестировать"
    if text == "💰 Готов инвестировать":
        user_id = message.from_user.id

        if user_id in already_invested and user_id not in DEV_IDS:
            await message.answer(
                "⚠️ Вы уже отправили заявку. Подождите, пока с вами свяжется помощник.",
                reply_markup=main_menu()
            )
            return

        # Если еще не отправлял — добавляем в множество
        already_invested.add(user_id)

        user = message.from_user
        user_info = (
            f"🚨 Новый инвестор!\n\n"
            f"👤 Имя: {user.full_name}\n"
            f"🆔 Telegram ID: {user.id}\n"
            f"💬 Username: @{user.username if user.username else 'нет'}\n"
            f"🌍 Язык: {user.language_code}\n"
        )

        # Сразу создаем клавиатуру
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Подтвердить заявку",
                callback_data="confirm_{}".format(user.id)  # лучше использовать user.id вместо message_id
            )]
        ])

        sent = await bot.send_message(
            chat_id=-1003081706651,
            text=user_info,
            reply_markup=keyboard
        )

        # Сохраняем текст инвестора
        invest_requests[user.id] = {
            "user_id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "text": user_info,
            "group_msg_id": sent.message_id  # для подтверждения вложения
        }


        # Отправляем пользователю подтверждение
        await message.answer(
            "🎉 Поздравляю! С вами скоро свяжется ваш личный помощник, чтобы помочь вам.",
            reply_markup=main_menu()
        )
        return

    elif text == "Часто задаваемые вопросы❓":
        await message.answer("Выберите интересующий вопрос:", reply_markup=faq_menu())
        return
    elif text in faq_data:
        await message.answer(faq_data[text])
        return
    elif text == "✨ Невозможное возможно благодаря рычагам":
        await message.answer("📘 Инструкция:\n\nВыберите один правильный ответ на каждый вопрос.\n"
                             "Помните, ИИ — это инструмент, а не волшебная палочка.", reply_markup=start_test_menu())
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
            await message.answer(f"Какая стоимость {goal_genitive[text]}?", reply_markup=option_keyboard(cost_options[text]))
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
            goal = user_data[user_id]["goal"]
            cost = user_data[user_id]["cost"]
            total = 0
            month = 0
            monthly_rate = 0.09
            monthly_totals = []

            while total < cost:
                month += 1
                total = (total + monthly)*(1+monthly_rate)
                monthly_totals.append(total)

            msg = "📈 Накопления по месяцам с учетом ежемесячного сложного процента 9% в среднем:\n\n"
            for i,val in enumerate(monthly_totals,start=1):
                if i<=3 or i>len(monthly_totals)-3:
                    msg+=f"Месяц {i}: {int(val):,} ₽\n"
                elif i==4:
                    msg+="...\n"

            msg+=f"\nС вашей ежемесячной инвестицией {monthly:,} ₽ вы сможете {goal_phrase[goal]} {cost:,} ₽ примерно через {month} месяцев.\n"
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
            month = 0
            capital = 0
            monthly_rate = 0.09
            monthly_totals = []

            while True:
                month += 1
                capital = (capital + monthly)*(1+monthly_rate)
                passive = capital*monthly_rate
                monthly_totals.append(passive)
                if passive >= target_income:
                    break

            msg = "📈 Пассивный доход по месяцам:\n\n"
            for i,pas in enumerate(monthly_totals,start=1):
                if i<=3 or i>len(monthly_totals)-3:
                    msg+=f"Месяц {i}: {int(pas):,} ₽\n"
                elif i==4:
                    msg+="...\n"

            msg+=f"\nПри вашей ежемесячной инвестиции {monthly:,} ₽ вы сможете {goal_phrase['Пассивный доход']} {target_income:,} ₽/мес примерно через {month} месяцев.\n"
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
            user_progress[user_id]+=1
            if user_progress[user_id]<len(test_questions):
                await send_test_question(message,user_progress[user_id])
            else:
                await message.answer("✅ Тест пройден! Вы поняли, что использование рычагов, таких как ИИ, "
                                     "помогает быстрее достигать целей.", reply_markup=main_menu())
                user_progress.pop(user_id)
        else:
            await message.answer("❌ Неверно. Попробуйте ещё раз.")
        return

    # Если ничего не подошло
    await message.answer("Я вас не понял. Используйте меню 👇", reply_markup=main_menu())


from aiogram import F

# --- Ловим ответы помощников в группе ---
@dp.message(F.chat.id == -1003081706651)
async def helper_reply_handler(message: types.Message):
    if (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.is_bot
    ):
        # Получаем данные инвестора из словаря
        investor = invest_requests.get(message.reply_to_message.message_id)

        if investor:
            user_id = investor["user_id"]

            # Отправляем пользователю уведомление + текст помощника
            await bot.send_message(
                chat_id=user_id,
                text="✅ Ваш личный помощник ответил вам:\n\n" + (message.text or "")
            )

            # Уведомляем группу
            await message.reply("📨 Сообщение пользователю доставлено")

import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Ловим нажатия inline кнопок в группе ---
@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    data = callback.data
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    user = callback.from_user

    # --- Кнопка "В меню" ---
    if data == "back_to_menu":
        await callback.message.answer("Сделай свой выбор", reply_markup=main_menu())
        await callback.answer()
        return

    # --- Подтверждение вложения ---
    if data and data.startswith("confirm_invest_"):
        if chat_id != -1003081706651:  # только группа помощников
            return
        try:
            msg_id = int(data.split("_")[2])
        except (IndexError, ValueError):
            await callback.answer("Ошибка данных кнопки", show_alert=True)
            return

        confirmer_name = user.full_name
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Обновляем текст сообщения
        new_text = callback.message.text + f"\n\n💵 Вложение подтверждено {now} пользователем {confirmer_name} ✅"
        await callback.message.edit_text(new_text, reply_markup=None)

        # Попытка закрепления сообщения
        try:
            await bot.pin_chat_message(chat_id=chat_id, message_id=message_id, disable_notification=True)
        except Exception as e:
            print("Ошибка закрепления:", e)

        await callback.answer("Вложение подтверждено и сообщение закреплено ✅")
        return

    # --- Подтвердить заявку (кнопка "✅ Подтвердить заявку") ---
    if data and data.startswith("confirm_"):
        if chat_id != -1003081706651:
            return
        try:
            msg_id = int(data.split("_")[1])
        except (IndexError, ValueError):
            await callback.answer("Ошибка данных кнопки", show_alert=True)
            return

        investor = invest_requests.get(msg_id)
        if not investor:
            await callback.answer("⚠️ Заявка уже обработана или не найдена", show_alert=True)
            return

        user_id = investor["user_id"]
        investor_name = investor["full_name"]
        investor_username = investor.get("username")
        investor_text = investor.get("text", "")

        helper_name = user.full_name
        helper_id = user.id
        helper_username = user.username
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # --- Сообщение инвестору ---
        keyboard_user = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=f"✉️ Написать помощнику {helper_name}",
                url=f"https://t.me/{helper_username}" if helper_username else f"tg://user?id={helper_id}"
            )
        ]])
        await bot.send_message(
            chat_id=user_id,
            text=(
                f"✅ Ваш личный помощник {helper_name} подтвердил заявку!\n"
                f"⏰ Время подтверждения: {now}\n\n"
                "Вы можете написать ему напрямую:"
            ),
            reply_markup=keyboard_user
        )

        # --- Сообщение в группе ---
        new_text_group = (
            f"✅ Заявка подтверждена!\n\n"
            f"📌 Инвестор:\n"
            f"🆔 Telegram ID: {user_id}\n"
            f"👤 Имя: {investor_name}\n"
            f"💬 Username: @{investor_username if investor_username else 'нет'}\n"
            f"💬 Сообщение инвестора:\n{investor_text}\n\n"
            f"📌 Помощник:\n"
            f"👤 Имя: {helper_name}\n"
            f"🆔 Telegram ID: {helper_id}\n"
            f"💬 Username: @{helper_username if helper_username else 'нет'}\n\n"
            f"⏰ Время подтверждения: {now}"
        )

        keyboard_group = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"✉️ Написать инвестору {investor_name}",
                    url=f"https://t.me/{investor_username}" if investor_username else f"tg://user?id={user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💵 Подтвердить вложение",
                    callback_data=f"confirm_invest_{msg_id}"
                )
            ]
        ])

        await callback.message.edit_text(new_text_group, reply_markup=keyboard_group)

        # Сохраняем group_msg_id для дальнейших действий
        invest_requests[msg_id]["group_msg_id"] = callback.message.message_id

        await callback.answer("Заявка подтверждена ✅")
        return

async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
