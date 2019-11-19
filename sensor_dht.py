import sys
import time
import Adafruit_DHT
import requests

if __name__ == '__main__':
    # Parse command line parameters.
    sensor_args = { '11': Adafruit_DHT.DHT11,
                    '22': Adafruit_DHT.DHT22,
                    '2302': Adafruit_DHT.AM2302 }

    gpio_dht = '17'
    sensor_dht = '11'    

    sensor = sensor_args[sensor_dht]            
    pin = gpio_dht

    '''
    if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
        sensor = sensor_args[sys.argv[1]]
        pin = sys.argv[2]
    else:
        print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
        print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
        sys.exit(1)
    '''
    count = 0
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        temperature = temperature * 9/5.0 + 32 # Convert to farhenheit

        if temperature is not None:
            #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            json_temperature = {'temperature': temperature, 'time': count}
            
            response = requests.post('http://10.13.147.179:5000/temperature', json=json_temperature)
            
            if response.ok:
                print(response.json())
        else:
            print('Failed to get reading. Try again!')
            
        if humidity is not None:
            json_humidity = {'humidity': humidity, 'time': count}
            
            response = requests.post('http://10.13.147.179:5000/humidity', json=json_humidity) # 192.168.1.90
            
            if response.ok:
                print(response.json())
        else:
            print('Failed to get reading. Try again!')
            # sys.exit(1)
        count = count + 5
        time.sleep(5)
