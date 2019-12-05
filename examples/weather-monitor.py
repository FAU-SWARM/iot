import sys
import os
import time
import argparse
import datetime
import iotlib
import traceback
import random


def main(args):
    print(vars(args))

    DEVICE_ID_FILE = os.path.join(args.cache, args.device, 'device')
    PROJECT_ID_FILE = os.path.join(args.cache, args.device, 'project')

    device_id = iotlib.get_device_id(
        args.endpoint + '/device', args.device, args.project, DEVICE_ID_FILE, proxies=args.proxy, metadata=dict(random=True)
    )
    project_id = iotlib.get_project_id(
        args.endpoint + '/project', args.project, PROJECT_ID_FILE, proxies=args.proxy
    )

    print(
        'device: <"{}"/{}>; project: <"{}"/{}>;'.format(
            args.device, device_id, args.project, project_id
        )
    )
    then = datetime.datetime.now()
    while True:
        try:
            dick = {
                'demo-luminoscity': 100 + random.randint(0, 69),
                'demo-humidity': 250 + random.randint(0, 69),
                'demo-temperature': 500 + random.randint(0, 69),
                'demo-windspeed': 750 + random.randint(0, 69),
            }
            print(repr(dick))
            success = iotlib.get_ping(args.endpoint + '/ping', proxies=args.proxy) and \
                iotlib.post_data(args.endpoint + '/raw_data', device_id, project_id, dick, proxies=args.proxy)
            print(
                'device: <"{}"/{}>; project: <"{}"/{}>; success: {}; uptime: <{}>'.format(
                    args.device, device_id, args.project, project_id, success,
                    datetime.datetime.now() - then
                )
            )
            time.sleep(args.sample)
        except KeyboardInterrupt:
            print('ctrl + c detected, cached in {}'.format(args.cache))
            break
        except Exception as e:
            print('encountered an error')
            traceback.format_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A dummy iot device, you supply the device name and project and it gets cooking.'
    )
    parser.add_argument(
        '-p',
        '--project',
        help='Project that the device corresponds to.',
        type=str,
        default='swarm'
    )
    parser.add_argument(
        '-d',
        '--device',
        help='Name of this dummy device.',
        type=str,
        default='Raspberry Pi-Dummy' + str(datetime.datetime.now())
    )
    parser.add_argument(
        '-s', '--sample', help='How often the device samples in seconds.', type=int, default=15
    )
    parser.add_argument(
        '-c',
        '--cache',
        help='Where cached files are stored like project and device ID.',
        type=str,
        default='/var/log/iot',
    )
    parser.add_argument(
        '-e',
        '--endpoint',
        help='The API that\'s dealing with all of this data.',
        type=str,
        default='http://localhost:6969/api/v0',
    )
    parser.add_argument(
        '-x',
        '--proxy',
        help='The API that\'s dealing with all of this data.',
        nargs='+',
        type=str,
    )

    args = parser.parse_args()

    args.cache = os.path.abspath(os.path.expanduser(args.cache))
    if not os.path.isdir(args.cache):
        os.makedirs(args.cache)
    if args.proxy is not None and len(args.proxy) > 0:
        if len(args.proxy) == 1:
            args.proxy = {
                'http': args.proxy[0],
            }
        elif len(args.proxy) == 2:
            args.proxy = {
                'http': args.proxy[0],
                'https': args.proxy[1],
            }
    else:
        args.proxy = None

    main(args)
