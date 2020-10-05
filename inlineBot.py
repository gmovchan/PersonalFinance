import telegram
from passwords import moneyBucketsToken
from telegram.ext import Updater
from telegram import InlineQueryResultArticle, InputTextMessageContent
#print(moneyBucketsToken)
updater = Updater(token=moneyBucketsToken, use_context=True)
dispatcher = updater.dispatcher
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)



updater.start_polling()