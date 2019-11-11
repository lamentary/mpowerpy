import socket, logging, time
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
        self.start_connection()

    def start_connection(self):        
        #with self.connection as s:
        s = self.connection
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.connect((self.ip, self.port))
        
        attempt = 0
        while True and attempt < 10:
            attempt = attempt + 1
            data = s.recv(1024)

            response = data.decode('utf-8', errors='replace')
            print(response)

            if ('login' in response):
                break
            else:
                if (len(data) > 0):
                    s.sendall(b'\n')
                    data = s.recv(1024)

            if (attempt == 10):
                error = 'Unable to connect to {0} port {1} after {2} attempts.'.format(self.ip, self.port, attempt)
                print(error)
                logging.error(error)
            else:
                isLoggedIn = False
                attempt = 0
                data = s.recv(1024)                    
                response = data.decode('utf-8', errors='replace')
                print(response)

                while (isLoggedIn == False and attempt < 10):                    
                    attempt = attempt + 1

                    #if (len(data) > 0):
                        #   response = data.decode('utf-8', errors='replace')

                    if ('login' in response):
                        response = self.send_command(self.username)
                        print(response)
                    elif ('password' in response or 'Password' in response):
                        response = self.send_command(self.password)
                        print(response)
                    elif ('#' in response):
                        isLoggedIn = True
                        self.send_command('cd /\r\n')
                        break
                    elif ('\r\n' == response):
                        data = s.recv(1024)
                        response = data.decode('utf-8', errors='replace')
                        print(response)
                    else:
                        error = 'Unable to login to {0} on port {1} with username {2} (response: {3})'.format(self.ip, self.port, self.username, response)
                        self.log_error(error)
                
                if (isLoggedIn == True):
                    break

    def send_command(self, command):
        logging.basicConfig(filename='tcp_client.log', level=logging.WARNING)
        s = self.connection

        if (self.isLoggedIn):
            s.sendall('\r\n')
            data = s.recv(1024)
            response = data.decode('utf-8', errors='replace')
            if ('#' not in response):
                self.start_connection()
        try:
            if len(command) == 0:
                result = 'No command to process'

            if command.find('\n') < 0:
               command = command + '\n'
            
            #with self.connection as s:
            attempt = 0
            s.sendall(bytes(command, encoding='utf-8'))
            while True and attempt < 5:
                attempt = attempt + 1
                data = s.recv(4096)
                print('Server says {0}'.format(data))
                result = data.decode('utf-8',errors='replace')

                if (result == command):
                    s.sendall(b'\n')
                elif (len(result) > 0 and result != command):
                    break
                                    
            print('Server says: {0}'.format(data.decode('utf-8', errors='replace')))
                

            result = data.decode('utf-8', errors='replace')
            print(result)
            print('Full socket result: {0}'.format(result))

            return result

        except Exception as ex:
            message = 'Error sending command \'{0}\' to {1} on port {2}: {3}'.format(command, self.ip, self.port, ex)
            self.log_error(message)

    def log_error(self, message):
        now = datetime.now()
        error = '{0}:\t{1}'.format(now.strftime('%m/%d/%Y %H:%M%S'),message)
        logging.error(error)
        print(error)
        