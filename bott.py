import logging
import pytz
from datetime import time
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Bot Token
TOKEN = "7802310543:AAFjhbWoqM5XYT7JATn2RFFlEY3hvXQyQkE"  # Replace with your token

# Timezone
TZ = pytz.timezone("Africa/Addis_Ababa")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello, Tadele! I'm your bot.")

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Show this help")

# Echo handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

# Scheduled job
async def scheduled_job(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="⏰ This is your scheduled reminder!")

def main():
    # Build Application
    app = ApplicationBuilder().token(TOKEN).build()

    # Schedule a daily job at 9:00 AM Addis Ababa time
    app.job_queue.run_daily(
        scheduled_job,
        time=time(9, 0, tzinfo=TZ),
        chat_id=123456789  # 🔁 Replace with your actual chat ID
    )

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
