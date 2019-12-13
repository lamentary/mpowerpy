class mRelay:
    port = 0
    id = ''
    label = ''
    model = ''
    output = 0
    power = 0.00
    enabled  = 0
    current = 0.00
    voltage = 0.00
    powerfactor = 0.00
    relay = 0
    lock = 0

    def get_relay_state(self, client):
        command = 'cat /proc/power/relay' + str(self.relay_number)
        results = client.send_command(command).replace('\r','').replace('\n','')
        self.state = results[0]
        return self.state

    def turn_relay_on(self, client):
        command = 'echo 1 > /proc/power/relay' + str(self.relay_number)
        client.send(command)
    
    def turn_relay_off(self, client):
        command = 'echo 0 > /proc/power/relay' + str(self.relay_number)
        client.send(command)


