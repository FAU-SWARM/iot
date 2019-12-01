# iot
IOT for the SWARM project

# Scripts
```batch
python iot\test\device.py --cache /var/log/iot/local/0 --device rpi-dummy0
python iot\test\device.py --cache /var/log/iot/local/1 --device rpi-dummy1 --project not-swarm

python iot\test\device.py --cache /var/log/iot/remote/2 --device rpi-dummy2 --endpoint http://swarm-fau4214.eastus.cloudapp.azure.com:6969/api/v0
python iot\test\device.py --cache /var/log/iot/remote/3 --device rpi-dummy3 --endpoint http://swarm-fau4214.eastus.cloudapp.azure.com:6969/api/v0 --project not-swarm
```
