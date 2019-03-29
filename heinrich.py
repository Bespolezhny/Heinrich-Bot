from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
from random import choice, randrange
import wikipedia
import datetime
from time import sleep
import pickle

updater = Updater(token=#token)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hallo! Ich bin Heinrich.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

def caps(bot, update, args):
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

def yes_or_no(bot, update):
	pool = ["Yes.", "No.", "Maybe."]
	answer = choice(pool)
	bot.send_message(chat_id=update.message.chat_id, text=answer)
ask_handler = CommandHandler("decide", yes_or_no)
dispatcher.add_handler(ask_handler)

def get_time(bot, update):
    foo = datetime.datetime.now()
    bar = str(foo).split(".")
    time = str(bar[0])
    bot.send_message(chat_id=update.message.chat_id, text=time)
get_time_handler = CommandHandler("time", get_time)
dispatcher.add_handler(get_time_handler)

def get_weather(bot, update, args):
    try:
        if len(args) == 2:
            foo = "{}+{}".format(args[0], args[1])
            loc = foo.lower()
        elif len(args) == 1:
            loc = args[0].lower()
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid="#apikey.format(loc), headers={"Accept": "application/json"})
        data = response.json()
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        city = data['name']
        weather_info = "It is {}°C in {} with {}".format(temp, city, description)
    except KeyError:
        weather_info = "Location not found!"
    sleep(3)
    bot.send_message(chat_id=update.message.chat_id, text=weather_info)
get_weather_handler = CommandHandler("weather", get_weather, pass_args=True)
dispatcher.add_handler(get_weather_handler)

def get_roll(bot, update, args):
    try:
        args = [int(arg) for arg in args]
        foo = randrange(args[0])
    except ValueError:
        foo = "Please provide a number."
    bot.send_message(chat_id=update.message.chat_id, text=foo)
get_roll_handler = CommandHandler("roll", get_roll, pass_args=True)
dispatcher.add_handler(get_roll_handler)

def get_pgp(bot, update, args):
	original = "users.pickle"
	if len(args) == 2:
		with open(original, "rb") as file:
			saved = pickle.load(file)
		with open(original,"wb") as file:
			saved.update({args[0]:args[1]})
			pickle.dump(saved, file)
			info = "Saved!"
	elif len(args) == 1:
		with open(original, "rb") as file:
			saved = pickle.load(file)
			info = saved[args[0]]
	else:
	    info = "Either submit a new user or access an existing one!"
	bot.send_message(chat_id=update.message.chat_id, text=info)
get_pgp_key = CommandHandler("pgp", get_pgp, pass_args=True)
dispatcher.add_handler(get_pgp_key)

def get_shout(bot, update, args):
    if len(args) > 1:
	    foo = ""
	    for item in args:
		    foo += str(item)
    else:
	    foo = args[0]
    space = "  "
    bar = foo.upper()
    from_next = bar[1:]
    descending = ""
    horizontal = ""
    count = 1
    for char in bar:
	    horizontal += char + space
    for char in from_next:
	    descending += "\n" + char + (space*count+char)
	    count += 2
    bot.send_message(chat_id=update.message.chat_id, text=horizontal+descending)
get_shout_handler = CommandHandler("shout", get_shout, pass_args=True)
dispatcher.add_handler(get_shout_handler)

def get_wiki(bot, update, args):
    if len(args) > 1:
	    foo = ""
	    for item in args:
		    foo += str(item)+ " "
    else:
	    foo = args[0]
    try:
        foo.lstrip()
        bar = wikipedia.summary(foo)
        bot.send_message(chat_id=update.message.chat_id, text=bar)
    except wikipedia.exceptions.DisambiguationError as e:
        msg = "Oops! Your search got a disambugation page, please search again from the results below:"
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        bot.send_message(chat_id=update.message.chat_id, text=e.options)
    except wikipedia.exceptions.PageError:
        err = "{} does not match any pages. Try another query!".format(foo)
        bot.send_message(chat_id=update.message.chat_id, text=err)

get_wiki_handler = CommandHandler("wiki", get_wiki, pass_args=True)
dispatcher.add_handler(get_wiki_handler)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Entschuldigung, Ich verstehe deine Frage nicht..")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.idle()
