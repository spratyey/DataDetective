import requests
import json
import os
import matplotlib.pyplot as plt
from dateutil import parser
from dotenv import load_dotenv
load_dotenv()

server_uri = 'http://onem2m.iiit.ac.in:443/~/in-cse/in-name/'
headers = {
    'X-M2M-Origin': 'guest:guest',
    'Content-type': 'application/json'
}
user_email = os.getenv('USER_EMAIL')
user_password = os.getenv('USER_PASSWORD')

api_key=''

def update_environment(api_key):
    with open('.env', 'w') as f:
        f.write(f"USER_EMAIL={user_email}\nUSER_PASSWORD={user_password}\nAPI_KEY={api_key}")
    load_dotenv()
