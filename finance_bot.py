from passwords import moneyBucketsToken
import logging
from telegram.ext import (CommandHandler, MessageHandler, Filters, Updater, ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from passwords import moneyBucketsToken
from main import personalFinance
from main import engine
#from main import createNewEngine

#print(engine.execute("SELECT * FROM money").fetchall())

#finance = personalFinance(engine)

#engine = createNewEngine()

#print(engine.table_names())

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

updater = Updater(token=moneyBucketsToken, use_context=True)
dispatcher = updater.dispatcher

pockets = {"wallet": 0, "drawer": 0, "bank": 0}

WALLET, DRAWER, BANK, SUM = range(4)

def checkInput(update):
    if not update.message.text.isdigit():
        update.message.reply_text("You can only send an integer in this case. Try again or send /cancel")
        return False
    return True

def start(update, context):
    #engine = createNewEngine()
    global finance
    #print(engine.table_names())
    finance = personalFinance(engine, update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, {}!".format(update.effective_chat.first_name))

def show(update, context):
    #print(finance.getTable())
    print(update.effective_chat)
    context.bot.send_message(chat_id=update.effective_chat.id, text=finance.getTable())

def add(update, context):
    #reply_keyboard = ["Yes", "No"]
    update.message.reply_text("How much money in your wallet? Type below.")

    return WALLET


def wallet(update, context):
    if not checkInput(update):
        return WALLET

    pockets["wallet"] = update.message.text

    #print(pockets)
    # reply_keyboard = ["Yes", "No"]
    update.message.reply_text("How much money in your drawer? Type below.")

    return DRAWER

def drawer(update, context):
    if not checkInput(update):
        return DRAWER

    pockets["drawer"] = update.message.text
    #print(pockets)
    # reply_keyboard = ["Yes", "No"]
    update.message.reply_text("How much money in your bank account? Type below.")

    return BANK

def bank(update, context):
    if not checkInput(update):
        return BANK

    pockets["bank"] = update.message.text
    finance.addMoney(pockets)
    #print(pockets)
    # reply_keyboard = ["Yes", "No"]
    update.message.reply_text("type to /pots to see how much money you have.")

    #return ConversationHandler.END

def pots(update, context):
    #print(pockets)
    # reply_keyboard = ["Yes", "No"]
    #update.message.reply_text("You have {} in the wallet, {} in the drawer and {} in the bank account.".format(
    #    pockets["wallet"], pockets["drawer"], pockets["bank"]))
    pockets = finance.getPockets()
    context.bot.send_message(chat_id=update.effective_chat.id, text="You have {} in the wallet, {} in the drawer and {} "
    "in the bank account.".format(pockets["wallet"], pockets["drawer"], pockets["bank"]))

    #return ConversationHandler.END

def sum(update, context):
    #print("chat_id: {}".format(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text=finance.compareMonths())

def cancel(update, context):
    print("try to cancel")
    #user = update.message.from_user
    update.message.reply_text("You have decided not to add a new entry.")

    return ConversationHandler.END

start_handler = CommandHandler("start", start)
show_handler = CommandHandler("show", show)
sum_handler = CommandHandler("sum", sum)
pots_handler = CommandHandler("pots", pots)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add)],

    states = {
        WALLET: [MessageHandler(Filters.text & ~Filters.command, wallet)],

        DRAWER: [MessageHandler(Filters.text & ~Filters.command, drawer)],

        BANK: [MessageHandler(Filters.text & ~Filters.command, bank)],
    },

    fallbacks=[CommandHandler('cancel', cancel)],
)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(show_handler)
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(pots_handler)
dispatcher.add_handler(sum_handler)

updater.start_polling()