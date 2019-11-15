import socket, logging, time, sys
from datetime import datetime
    
class TcpClient:

    ip = ''
    port = 0
    username = ''
    password = ''
    isLoggedIn = False
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def start_connection(self):     
        s = self.connection
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.connect((self.ip, self.port))
        response = ''

        attempt = 0
        while len(response) == 0 and attempt < 10:
            attempt = attempt + 1
            data = s.recv(1024)
            time.sleep(.5)

            response = data.decode('utf-8', errors='replace')
            print(response)

        self.log_in(response)
        return response

    def log_in(self, response):
        s = self.connection
        
        while('login' not in response):
            time.sleep(.1)
            data = s.recv(512)
            response = response + data.decode('utf-8', errors='replace')
            print('building initial server response: {0}'.format(response))
        
        s.sendall(bytes(self.username + '\r\n', 'utf-8'))
        data = s.recv(512)
        response = data.decode('utf-8', errors='replace')

        while ('Password' not in response):
            time.sleep(.1)
            data = s.recv(512)
            response = response + data.decode('utf-8', errors='replace')
            print('building user name sent response: {0}'.format(response))

        s.sendall(bytes(self.password + '\r\n', 'utf-8'))
        data = s.recv(512)
        response = data.decode('utf-8', errors='replace')

        while ('#' not in response):
            time.sleep(.1)
            data = s.recv(512)
            response = response + data.decode('utf-8', errors='replace')
            print ('building password sent response: {0}'.format(response))
            
        print('logged in and waiting for response')

    def send_command(self, command):
        logging.basicConfig(filename='tcp_client.log', level=logging.WARNING)
        s = self.connection
                
        if ('\r\n' not in command):
            command = command + '\r\n'

        print('Sending command "{0}"'.format(command.replace('\r\n','')))
        try:
            s.sendall(b'\r\n')
            data = s.recv(512)
        except OSError:
            print('An error occurred sending {0}: {1}'.format(command, sys.exc_info()[0]))
            self.start_connection()
        
        s.sendall(bytes(command, 'utf-8'))
        data = s.recv(512)
        result = data.decode('utf-8', errors='replace')

        while ('#' not in result):
            data = s.recv(512)
            result = result + data.decode('utf-8', errors='replace')
        
        return result.replace('MF.v2.1.11#','Command processed.  Awaiting next command')
        
    def sign_out(self):
        self.connection.close();

    def log_error(self, message):
        now = datetime.now()
        error = '{0}:\t{1}'.format(now.strftime('%m/%d/%Y %H:%M%S'),message)
        logging.error(error)
        print(error)
        