import random
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from constants import CNB
from start import start
from bd import update_cnb


async def cnb_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["камень", "ножницы", "бумага"]]
    context.user_data['result'] = ''
    markup = ReplyKeyboardMarkup(
        keyboard,
        input_field_placeholder="Выберите кем будете ходить",
        one_time_keyboard=True,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Давай, сыграем в камень-ножницы-бумага \n Загадай свой предмет",
        reply_markup=markup,
    )
    return CNB


async def cnb_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Меню', 'Играть снова']]
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
    )
    result = context.user_data['result']
    human_move = update.effective_message.text
    comp_list = ["ножницы", "бумага", "камень"]
    comp_list_ind = random.randint(0, 2)
    comp_move = comp_list[comp_list_ind]
    dicti = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}
    if human_move == comp_move:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Ничья, т.к. ход компьютера был: {comp_move}",
            reply_markup=markup,
        )
        result = 'cnb_draws'
    elif dicti[human_move] == comp_move:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{human_move} побеждает {comp_move}, т.к. ход компьютера был: {comp_move}",
            reply_markup=markup,
        )
        result = 'cnb_wins'
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{comp_move} побеждает {human_move}, т.к. ход компьютера был: {comp_move}",
            reply_markup=markup,
        )
        result = 'cnb_losses'
    
    await update_cnb(update.effective_user.id, result)
    
    

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == 'Меню':
        return await start(update, context)
    elif update.effective_message.text == 'Играть снова':
        return await cnb_start(update, context)