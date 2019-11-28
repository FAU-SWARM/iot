import sys
import os
import time
from datetime import datetime
import requests
import random

ID_FILE = os.path.expanduser('~/dummy_id_file')
# print(ID_FILE)
# if os.path.isfile(ID_FILE):
#     with open(ID_FILE) as r:
#         id = r.read()
# else:
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
r = requests.get('http://localhost:6969/api/v0/project')
body = r.json() if r.status_code == 200 else []
project_id = None
for project in body['data']:
    if 'name' in project and project['name'].lower() == 'swarm':
        project_id = project['_id']

print('device_id: <{}>; project_id: <{}>'.format(id, project_id))


def get_time():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H:%M:%S")
    return month + '/' + day + '/' + year + ', ' + time


period = 1
if len(sys.argv) > 1:
    period = int(sys.argv[1])


while True:

    raw = {
        'Temperature': random.randint(0, 69),
        'Humidity': random.randint(0, 69),
        'Lux': random.randint(0, 69),
        'Date': get_time()
    }

    post_body = {'raw': raw, 'device': id, 'project': project_id}
    r = requests.post('http://localhost:6969/api/v0/raw_data', json=post_body)
    print(
        'device_id: <{}>; project_id: <{}>; period: <{}s>; (r.status_code == 200) -- {};'.format(
            id, project_id, period, r.status_code == 200
        )
    )
    time.sleep(period)
