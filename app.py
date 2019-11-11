import tcpclient 

ip = "192.168.1.xxx"
port = 23
username = 'ubnt'
password = 'ubnt'

loggedIn = False

client = tcpclient.TcpClient(ip, port, username, password)
print('Sending ls')
response = client.send_command('ls\r\n')
print (response)