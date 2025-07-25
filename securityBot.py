import logging
import os
from warnings import filters
import psutil
import platform
import socket
from telegram import ReplyKeyboardMarkup

from datetime import datetime
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import schedule
from telegram.ext import MessageHandler, filters
import threading
import time
from dotenv import load_dotenv

from alert import alert 
from config import ALLOWED_USERS, PENDING_USERS
from network import analyze_network
from security import perform_security_checks


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# Logging
logging.basicConfig(filename="security_logs.txt", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ALLOWED_USERS.add(ADMIN_CHAT_ID)

keyboard = ReplyKeyboardMarkup(
    [
        ["/status", "/alert"],
        ["/analyze_network", "/whoami"],
        ["/security", "/allow"],
        ["/start"]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


# 🟢 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    if user_id not in ALLOWED_USERS:
        if user_id not in PENDING_USERS:
            PENDING_USERS.add(user_id)
            # Notify admin
            bot = Bot(TOKEN)
            await context.bot.send_message(
    chat_id=ADMIN_CHAT_ID,
    text=f"🔐 Access Request from {user_name} (ID: {user_id})\nReply with /allow {user_id} to grant access."
    
)


        await update.message.reply_text("⏳ Access pending. Please wait for admin approval.")
        return

    welcome_message = (
        "🔐 Advanced Security Bot is Active and Monitoring.\n"
        "• /status — system status\n"
        "• /alert — system alert\n"
        "• /analyze_network — network issues\n"
        "• /whoami — who you are\n"
        "• /security — perform security checks\n"
        "• /allow <user_id> — approve new users\n"
        "• /start — show this message again" 
    )
    await update.message.reply_text(welcome_message, reply_markup=keyboard)
async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👤 Your user ID is: {update.effective_user.id}")

# 🔵 /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("🚫 Unauthorized.")
        return

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    system_info = platform.uname()

    msg = f"""🖥️ **System Status**
📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🧠 CPU Usage: {cpu}%
📦 RAM Usage: {memory}%
💾 Disk Usage: {disk}%
🔁 Boot Time: {boot_time}
📡 Hostname: {hostname}
🌐 IP: {ip_address}
💻 OS: {system_info.system} {system_info.release} ({system_info.machine})
"""
    await update.message.reply_text(msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⏳ Access pending. Please wait for admin approval or send /start to request access.")
    else:
        await update.message.reply_text("🤖 I'm a system monitor bot. Use /status or /alert.")

# 🛡️ Scheduled check for risk/failure
def security_check():
    try:
        alerts = []

        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        if cpu > 85:
            alerts.append(f"⚠️ High CPU Usage: {cpu}%")
        if memory > 90:
            alerts.append(f"⚠️ High Memory Usage: {memory}%")
        if disk > 90:
            alerts.append(f"⚠️ Disk Almost Full: {disk}%")

        # Check uptime and restart risk
        uptime_seconds = time.time() - psutil.boot_time()
        if uptime_seconds < 300:
            alerts.append("⚠️ System Just Restarted (Uptime < 5 min)")

        # Future: Add process watcher, log file tampering, network scan detection...

        if alerts:
            alert_message = "🚨 System Risk Detected:\n" + "\n".join(alerts)
            send_telegram_alert(alert_message)
            logging.warning(alert_message)
    except Exception as e:
        error = f"❌ Error during security check: {e}"
        logging.error(error)
        send_telegram_alert(error)

async def allow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_CHAT_ID):
        await update.message.reply_text("🚫 Only the admin can approve users.")
        return

    try:
        user_id = int(context.args[0])
        ALLOWED_USERS.add(user_id)
        PENDING_USERS.discard(user_id)
        await update.message.reply_text(f"✅ User {user_id} has been approved.")
        # Notify the user
        bot = Bot(TOKEN)
        bot.send_message(chat_id=user_id, text="✅ You have been approved. You may now use the bot.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def security_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⏳ Access pending. Please wait for admin approval.")
        return

    try:
        report = perform_security_checks()

        # Telegram message limit
        max_length = 4000

        # Split and send in chunks
        for i in range(0, len(report), max_length):
            await update.message.reply_text(report[i:i + max_length])

    except Exception as e:
        await update.message.reply_text(f"❌ Security check failed: {e}")

# 🚨 Telegram Alert Sender
def send_telegram_alert(message):
    bot = Bot(TOKEN)
    bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

# ⏱️ Background job runner
def run_schedule():
    schedule.every(15).seconds.do(security_check)
    while True:
        schedule.run_pending()
        time.sleep(1)

# 🔁 Main app loop
def main():
    threading.Thread(target=run_schedule, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("allow", allow))
    app.add_handler(CommandHandler("whoami", whoami))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("analyze_network", analyze_network))
    app.add_handler(CommandHandler("security", security_command))

    print("🔐 Security Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
