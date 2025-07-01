import logging
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tarot_cards import tarot_cards
from already_replied_messages import already_replied_messages
import os


# Load token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track daily usage per user
user_last_draw = {}  # {user_id: date}


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ကဲ ဘာသိချင်လဲ\n/MAYML ကိုနှိပ်လိုက်")


# Shared logic for drawing a tarot card
async def draw_tarot(update: Update, user_id: int):
    today = datetime.now().date()

    if user_id in user_last_draw and user_last_draw[user_id] == today:
        await update.message.reply_text(random.choice(already_replied_messages)
                                        )
        return

    card = random.choice(tarot_cards)
    message = f"{card['meaning']}"
    await asyncio.sleep(1)  # slight delay to prevent Telegram API overload
    await update.message.reply_text(message)

    user_last_draw[user_id] = today


# /MAYML command
async def MAYML(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await draw_tarot(update, user_id)


# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["MAYML", "mayml"], MAYML))

    print("Bot is running...")
    app.run_polling()
