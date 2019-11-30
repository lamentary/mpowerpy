from mRelay import mRelay
import telnetclient
import getpass
import json

class mDevice:
    client = {}
    name = ''
    host = ''
    port = 23
    username = ''
    password = ''
    save_password = False
    relays = []

    def __init__(self, name, host, port, username, password):    
        self.name = name
        self.host = host
        self.port = port
        self.username = username

        if password == '':
            print('Password needed for {0} ({1}:{2})'.format(self.name, self.host, self.port))
            self.password = getpass.getpass().replace('\n','').replace('\r','')
        else:
            self.password = password
            
        self.client = telnetclient.TelNetter(self.host, self.port, self.username, self.password)
        self.relays = []
        self.initialize()

    def initialize(self):
        print('Initializing device')
        print('Asking device for relays')
        
        data = self.client.send_command('ls /proc/power | grep relay')
        values = data.split('\r\n')
        print('Found relays:\n{0}'.format(values))
        i = 1

        for value in values:
            if 'relay' in value:
                print('\tRegistering relay {0}'.format(i))
                relay = mRelay()
                relay.relay_number = i
                relay.get_relay_state(self.client)

                if relay.state == '1':
                    state = 'On'
                else:
                    state = 'Off'

                print('\t\tRelay state: {0} ({1})'.format(relay.state, state))
                self.relays.append(relay)
                i = i + 1

    def json_encode(self):
        json = {
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": '',
            "relays": len(self.relays)
        }

        if self.save_password:
            json["password"] = self.password

        return json
                