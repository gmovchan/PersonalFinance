from passwords import moneyBucketsToken
import logging
from telegram.ext import (CommandHandler, MessageHandler, Filters, Updater, ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, Bot)
from passwords import moneyBucketsToken
from main import personalFinance
from main import engine
#from main import createNewEngine

#print(engine.execute("SELECT * FROM money").fetchall())

#finance = personalFinance(engine)

#engine = createNewEngine()

#print(engine.table_names())

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

pockets = {"wallet": 0, "drawer": 0, "bank": 0}

WALLET, DRAWER, BANK, SUM = range(4)

finance = False
chat_id = False

def createFinanceModel(id):
    global finance
    global chat_id
    chat_id = id
    if not finance:
        finance = personalFinance(engine, id)

def restartFinanceModel(id=chat_id):
    global finance
    finance = personalFinance(engine, id)

def checkInput(update):
    if not update.message.text.isdigit():
        update.message.reply_text("You can only send an integer in this case. Try again or send /cancel")
        return False
    return True

def start(update, context):
    #engine = createNewEngine()
    #global finance
    #print(engine.table_names())
    #createFinanceModel(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, {}!".format(update.effective_chat.first_name))

def show(update, context):
    global finance
    print("finance in show")
    print(finance)
    createFinanceModel(update.effective_chat.id)
    #print(finance.getTable())
    print(update.effective_chat)
    context.bot.send_message(chat_id=update.effective_chat.id, text=finance.getTable())

def add(update, context):
    print("add")
    createFinanceModel(update.effective_chat.id)
    print("finance in add")
    print(finance)
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

    return ConversationHandler.END

def pots(update, context):
    createFinanceModel(update.effective_chat.id)
    #print(pockets)
    # reply_keyboard = ["Yes", "No"]
    #update.message.reply_text("You have {} in the wallet, {} in the drawer and {} in the bank account.".format(
    #    pockets["wallet"], pockets["drawer"], pockets["bank"]))
    pockets = finance.getPockets()
    context.bot.send_message(chat_id=update.effective_chat.id, text="You have {} in the wallet, {} in the drawer and {} "
    "in the bank account.".format(pockets["wallet"], pockets["drawer"], pockets["bank"]))

    #return ConversationHandler.END

def sum(update, context):
    createFinanceModel(update.effective_chat.id)
    #print("chat_id: {}".format(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text=finance.compareMonths())

def cancel(update, context):
    print("try to cancel")
    #user = update.message.from_user
    update.message.reply_text("You have decided not to add a new entry.")

    return ConversationHandler.END

def fill(update, context):
    createFinanceModel(update.effective_chat.id)
    finance.fillDB(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="You have filled the database with fake data")

def sendMsg(msg, chat_if=chat_id, token=moneyBucketsToken):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=msg)

def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    print("Update {} caused error {}".format(update, context.error))
    restartFinanceModel()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Some error has happened and the bot has been restarted as a precaution. "
                                  "\nThe cause of the error: {}".format(context.error))

def main():

    updater = Updater(token=moneyBucketsToken, use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler("start", start)
    show_handler = CommandHandler("show", show)
    sum_handler = CommandHandler("sum", sum)
    pots_handler = CommandHandler("pots", pots)
    fill_handler = CommandHandler("fill", fill)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add)],

        states={
            WALLET: [MessageHandler(Filters.text & ~Filters.command, wallet)],

            DRAWER: [MessageHandler(Filters.text & ~Filters.command, drawer)],

            BANK: [MessageHandler(Filters.text & ~Filters.command, bank)],
        },

        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(start_handler)
    dp.add_handler(show_handler)
    dp.add_handler(conv_handler)
    dp.add_handler(pots_handler)
    dp.add_handler(sum_handler)
    dp.add_handler(fill_handler)
    dp.add_error_handler(error_callback)

    updater.start_polling()

main()