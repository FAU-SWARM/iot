import json
import sys
import os
import time
from datetime import datetime
import Adafruit_DHT
import requests
import smbus
import random

ID_FILE = os.path.expanduser('~/dummy_id_file')
print(ID_FILE)
if os.path.isfile(ID_FILE):
    print('hi')
    with open(ID_FILE) as r:
        id = r.read()
else:
    print('hi2')
    r = requests.post('http://swarm-fau4214.eastus.cloudapp.azure.com:6969/api/v0/device', json =
    { 'name': 'Raspberry Pi-J' + str(datetime.now()),
    'meta_data': { 'type': 'random' }  
    })
    with open(ID_FILE, 'w') as w:
        print('hi3')
        print(vars(r))
        var = json.loads(r.text)
        id = var['data']['_id']
        w.write(id)


def get_time():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H:%M:%S")
    return month + '/' + day + '/' + year + ', ' + time

def post_request(sensor_reading, sensor_type, route):
    address = 'http://192.168.1.90' # home: 192.168.1.90, school: 10.13.147.179
    port = '5000'
    json_string = {sensor_type: sensor_reading, 'Time': get_time()}
    print(address + ':' + port + route)
    print(json_string)
#    response = requests.post(address + ':' + port + route, json_string)
#    if response.ok:
#            print(response.json())

while True:
    
    raw = { 'Temperature': random.randint(0,69),
            'Humidity': random.randint(0,69),
            'Lux': random.randint(0,69),
            'Date': get_time()
            }
            
    post_body = { 'raw': raw,
                'device': id }
    r = requests.post('http://swarm-fau4214.eastus.cloudapp.azure.com:6969/api/v0/raw_data', 
                        json = post_body)
    print(r.status_code == 200)
    time.sleep(1)
