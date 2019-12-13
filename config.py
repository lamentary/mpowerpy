import os, json
from mDevice import mDevice

class Config:
    devices = []
    configFile = 'configuration.json'

    def load(self):    
        if (os.path.isfile(self.configFile)):
            with open(self.configFile, 'r') as config:
                data = json.load(config)
                
                for dev in data['devices']:
                    md = mDevice(dev['name'], dev['host'], dev['username'], dev['password'])
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
