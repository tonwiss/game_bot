from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes
)
from bd import create_user
from constants import MAINMENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_user(update.effective_user)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello, {update.effective_user.first_name}\n/cnb\n/bak\n/cao\n/rate",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MAINMENU