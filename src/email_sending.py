from getpass import getpass
import ssl
import smtplib
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import *
from telegram.ext import *
import shutil
import os
from os import listdir
from os.path import isfile, join
import json
from dotenv import load_dotenv
load_dotenv()
updater = Updater(os.getenv("BOT_TOKEN"),
                  use_context=True)


def daily_summary(dirpath):
    markdown_text = "*Daily Update*\n"
    email_text = "Subject: Daily Update\n\n"
    files_in_dir = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    for file in files_in_dir:
        if file == 'freq_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'], dict_val['max_gap']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            # print(sorted_data)
            markdown_text += "*The most irregularly posting sensors today:*\n"
            email_text += "The most irregularly posting sensors today:\n"
            n = min(5, len(sorted_data))
            for i in range(n):
                markdown_text += "\- " + \
                    sorted_data[i][0].replace('-', '\-')+"\n"
                email_text += sorted_data[i][0]+"\n"

        if file == 'nans_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'], dict_val['nan_percent']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            # print(sorted_data)
            markdown_text += "*Sensors with the most number of nan values today:*\n"
            email_text += "\nSensors with the most number of nan values today:\n"
            n = min(5, len(sorted_data))
            for i in range(n):
                markdown_text += "\- " + \
                    sorted_data[i][0].replace('-', '\-')+"\n"
                email_text += sorted_data[i][0]+"\n"

        if file == 'outlier_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'], dict_val['num_anomalies']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            # print(sorted_data)
            markdown_text += "*Sensors with the most outliers detected today:*\n"
            email_text += "\nSensors with the most outliers detected today:\n"
            n = min(5, len(sorted_data))
            for i in range(n):
                markdown_text += "\- " + \
                    sorted_data[i][0].replace('-', '\-')+"\n"
                email_text += sorted_data[i][0]+"\n"

    notify('registered_users.json', markdown_text)
    for file in files_in_dir:
        if file == 'freq_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'], dict_val['max_gap']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            send_plot(sorted_data[0][0], file.split(
                '_')[0], 'registered_users.json')

        if file == 'nans_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'], dict_val['nan_percent']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            send_plot(sorted_data[0][0], file.split(
                '_')[0], 'registered_users.json')

        if file == 'outlier_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'], dict_val['num_anomalies']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            send_plot(sorted_data[0][0], file.split(
                '_')[0], 'registered_users.json')
    shutil.make_archive('summary', 'zip', './output')
    # send_doc('registered_users.json')

    send_email(email_text)


def send_doc(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    dirpath = './output'
    fname = []
    for chat_id in data['registered_chat_ids']:
        try:
            updater.bot.send_document(chat_id=chat_id, document=open(
                'summary.zip', 'rb'), caption="Daily Summary")
        except:
            print("Error sending document to chat_id: "+str(chat_id))


def send_plot(sensor_name, plot_type, json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    dirpath = './output'
    fname = []
    for root, d_names, f_names in os.walk(dirpath):
        for f in f_names:
            fname.append(os.path.join(root, f))
    for file in fname:
        if (sensor_name in file) and (plot_type in file):
            for chat_id in data['registered_chat_ids']:
                try:
                    updater.bot.send_photo(chat_id=chat_id, photo=open(
                        file, 'rb'), caption=sensor_name+":"+"\n"+""+plot_type+" plot")
                except:
                    print("Error sending document to chat_id: "+str(chat_id))


def notify(json_file, markdown_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    for chat_id in data['registered_chat_ids']:
        try:
            updater.bot.send_message(
                chat_id=chat_id, text=markdown_file, parse_mode=ParseMode.MARKDOWN_V2)
        except:
            print("Error sending document to chat_id: "+str(chat_id))


def send_email(email_text):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "spratyey@gmail.com"  # Enter your address
    receiver_email = "spratyey@gmail.com"  # Enter receiver address
    password = getpass()

    message = email_text

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
