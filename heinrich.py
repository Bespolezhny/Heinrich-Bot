from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
from random import choice

updater = Updater(token="613237750:AAHRyK7giT61cVUPXHYL9OUgTLw_e2-dWqE")
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hallo! Ich bin Heinrich.")

start_handler = CommandHandler('start', start) 
dispatcher.add_handler(start_handler)
updater.start_polling()

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text) 

echo_handler = MessageHandler(Filters.text, echo) 
dispatcher.add_handler(echo_handler)
     
def caps(bot, update, args):  
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=text_caps)	

caps_handler = CommandHandler('caps', caps, pass_args=True)	    
dispatcher.add_handler(caps_handler)

def yes_or_no(bot, update):
	pool = ["Yes.", "No.", "Maybe.", "I don't know.", "Can you repeat the question?"]
	answer = choice(pool)
	bot.send_message(chat_id=update.message.chat_id, text=answer)
ask_handler = CommandHandler("decideforme", yes_or_no)
dispatcher.add_handler(ask_handler)	

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Entschuldigung, Ich kann nicht verstehe deine Frag.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)    

updater.idle()