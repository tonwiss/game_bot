from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from telegram.constants import ParseMode
from constants import CAO
from start import start
from bd import update_cao


async def cao_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Давай поиграем в крестики-нолики!",
    )
    cao_field = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    context.user_data["queue"] = 1
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"`{'-' * 13}\n| {cao_field[0]} | {cao_field[1]} | {cao_field[2]} |\n{'-' * 13}\n| {cao_field[3]} | {cao_field[4]} | {cao_field[5]} |\n{'-' * 13}\n| {cao_field[6]} | {cao_field[7]} | {cao_field[8]} |\n{'-' * 13}`",
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    keyboard = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите следующее действие",
        reply_markup=markup,
    )
    context.user_data["cao_field"] = cao_field
    context.user_data["result"] = ""
    return CAO


async def cao_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cao_field = context.user_data["cao_field"]
    result = context.user_data["result"]
    queue = context.user_data["queue"]

    if queue % 2 != 0:
        hernya = "X"
    else:
        hernya = "O"

    move = int(update.effective_message.text)
    cao_field[move - 1] = hernya

    if (
        (cao_field[0] == cao_field[1] == cao_field[2])
        or (cao_field[3] == cao_field[4] == cao_field[5])
        or (cao_field[6] == cao_field[7] == cao_field[8])
        or (cao_field[0] == cao_field[3] == cao_field[6])
        or (cao_field[1] == cao_field[4] == cao_field[7])
        or (cao_field[2] == cao_field[5] == cao_field[8])
        or (cao_field[0] == cao_field[4] == cao_field[8])
        or (cao_field[2] == cao_field[4] == cao_field[6])
    ):
        keyboard = [["Играть снова"], ["Меню"]]
        markup = ReplyKeyboardMarkup(keyboard)
        if hernya == "X":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Победа крестиков!!!!",
                reply_markup=markup,
            )
            result = "cao_cross"
            await update_cao(update.effective_user.id, result)
            return CAO
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Победа ноликов!!!!",
                reply_markup=markup,
            )
            result = "cao_null"
            await update_cao(update.effective_user.id, result)
            return CAO
    elif queue == 9:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ничья",
            reply_markup=markup,
        )
        result = "draw"
        await update_cao(update.effective_user.id, result)
        return CAO

    keyboard = []
    num = 0
    for i in range(3):
        line = []
        for j in range(3):
            line.append(str(cao_field[num]))
            num += 1
        keyboard.append(line)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"`{'-' * 13}\n| {cao_field[0]} | {cao_field[1]} | {cao_field[2]} |\n{'-' * 13}\n| {cao_field[3]} | {cao_field[4]} | {cao_field[5]} |\n{'-' * 13}\n| {cao_field[6]} | {cao_field[7]} | {cao_field[8]} |\n{'-' * 13}`",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    markup = ReplyKeyboardMarkup(
        keyboard,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите следующее действие",
        reply_markup=markup,
    )
    queue += 1
    context.user_data["queue"] = queue


async def check_cao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == "Меню":
        return await start(update, context)
    elif update.effective_message.text == "Играть снова":
        return await cao_start(update, context)