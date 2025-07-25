from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello, Tadele! I'm your bot.")

# Create scheduler with timezone
scheduler = AsyncIOScheduler(timezone=pytz.UTC)

app = (ApplicationBuilder()
       .token("7604878367:AAFmstkykaZ6McOyfnEwMkqr7gbc2_4S4V8")
       .build())

# Replace the default scheduler
app.job_queue._scheduler = scheduler
app.job_queue._scheduler.start()

app.add_handler(CommandHandler("start", start))

print("✅ Bot is running...")
app.run_polling()