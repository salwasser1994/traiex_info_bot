import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Отправь мне любой файл, фото, видео или голосовое сообщение, "
        "и я пришлю тебе его file_id."
    )

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    msg = update.message

    # Определяем тип файла
    if msg.document:
        file = msg.document
    elif msg.photo:
        file = msg.photo[-1]  # Берём фото в наилучшем качестве
    elif msg.video:
        file = msg.video
    elif msg.audio:
        file = msg.audio
    elif msg.voice:
        file = msg.voice
    elif msg.video_note:
        file = msg.video_note
    elif msg.sticker:
        file = msg.sticker
    else:
        await msg.reply_text("❌ Не удалось определить тип файла.")
        return

    await msg.reply_text(f"✅ file_id:\n<code>{file.file_id}</code>", parse_mode="HTML")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(MessageHandler(filters.ALL, get_file_id))

    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
