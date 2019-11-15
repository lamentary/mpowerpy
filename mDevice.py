from tcpclient import TcpClient
from mRelay import mRelay

class mDevice:
    client = {}
    relays = []

    def __init__(self, tcpClient):
        self.client = tcpClient
        self.relays = []
        self.initialize()

    def initialize(self):
        print('Initializing device at {0}'.format(self.client.ip))
        print('Asking device for relays')
        data = self.client.send('ls /proc/power | grep relay')
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



