from passwords import moneyBucketsToken
import logging
from telegram.ext import (CommandHandler, MessageHandler, Filters, Updater, ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from passwords import moneyBucketsToken

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

updater = Updater(token=moneyBucketsToken, use_context=True)
dispatcher = updater.dispatcher

keyboard = ReplyKeyboardMarkup([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["0", ",", "Send"]], resize_keyboard=False,
                               one_time_keyboard=False)

def showKeyboard(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Some text here", reply_markup=keyboard)

keyboard_handler = CommandHandler("keyboard", showKeyboard)

dispatcher.add_handler(keyboard_handler)

updater.start_polling()