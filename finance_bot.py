from passwords import moneyBucketsToken
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from passwords import moneyBucketsToken

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

updater = Updater(token=moneyBucketsToken, use_context=True)
dispatcher = updater.dispatcher

keyboard = ReplyKeyboardMarkup([["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["0", ",", ""]], resize_keyboard=False,
                               one_time_keyboard=False)

def showKeyboard(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Some text here", reply_markup=keyboard)

keyboard_handler = CommandHandler("keyboard", showKeyboard)

dispatcher.add_handler(keyboard_handler)

updater.start_polling()