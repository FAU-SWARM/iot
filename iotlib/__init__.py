import os
import requests
import datetime
import requests
import random


def get_ping(uri, proxies=None):
    if proxies is not None:
        r = requests.post(uri, proxies=proxies)
    else:
        r = requests.post(uri)
    var = r.json()
    return r.status_code == 200 and var['data'] == 'pong'


def get_device_id(uri, device_name, project_name, filename, proxies=None, metadata=dict()):
    metadata['project'] = project_name
    if os.path.isfile(filename):
        with open(filename) as r:
            device_id = r.read()
    else:
        if proxies is not None:
            r = requests.post(uri, json={'name': device_name, 'meta_data': metadata}, proxies=proxies)
        else:
            r = requests.post(uri, json={'name': device_name, 'meta_data': metadata})
        with open(filename, 'w') as w:
            var = r.json()
            device_id = var['data']['_id']
            w.write(device_id)
    return device_id


def get_project_id(uri, project_name, filename, proxies=None):
    project_id = None
    if os.path.isfile(filename):
        with open(filename) as r:
            project_id = r.read()
    else:
        if proxies is not None:
            r = requests.get(uri, proxies=proxies)
        else:
            r = requests.get(uri)
        body = r.json() if r.status_code == 200 else []
        for project in body['data']:
            if 'name' in project and project['name'].lower() == project_name:
                project_id = project['_id']

        if project_id is None:
            if proxies is not None:
                r = requests.post(uri, json={"name": project_name}, proxies=proxies)
            else:
                r = requests.post(uri, json={"name": project_name})
            var = r.json()
            project_id = var['data']['_id']

        with open(filename, 'w') as w:
            w.write(project_id)
    return project_id


def post_random_data(uri, device_id, project_id, proxies=None):
    raw = {
        'Temperature': random.randint(0, 69696969),
        'Humidity': random.randint(0, 69696969),
        'Lux': random.randint(0, 69696969),
        'Date': str(datetime.datetime.now()),
    }

    post_body = {'raw': raw, 'device': device_id, 'project': project_id}
    if proxies is not None:
        r = requests.post(uri, json=post_body, proxies=proxies)
    else:
        r = requests.post(uri, json=post_body)

    return r.status_code == 200


def post_data(uri, device_id, project_id, data, proxies=None):
    post_body = {'raw': data, 'device': device_id, 'project': project_id}
    if proxies is not None:
        r = requests.post(uri, json=post_body, proxies=proxies)
    else:
        r = requests.post(uri, json=post_body)

    return r.status_code == 200
