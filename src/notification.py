from getpass import getpass
import re
import ssl
import smtplib
import yagmail
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
files_to_send=[]
recipients=set()

def daily_summary(dirpath):
    markdown_text = "*Daily Update*\n"
    email_text ="Daily Update\n\n"
    files_in_dir = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    for file in files_in_dir:
        if file == 'freq_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'],dict_val['max_gap']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            # print(sorted_data)
            markdown_text += "\n*The most irregularly posting sensors today:*\n"
            email_text += "The most irregularly posting sensors today:\n"
            n = min(5,len(sorted_data))
            for i in range(n):
                markdown_text += "\- "+sorted_data[i][0].replace('-','\-')+"\n"
                email_text += sorted_data[i][0]+"\n"

        if file == 'nans_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'],dict_val['nan_percent'], dict_val['nan_params']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            # print(sorted_data)
            markdown_text += "\n*Sensors with the most number of nan values today:*\n"
            email_text += "\nSensors with the most number of nan values today:\n"
            n = min(5,len(sorted_data))
            for i in range(n):
                markdown_text += "\- *"+sorted_data[i][0].replace('-','\-')+"*, ``` \("
                email_text += sorted_data[i][0]+"    ("
                for param in sorted_data[i][2]:
                    markdown_text += param+", "
                    email_text += param+", "
                markdown_text=markdown_text[:-2]
                email_text=email_text[:-2]
                markdown_text += ")```\n"
                email_text += ")\n"

        if file == 'outlier_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'],dict_val['num_anomalies']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            # print(sorted_data)
            markdown_text += "\n*Sensors with the most outliers detected today:*\n"
            email_text += "\nSensors with the most outliers detected today:\n"
            n = min(5,len(sorted_data))
            for i in range(n):
                markdown_text += "\- "+sorted_data[i][0].replace('-','\-')+"\n"
                email_text += sorted_data[i][0]+"\n"
        
        if file == 'dead_nodes.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)

            with open('./verticalconfig.json', 'r') as f:
                vertical_config = json.load(f)

            markdown_text += "\n*Dead nodes today* \(Check dead\_nodes\.json for exact node IDs\):\n"
            email_text += "\nDead nodes today (Check dead_nodes.json for exact node IDs):\n"
            for vertical in vertical_config['verticals']:
                deadnodes = []
                for item in json_data:
                    if item['Node'] in vertical['sensor_nodes']:
                        deadnodes.append(item['Node'])
                markdown_text += "\- "+vertical['vertical_id'].replace('-', '\-')+" : "+str(
                    len(deadnodes))+" out of "+str(len(vertical['sensor_nodes']))+" dead"+"\n"
                email_text += vertical['vertical_id']+" : "+str(
                    len(deadnodes))+" out of "+str(len(vertical['sensor_nodes']))+" dead\n "
                # for node in deadnodes:
                #    email_text += node+", "
                # email_text = email_text[:-2]+")\n"


            
            #sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            
        
    print("(1/3)Posting summary to telegram")
    notify('registered_users.json',markdown_text)
    for file in files_in_dir:
        if file == 'freq_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'],dict_val['max_gap']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            send_plot(sorted_data[0][0],file.split('_')[0],'registered_users.json')

        if file == 'nans_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'],dict_val['nan_percent']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            send_plot(sorted_data[0][0],file.split('_')[0],'registered_users.json')

        if file == 'outlier_metadata.json':
            with open(dirpath+'/'+file, 'r') as f:
                json_data = json.load(f)
            data = []
            for dict_val in json_data:
                data.append([dict_val['node'],dict_val['num_anomalies']])
            sorted_data = sorted(data, key=lambda x: -abs(x[1]))
            send_plot(sorted_data[0][0],file.split('_')[0],'registered_users.json')
    shutil.make_archive('summary', 'zip', './output')
    print("(2/3)Sending zip file to telegram")
    send_doc('registered_users.json')
    print("(3/3)Composing email. This may take a while...")
    send_email(email_text)
    print("All Done.")

def send_doc(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    dirpath = './output'
    fname = []
    for chat_id in data['registered_chat_ids']:
        try:
            files_to_send.append('summary.zip')
            files_to_send.append('./output/metadata/dead_nodes.json')
            updater.bot.send_document(chat_id=chat_id, document=open('summary.zip', 'rb'),caption = "Daily Summary")
            updater.bot.send_document(chat_id=chat_id, document=open('./output/metadata/dead_nodes.json', 'r'),caption = "Daily Summary")
        except:
            print("Error sending document to chat_id: "+str(chat_id))
            
            
def send_plot(sensor_name,plot_type,json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    dirpath = './output'
    fname = []
    for root,d_names,f_names in os.walk(dirpath):
        for f in f_names:
            fname.append(os.path.join(root, f))
    for file in fname:
        if (sensor_name in file) and (plot_type in file):
            for chat_id in data['registered_chat_ids']:
                try:
                    files_to_send.append(file)
                    updater.bot.send_photo(chat_id=chat_id, photo=open(file, 'rb'),caption = sensor_name+":"+"\n"+""+plot_type+" plot")
                except:
                    print("Error sending document to chat_id: "+str(chat_id))
            


def notify(json_file,markdown_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    for chat_id in data['registered_chat_ids']:
        try:
            updater.bot.send_message(chat_id=chat_id, text=markdown_file, parse_mode=ParseMode.MARKDOWN_V2)
        except:
            print("Error sending document to chat_id: "+str(chat_id))

def send_email(email_text):
    pswd=getpass()
    yag = yagmail.SMTP('spratyey@gmail.com',pswd)
    contents = [
        email_text
    ]
    contents.extend(files_to_send)
    configure_recipients(email_text)
    unique_recipients=list(recipients)
    yag.send(unique_recipients, 'Daily Update', contents)

def configure_recipients(email_text):
    with open('verticalconfig.json') as json_file:
        # load config file data
        config_file_data = json.load(json_file)
        # for each vertical in the config file, ...
        for vertical in config_file_data['verticals']:
            if email_text.find(vertical['vertical_id'])!=-1:
                # ... add the vertical's email to the list of recipients
                for incharge in vertical['incharge']:
                    recipients.add(incharge)
