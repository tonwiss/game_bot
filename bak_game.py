import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from constants import BAK
from start import start
from bd import update_bak

async def bak_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['quant_moves'] = 0
    context.user_data['record'] = 0
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Давай поиграем в быки и коровы!",
    )
    lst = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    while lst[0] == "0":
        random.shuffle(lst)
    context.user_data["comp_move"] = "".join(lst[:4])
    print(context.user_data['comp_move'])
    return BAK


async def bak_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    record = context.user_data['record']
    quant_moves = context.user_data['quant_moves']
    comp_move = context.user_data["comp_move"]
    human_move = str(update.effective_message.text)
    if human_move != comp_move:
        while human_move != comp_move:
            right_els = []
            cows = 0
            bools = 0
            count = 0
            for el in human_move:
                if el in comp_move:
                    right_els.append(el)
                    count += comp_move.count(el)
            for i in range(count):
                if human_move.index(right_els[i]) == comp_move.index(right_els[i]):
                    bools += 1
                else:
                    cows += 1
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"Коровы: {cows}, быки: {bools}"
            )
            quant_moves += 1
            human_move = str(update.effective_message.text)
            break
    else:
        keyboard = [['Играть снова'], ['Меню']]
        markup = ReplyKeyboardMarkup(
            keyboard,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Победа!!!! Конец",
            reply_markup=markup,
        )
        record = quant_moves
        await update_bak(update.effective_user.id, record)


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == 'Меню':
        return await start(update, context)
    elif update.effective_message.text == 'Играть снова':
        return await bak_start(update, context)