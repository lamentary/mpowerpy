from telnetlib import Telnet

class TelNetter:
    COMMAND_PROMPT = b'MF.v2.1.11# '
    host = ''
    port = 0
    username = ''
    password = ''
    tn = Telnet()

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        

    def connect(self):
        print('Logging in to {0}:{1}'.format(self.host, self.port))
        self.tn = Telnet(host=self.host,port=self.port)
        self.tn.read_until(b'login: ')
        self.tn.write(bytes(self.username + '\n', 'ascii'))
        self.tn.read_until(b'Password: ')
        self.tn.write(bytes(self.password + '\n', 'ascii'))
        recvd = self.tn.read_until(self.COMMAND_PROMPT).decode('ascii')
        print (recvd)
        
    def send_command(self, cmd):    
        #tn = self.connect(self.host, self.port, self.username, self.password)
        if self.tn.host is None:
            self.connect()

        if '\n' not in cmd:
            cmd = cmd + '\n'

        self.tn.write(bytes(cmd, 'ascii'))
        recvd = self.tn.read_until(self.COMMAND_PROMPT).decode('ascii')
        print('Sent: {}'.format(cmd.replace('\n','')))
        resp = recvd.replace('{}'.format(self.COMMAND_PROMPT.decode('ascii')),'')  
        resp = resp.replace(cmd.replace('\n','').replace('\r',''), '')  
        #tn.close()

        return resp.replace(cmd, '')

    def close_connection(self):
        self.tn.close()

    def get_command(self):
        print()
        cmd = input('Enter a command: ')

        if ('\n' not in cmd):
            cmd = cmd + '\n'

        if ('quit' not in cmd.lower()):
            resp = self.send_command(cmd)
            resp = resp.replace(cmd.replace('\n',''),'')
            print(resp)
            self.get_command()
        else:
            print('Done')
            
