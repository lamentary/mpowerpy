import os, json
from mfi.mDevice import mDevice
import getpass
import comm.webrequest

class Config:
    devices = []
    configFile = 'config/configuration.json'

    def load(self, autoinitialize = True):    
        if (os.path.isfile(self.configFile)):
            with open(self.configFile, 'r') as config:
                data = json.load(config)
                
                for dev in data['devices']:
                    md = mDevice(dev['name'], dev['host'], dev['username'], dev['password'], autoinitialize)
                    self.devices.append(md)
                    

    def save(self):
        devs = self.get_device_list()

        with open(self.configFile, 'w') as config:
            json.dump(devs, config)

    def get_device_list(self):
        dict_list = []
            
        for dev in self.devices:            
            dict_list.append(dev.json_encode())
            
        devDict = { "devices": dict_list }
            
        return devDict

_config = Config()

def _load_config():    
    if len(_config.devices) == 0:
        _config.load(False)

def _device_manager():
    _load_config()
    print('MPower Setup')
    print()
    print('Options:')
    print('l\t-\tList devices')
    print('a\t-\tAdd a Device')
    print('d #\t-\tDelete a Device by its Number')
    print('m #\t-\tModify a Device by its Number')
    print('q\t-\tQuits setup')
    print()
    selection = input('Select an option: ')

    if 'l' in selection.lower():
        _list_devices()
    elif 'a' in selection.lower():
        add_device()
    elif 'm' in selection.lower():
        index = _parse_index_no(selection)

        if (index >= 0):
            _modify_device(index)
        else:
            _device_manager()
    elif 'd' in selection.lower():
        index = _parse_index_no(selection)

        if (index >= 0):
            delete_device(index)
        else:
            _device_manager()

def _parse_index_no(selection):
    if (' ' not in selection):
        print('Invalid selection')
        _device_manager()
    
    values = selection.split(' ')
    index = 0

    try:
        index = int(values[1])
    except ValueError:
        print('Invalid selection (expected command and "#", where "#" is the device number)')
        return -1
    except:
        print('An error has occured and the command cannot be completed')
        return -1
    
    if (index >= len(_config.devices)):
        print('Invalid device number')
        return -1

    return index

def _list_devices():
    index = 0

    print('Device List')
    print()

    for d in _config.devices:
        dev = mDevice(d.host, d.name, d.username, d.password, False)
        print('{0}\t-\t{1} ({2})'.format(index, dev.name, dev.host))
        index = index + 1
    
    print()
    _device_manager()

def add_device():
    _load_config()
    name = input('Enter a Friendly Name: ')
    host = input('Enter the Device\'s Host Name/IP Address: ')
    username = input('Enter login user name: ')
    password = getpass.getpass().replace('\r','').replace('\n','')
    store_password = input('Do you wish to store the password in the config file? (WARNING: This will be stored unencrypted, and you\'ll need to manage security yourself) (y/N): ')

    dev = mDevice(name, host, username, password)

    if 'y' not in store_password.lower():
        dev.password = ''
    
    _config.devices.append(dev)
    _config.save()
    _config.devices.clear()
    _load_config()
    print('{} added successfully'.format(name))
    _device_manager()
    
def _modify_device(index):
    _load_config()   

    d = _config.devices[index]
    name = input('Enter a Friendly Name ({}): '.format(d.name))
    
    if (len(name) > 0):
        d.name = name
    
    host = input('Enter the Device\'s Host Name/IP Address ({}): '.format(d.host))

    if (len(host) > 0):
        d.host = host

    username = input('Enter login user name ({}): '.format(d.username))

    if (len(username) > 0):
        d.username = username

    password = getpass.getpass().replace('\r','').replace('\n','')
    store_password = input('Do you wish to store the password in the config file? (WARNING: This will be stored unencrypted, and you\'ll need to manage security yourself) (y/N): ')

    if 'y' not in store_password.lower():
        d.password = ''
    else:
        d.password = password

    print('Attempting to login with new information')
    rqr = comm.webrequest.Requester(d.host, d.username, d.password)
    
    if rqr.login() == False:
        save_anyway = input('Login failed.  Would you like to save anyway? (y/N): ')
        
        if ('y' not in save_anyway.lower()):
            print('Modifications not saved')
            _config.devices.clear
            _load_config()
            _device_manager()

    _config.save()
    print('{0}\t-\t{1} saved successfully'.format(index, d.name))
    _device_manager()

def delete_device(index):
    _load_config()
    d = _config.devices[index]

    if (d is None):
        print('Invalid selection.  No device found at {}'.format(index))
        _device_manager()

    del _config.devices[index]
    _config.save()
    _config.devices.clear()
    _load_config()
    _device_manager()

if __name__ == '__main__':
    _device_manager()
