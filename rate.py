from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from constants import RATE
from bd import get_rate_cnb, get_rate_bak, get_rate_cao
from start import start


async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Стата К-Н-Б", callback_data="knb_stat")],
        [InlineKeyboardButton("Стата Б-И-К", callback_data="bak_stat")],
        [InlineKeyboardButton("Стата К-И-Н", callback_data="cao_stat")],
        [InlineKeyboardButton("Меню", callback_data="menu")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Посмотрите статистику по...",
        reply_markup=markup,
    )
    return RATE


async def rate_proc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "rate":
        keyboard = [
            [InlineKeyboardButton("Стата К-Н-Б", callback_data="knb_stat")],
            [InlineKeyboardButton("Стата  Б-И-К", callback_data="bak_stat")],
            [InlineKeyboardButton("Стата К-И-Н", callback_data="cao_stat")],
            [InlineKeyboardButton("Меню", callback_data="menu")],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Посмотрите статистику по...", reply_markup=markup
        )
    elif query.data == "knb_stat":
        users_lst = await get_rate_cnb()
        text = "Стата К-Н-Б\n"

        for n, user in enumerate(users_lst):
            text += f"{n + 1}. {user[1]} — {user[0]}%\n"
        keyboard = [
            [InlineKeyboardButton("Вернуться к статистике", callback_data="rate")],
            [InlineKeyboardButton("Стата  Б-И-К", callback_data="bak_stat")],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=markup)

    elif query.data == "bak_stat":
        users_lst = await get_rate_bak()
        text_1 = "Стата Б-И-К\n"
        text_2 = ""
        text_3 = ""
        f = False

        for n, user in enumerate(users_lst[:3]):
            text_2 += f"{user[0]}, {user[1]}\n"
            if user[2] == update.effective_user.id:
                f = True
        user_own_record = ""
        if f is False:
            for n, user in enumerate(users_lst):
                if user[2] == update.effective_user.id:
                    user_own_record = user[1]
                    break
            text_3 = f"Ваш рекорд: {user_own_record}"

        keyboard = [
            [InlineKeyboardButton("Вернуться к статистике", callback_data="rate")],
            [InlineKeyboardButton("Стата Б-И-К", callback_data="bak_stat")],
        ]
        text = text_1 + text_2 + text_3
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=markup)

    elif query.data == "cao_stat":
        text_1 = "Стата К-И-Н\n"
        text_2 = await get_rate_cao(update.effective_user.id)
        keyboard = [
            [InlineKeyboardButton("Вернуться к статистике", callback_data="rate")],
            [InlineKeyboardButton("Стата К-И-Н", callback_data="cao_stat")],
        ]
        text = text_1 + text_2
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=markup)
    elif query.data == 'menu':
        return await start(update, context)