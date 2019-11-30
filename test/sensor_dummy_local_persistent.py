import sys
import os
import time
from datetime import datetime
import requests
import random

PROJECT = 'swarm'
DESCRIPTION = '''SWARM is a prototype project that aims to combine sensory data obtained from a swarm of IOT devices by utilizing client-server architecture and the cloud. These IOT devices collect sensory data like temperature, time, windspeed, humidity, and luminosity and transmit the data to a full-stack application which stores, analyzes and displays this data. The full stack application will be composed of a consumable API, a storage database, and publicly accessible website that provides visualizations'''

ID_FILE = os.path.expanduser('~/dummy_id_file')
PROJECT_ID_FILE = os.path.expanduser('~/dummy_project_file')
if os.path.isfile(ID_FILE):
    with open(ID_FILE) as r:
        id = r.read()
else:
    r = requests.post(
        'http://localhost:6969/api/v0/device',
        json={
            'name': 'Raspberry Pi-J' + str(datetime.now()),
            'meta_data': {
                'project': 'swarm',
                'type': 'random'
            }
        }
    )
    with open(ID_FILE, 'w') as w:
        var = r.json()
        id = var['data']['_id']
        w.write(id)


project_id = None
if os.path.isfile(PROJECT_ID_FILE):
    with open(PROJECT_ID_FILE) as r:
        project_idid = r.read()
else:
    r = requests.get('http://localhost:6969/api/v0/project')
    body = r.json() if r.status_code == 200 else []
    for project in body['data']:
        if 'name' in project and project['name'].lower() == PROJECT:
            project_id = project['_id']

    if project_id is None:
        r = requests.post(
            'http://localhost:6969/api/v0/project',
            json={
                "name": PROJECT,
                "description": DESCRIPTION,
                "img": "<string>"
            }
        )
        var = r.json()
        project_id = var['data']['_id']

    with open(PROJECT_ID_FILE, 'w') as w:
        w.write(project_id)


print('device_id: <{}>; project_id: <{}>'.format(id, project_id))


period = 1
if len(sys.argv) > 1:
    period = int(sys.argv[1])


while True:

    raw = {
        'Temperature': random.randint(0, 69696969),
        'Humidity': random.randint(0, 69696969),
        'Lux': random.randint(0, 69696969),
        'Date': str(datetime.now()),
    }

    post_body = {'raw': raw, 'device': id, 'project': project_id}
    r = requests.post('http://localhost:6969/api/v0/raw_data', json=post_body)
    print(
        'device_id: <{}>; project_id: <{}>; period: <{}s>; (r.status_code == 200) -- {};'.format(
            id, project_id, period, r.status_code == 200
        )
    )
    time.sleep(period)
