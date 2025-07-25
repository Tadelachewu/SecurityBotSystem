from telegram import Update
from telegram.ext import ContextTypes
from ai import analyze_logs_with_ai
from config import ALLOWED_USERS
from health_check import check_system_health_detailed
from log import read_log_tail

MAX_MESSAGE_LENGTH = 4096

async def send_long_message(context, chat_id, text):
    """Send a long message in chunks to avoid Telegram limit errors."""
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        await context.bot.send_message(chat_id=chat_id, text=text[i:i+MAX_MESSAGE_LENGTH])

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⏳ Access pending. Please wait for admin approval.")
        return

    try:
        status, alerts = check_system_health_detailed()
        logs = read_log_tail()
        log_analysis = analyze_logs_with_ai(logs)

        message = f"📊 System Report\n\n" + "\n".join(status)
        if alerts:
            message += "\n\n🚨 Alerts:\n" + "\n".join(alerts)
        else:
            message += "\n\n✅ No major issues found."

        message += "\n\n🧠 AI Log Analysis:\n" + log_analysis

        await send_long_message(context, update.effective_chat.id, message)

    except Exception as e:
        error_msg = f"❌ Failed to generate alert: {e}"
        await update.message.reply_text(error_msg)
        print(error_msg)
