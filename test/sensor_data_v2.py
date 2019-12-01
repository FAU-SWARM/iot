import sys
import os
import time
import argparse
import datetime
import iotlib
import traceback

import smbus
import Adafruit_DHT


def main(args):
    print(vars(args))

    sensor_args = {'11': Adafruit_DHT.DHT11, '22': Adafruit_DHT.DHT22, '2302': Adafruit_DHT.AM2302}

    gpio_dht = '17'
    sensor_dht = '11'

    sensor = sensor_args[sensor_dht]
    pin = gpio_dht

    bus = smbus.SMBus(1)
    addr = 0x10

    #Write registers
    als_conf_0 = 0x00
    als_WH = 0x01
    als_WL = 0x02
    pow_sav = 0x03

    #Read registers
    als = 0x04
    white = 0x05
    interrupt = 0x06

    # These settings will provide the max range for the sensor (0-120Klx)
    # but at the lowest precision:
    #              LSB   MSB
    confValues = [0x00, 0x13]  # 1/8 gain, 25ms IT (Integration Time)
    #Reference data sheet Table 1 for configuration settings

    interrupt_high = [0x00, 0x00]  # Clear values
    #Reference data sheet Table 2 for High Threshold

    interrupt_low = [0x00, 0x00]  # Clear values
    #Reference data sheet Table 3 for Low Threshold

    power_save_mode = [0x00, 0x00]  # Clear values
    #Reference data sheet Table 4 for Power Saving Modes

    bus.write_i2c_block_data(addr, als_conf_0, confValues)
    bus.write_i2c_block_data(addr, als_WH, interrupt_high)
    bus.write_i2c_block_data(addr, als_WL, interrupt_low)
    bus.write_i2c_block_data(addr, pow_sav, power_save_mode)

    DEVICE_ID_FILE = os.path.join(args.cache, 'device')
    PROJECT_ID_FILE = os.path.join(args.cache, 'project')

    device_id = iotlib.get_device_id(
        args.endpoint + '/device', args.device, args.project, DEVICE_ID_FILE, proxies=args.proxy
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
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            temperature = temperature * 9 / 5.0 + 32  # Convert to farhenheit

            # Reading lux (luminosity)
            word = bus.read_word_data(addr, als)

            gain = 1.8432  #Gain for 1/8 gain & 25ms IT
            #Reference www.vishay.com/docs/84323/designingveml7700.pdf
            # 'Calculating the LUX Level'

            lux_val = round(word * gain, 1)  #Round value for presentation

            success = iotlib.get_ping(args.endpoint + '/ping', proxies=args.proxy) and \
                iotlib.post_data(args.endpoint + '/raw_data', device_id, project_id, dict(Temperature=temperature, Humidity=humidity, Lux=lux_val), proxies=args.proxy)
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
