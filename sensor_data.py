import json
import sys
import os
import time
from datetime import datetime
import Adafruit_DHT
import requests
import smbus

ID_FILE = os.path.expanduser('~/device_id_file')
print(ID_FILE)
if os.path.isfile(ID_FILE):
    print('hi')
    with open(ID_FILE) as r:
        id = r.read()
else:
    print('hi2')
    r = requests.post('http://swarm-fau4214.eastus.cloudapp.azure.com:6969/api/v0/device', json =
    { 'name': 'Raspberry Pi-J' + str(datetime.now()),
    'meta_data': { 'one': 'key' }  
    })
    with open(ID_FILE, 'w') as w:
        print('hi3')
        print(vars(r))
        var = json.loads(r.text)
        id = var['data']['_id']
        w.write(id)

print(id)

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

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
confValues = [0x00, 0x13] # 1/8 gain, 25ms IT (Integration Time)
#Reference data sheet Table 1 for configuration settings

interrupt_high = [0x00, 0x00] # Clear values
#Reference data sheet Table 2 for High Threshold

interrupt_low = [0x00, 0x00] # Clear values
#Reference data sheet Table 3 for Low Threshold

power_save_mode = [0x00, 0x00] # Clear values
#Reference data sheet Table 4 for Power Saving Modes

bus.write_i2c_block_data(addr, als_conf_0, confValues)
bus.write_i2c_block_data(addr, als_WH, interrupt_high)
bus.write_i2c_block_data(addr, als_WL, interrupt_low)
bus.write_i2c_block_data(addr, pow_sav, power_save_mode)

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
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    temperature = temperature * 9/5.0 + 32 # Convert to farhenheit

    if temperature is not None:
        pass
        #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        #post_request(sensor_reading=temperature, sensor_type='Temperature', route='/temperature')
    else:
        print('Failed to get reading. Try again!')

    if humidity is not None:
        pass
        #post_request(sensor_reading=humidity, sensor_type='Humidity', route='/humidity')
    else:
        print('Failed to get reading. Try again!')
        # sys.exit(1)
    
    # Reading lux (luminosity)
    word = bus.read_word_data(addr,als)

    gain = 1.8432 #Gain for 1/8 gain & 25ms IT
    #Reference www.vishay.com/docs/84323/designingveml7700.pdf
    # 'Calculating the LUX Level'

    lux_val = word * gain
    lux_val = round(lux_val,1) #Round value for presentation
    #post_request(sensor_reading=lux_val, sensor_type='Lux', route='/lux')
    
    raw = { 'Temperature': temperature,
            'Humidity': humidity,
            'Lux': lux_val,
            'Date': get_time()
            }
            
    post_body = { 'raw': raw,
                'device': id }
    r = requests.post('http://swarm-fau4214.eastus.cloudapp.azure.com:6969/api/v0/raw_data', 
                        json = post_body)
    print(r.status_code == 200)
    time.sleep(1)
