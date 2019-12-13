from mRelay import mRelay
import webrequest
import telnetclient
import getpass
import json
import time

class mDevice:
    cnx = {}
    name = ''
    host = ''
    username = ''
    password = ''
    save_password = False
    relays = []

    def __init__(self, name, host, username, password, autoinitialize = True):    
        self.name = name
        self.host = host
        self.username = username
        self.password = password
        self.cnx = webrequest.Requester(host, username, password)
        self.relays = []

        if (autoinitialize):
            self.initialize()

    def initialize(self):
        print('Initializing device')
        if self.password == '':
            print('Password needed for {0} ({1})'.format(self.name, self.host))
            self.password = getpass.getpass().replace('\n','').replace('\r','')

        print('Asking device for relays')
        results = json.loads(self.cnx.get_general_info())
        print(results)
        sensors = results['sensors']

        for sensor in sensors:
            r = mRelay()
            r.port = sensor['port']
            r.id = sensor['id']
            r.label = sensor['label']
            r.model = sensor['model']
            r.output = sensor['output']
            r.power = sensor['power']        
            r.enabled = sensor['enabled']
            r.current = sensor['current']
            r.voltage = sensor['voltage']
            r.powerfactor = sensor['powerfactor']
            r.relay = sensor['relay']
            r.lock = sensor['lock']
            self.relays.append(r)

    def get_relay_state(self, relay_no = 0):
        states = json.loads(self.cnx.get_general_info(relay_no))
        sensors = states['sensors']

        for sensor in sensors:            
            r = self.relays[sensor['port'] - 1]     # The relays list is a 0-based index, but the ports on the device use a 1-based index
            r.output = sensor['output']
            r.power = sensor['power']        
            r.enabled = sensor['enabled']
            r.current = sensor['current']
            r.voltage = sensor['voltage']
            r.powerfactor = sensor['powerfactor']
            r.relay = sensor['relay']
            r.lock = sensor['lock']

    def change_relay_state(self, relay_no = 0, state = 1):
        message = ''

        if (relay_no > 0):
            message = 'Set relay {0} to {1} results: {2}'.format(relay_no, state, self.cnx.change_relay_state(relay_no, state))   
            self.get_relay_state(relay_no)         
        else:
            for relay in self.relays:
                if len(message) > 0:
                    message = message + '\r\n'
                message = message + 'Set relay {0} to {1} results: {2}'.format(relay.port, state, self.cnx.change_relay_state(relay.port, state))
            self.get_relay_state()

        return message              

    def json_encode(self):
        json = {
            "name": self.name,
            "host": self.host,
            "username": self.username,
            "password": '',
            "relays": len(self.relays)
        }

        if self.save_password:
            json["password"] = self.password

        return json
                

def print_relay_states(d):
    for relay in d.relays:
        if (relay.relay == 1):
            state = 'ON'
        else:
            state = 'OFF'   
        print('Relay {0} state: {1}'.format(relay.port, state))

if __name__ == '__main__':
    d = mDevice('Mini', '192.168.1.217', 'ubnt', 'ubnt')
    print('Found {} relays'.format(len(d.relays)))    
    print('Turning all relays off')
    print('After command: ' + d.change_relay_state(0, 0))    
    print_relay_states(d)
    print(d.cnx.get_general_info())
    print('Turning all relays on')
    print('After command: ' + d.change_relay_state(0, 1))    
    print(d.cnx.get_general_info())
    print_relay_states(d)


    

