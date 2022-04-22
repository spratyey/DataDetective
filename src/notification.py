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

def notify(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    for chat_id in data['registered_chat_ids']:
        updater.bot.send_message(chat_id=chat_id, text="Daily Update")

notify('registered_users.json')