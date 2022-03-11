import requests
import json
import matplotlib.pyplot as plt
from dateutil import parser

server_uri = 'http://onem2m.iiit.ac.in:443/~/in-cse/in-name/'

uri_cnt = 'http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WE/WE-VN04-00/Data/la'
headers = {
    'X-M2M-Origin': 'guest:guest',
    'Content-type': 'application/json'
}
response = requests.get(uri_cnt, headers=headers)
jsondata = json.loads(response.text)
print(jsondata)
