import requests
import json
import os
import matplotlib.pyplot as plt
from dateutil import parser
from dotenv import load_dotenv, set_key, find_dotenv

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

user_email = os.getenv('USER_EMAIL')
user_password = os.getenv('USER_PASSWORD')


def update_environment(api_key):
    os.environ["API_KEY"] = api_key
    set_key(dotenv_file, "API_KEY", os.environ["API_KEY"])
