import requests
import json
import matplotlib.pyplot as plt
from dateutil import parser
server_uri = 'http://onem2m.iiit.ac.in:40443/~/in-cse/in-name/'
headers = {
    'X-M2M-Origin': 'guest:guest',
    'Content-type': 'application/json'
}
