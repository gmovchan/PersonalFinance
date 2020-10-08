from passwords import moneyBucketsToken
import logging
from telegram.ext import (CommandHandler, MessageHandler, Filters, Updater, ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from passwords import moneyBucketsToken
from main import personalFinance

finance = personalFinance()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

updater = Updater(token=moneyBucketsToken, use_context=True)
dispatcher = updater.dispatcher

'''keyboard = ReplyKeyboardMarkup([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["0", ",", "Send"]], resize_keyboard=False,
                               one_time_keyboard=False)

def showKeyboard(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Some text here", reply_markup=keyboard)

keyboard_handler = CommandHandler("keyboard", showKeyboard)

dispatcher.add_handler(keyboard_handler)'''

pockets = {"wallet": 0, "drawer": 0, "bank": 0}

WALLET, DRAWER, BANK, SUM = range(4)

def show(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML, text=finance.getTable())

def add(update, context):
    #reply_keyboard = ["Yes", "No"]
    update.message.reply_text("How much money in your wallet? Type below.")

    return WALLET


def wallet(update, context):
    pockets["wallet"] = update.message.text
    print(pockets)
    # reply_keyboard = ["Yes", "No"]
    update.message.reply_text("How much money in your drawer? Type below.")

    return DRAWER

def drawer(update, context):
    pockets["drawer"] = update.message.text
    print(pockets)
    # reply_keyboard = ["Yes", "No"]
    update.message.reply_text("How much money in your bank account? Type below.")

    return BANK

def bank(update, context):
    pockets["bank"] = update.message.text
    print(pockets)
    # reply_keyboard = ["Yes", "No"]
    update.message.reply_text("print to /sum to see how much money you have.")

    return ConversationHandler.END

def sum(update, context):
    print(pockets)
    # reply_keyboard = ["Yes", "No"]
    #update.message.reply_text("You have {} in the wallet, {} in the drawer and {} in the bank account.".format(
    #    pockets["wallet"], pockets["drawer"], pockets["bank"]))

    context.bot.send_message(chat_id=update.effective_chat.id, text="You have {} in the wallet, {} in the drawer and {} \
    in the bank account.".format(pockets["wallet"], pockets["drawer"], pockets["bank"]))

    #return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("You have decided not to add a new entry.")

    return ConversationHandler.END

show_handler = CommandHandler("show", show)
sum_handler = CommandHandler("sum", sum)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add)],

    states = {
        WALLET: [MessageHandler(Filters.text, wallet)],

        DRAWER: [MessageHandler(Filters.text, drawer)],

        BANK: [MessageHandler(Filters.text, bank)],

        SUM: [MessageHandler(Filters.text, sum)]
    },

    fallbacks=[CommandHandler("cancel", cancel)]
)

dispatcher.add_handler(show_handler)
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(sum_handler)

updater.start_polling()