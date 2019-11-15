import socket, logging, time, sys
from datetime import datetime
    
class TcpClient:

    ip = ''
    port = 0
    username = ''
    password = ''
    isLoggedIn = False
    connection = {}
    
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.start_connection()

    def start_connection(self):     
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        
        print('Sending login info: username')
        response = self.get_results(self.username + '\r\n', 'Password')

        print('Sending login info: password')
        self.get_results(self.password + '\r\n')
            
        print('logged in and waiting for response')

    def send(self, command):
        logging.basicConfig(filename='tcp_client.log', level=logging.WARNING)
        s = self.connection
                
        if ('\r\n' not in command):
            command = command + '\r\n'

        #print('Sending command "{0}"'.format(command.replace('\r\n','')))
        try:
            s.sendall(b'\r\n')
            data = s.recv(512)
        except OSError:
            print('An error occurred sending {0}: {1}'.format(command, sys.exc_info()[0]))
            self.start_connection()
        
        result = self.get_results(command)
        
        return result.replace('MF.v2.1.11#','')
        
    def get_results(self, command, end_of_trans = '#'):
        s = self.connection

        s.sendall(bytes(command, 'utf-8'))
        data = s.recv(512)
        response = data.decode('utf-8', errors='replace')

        while (end_of_trans not in response):
            time.sleep(.1)
            data = s.recv(512)
            response = response + data.decode('utf-8', errors='replace')

        return response.replace(command,'')

    def sign_out(self):
        self.connection.close();

    def log_error(self, message):
        now = datetime.now()
        error = '{0}:\t{1}'.format(now.strftime('%m/%d/%Y %H:%M%S'),message)
        logging.error(error)
        print(error)
        