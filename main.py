import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models import ChatOllama

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

chat_model = ChatOllama(model="dolphin-phi")

messages = [
    SystemMessage(content="You are a bored AI called The Librarian, waiting from users to talk to you through Telegram")
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print (update.message.text)
    messages.append(HumanMessage(content=update.message.text))
    robot = chat_model.invoke(messages)
    messages.append(robot)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=robot.content)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

if __name__ == '__main__':
    application = ApplicationBuilder().token('////TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    caps_handler = CommandHandler('caps', caps)
    
    application.add_handlers([echo_handler, start_handler, caps_handler])
    
    application.run_polling()