from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import *
from telegram.ext import * 
import os
import json
from dotenv import load_dotenv
load_dotenv()
updater = Updater(os.getenv("BOT_TOKEN"),
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("/dailyupdate")], [KeyboardButton("/help")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(buttons))
  
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /register - register for daily and weekly summary and updates
    /dailyupdate - To get the daily update image""")
  
def register_user(update: Update, context: CallbackContext):
    # open json file
    with open('registered_users.json', 'r') as f:
        registered_users = json.load(f)
    # add user to json file
    registered_users['registered_chat_ids'].append(update.effective_chat.id)
    # save json file
    with open('registered_users.json', 'w') as f:
        json.dump(registered_users, f)
    update.message.reply_text("Registered Successfully!")

def daily_update(update: Update, context: CallbackContext):
    # update.message.reply_photo(open('./output/AQ/analytics/AQ-AN00-00_nan.png', 'rb'),"Nan dection plot")
    # update.message.reply_photo(open('./output/AQ/analytics/AQ-AN00-00_intervals.png', 'rb',"Interval plot"))
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('./output/AQ/analytics/AQ-AN00-00_nan.png', 'rb'))
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('./output/AQ/analytics/AQ-AN00-00_intervals.png', 'rb'))

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
  
  
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
  

updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('register', register_user))
updater.dispatcher.add_handler(CommandHandler('dailyupdate', daily_update))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
updater.start_polling()
