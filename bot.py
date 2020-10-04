import telegram
#from main import personalFinance
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from passwords import moneyBucketsToken

updater = Updater(token=MessageHandler, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
    text_caps = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

start_handler = CommandHandler("start", start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
caps_handler = CommandHandler("caps", caps)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)

updater.start_polling()

'''bot = telegram.Bot(token="1296037754:AAFnsmrAHX2ejtvUbl2iaE_PLYQCAGQCWgQ")
print(bot.get_me())'''

'''finance = personalFinance()
finance.start()'''