from mfi.mDevice import mDevice
from mfi.mRelay import mRelay
from config.config import Config
import json

username = 'ubnt'
password = 'ubnt'

config = Config()

print('Loading configuration')
config.load()

if (len(config.devices) == 0):
    print('No devices found, creating devices')
    mp8 = mDevice('MPower Pro 8',"192.168.1.217", username, password)
    mpmini = mDevice('MPower Mini',"192.168.1.215", username, password)
    mp8.save_password = True
    mpmini.save_password = True
    devices = config.devices
    devices.append(mp8)
    devices.append(mpmini)
    config.save()
else:
    print('{0} devices loaded.'.format(len(config.devices)))

    for device in config.devices:
        print('Getting information for "{}"'.format(device.name))
        mp = mDevice(device.name, device.host, device.username, device.password)
        print (mp.print_relay_states())
