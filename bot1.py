import logging
import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
)
from cao_game import cao_game, cao_start, check_cao
from rate import rate, rate_proc
from bd import create_table
from bak_game import bak_game, bak_start, check_bak
from cnb_game import cnb_game, cnb_start, check_cnb
from start import start
from constants import MAINMENU, CNB, BAK, CAO, RATE
import asyncio

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    persistence = PicklePersistence(filepath="game_bot")
    application = ApplicationBuilder().token(os.getenv("TOKEN")).persistence(persistence).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("cnb", cnb_start),
                CommandHandler("bak", bak_start),
                CommandHandler("cao", cao_start,),
                CommandHandler("rate", rate),
            ],
            CNB: [MessageHandler(filters.Regex('^(камень|ножницы|бумага)$'), cnb_game), MessageHandler(filters.Regex('^(Меню|Играть снова)$'), check_cnb)],
            BAK: [MessageHandler(filters.Regex('^(Меню|Играть снова)$'), check_bak), MessageHandler( filters.TEXT & ~filters.COMMAND, bak_game)],
            CAO: [MessageHandler(filters.Regex('^(Меню|Играть снова)$'), check_cao), MessageHandler(filters.TEXT & ~filters.COMMAND, cao_game)],
            RATE: [CallbackQueryHandler(rate_proc)],
        },
        fallbacks=[CommandHandler("start", start)],
        name='game_bot', persistent=True
    )
    application.add_handler(conv_handler)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_table())

    application.run_polling()