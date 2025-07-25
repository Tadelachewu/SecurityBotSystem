from telegram import Update
from telegram.ext import ContextTypes
from analyze_network_with_ai import analyze_network_with_ai
from config import ALLOWED_USERS
from network_analysis import collect_network_data

MAX_MESSAGE_LENGTH = 4000  # Keep a safe margin from Telegram's 4096 limit

async def analyze_network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⏳ Access pending. Please wait for admin approval.")
        return

    try:
        # Step 1: Collect network data
        network_data = collect_network_data()

        # Step 2: AI analyze
        ai_summary = analyze_network_with_ai(network_data)

        # Step 3: Send response in chunks
        if len(ai_summary) > MAX_MESSAGE_LENGTH:
            chunks = [ai_summary[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(ai_summary), MAX_MESSAGE_LENGTH)]
            await update.message.reply_text("📡 Network Report is long. Splitting into parts:")
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(f"📡 Network Report:\n\n{ai_summary}")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to analyze network: {e}")
