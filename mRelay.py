class mRelay:
    relay_number = 0
    state = 0

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


