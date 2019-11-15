import tcpclient 

ip = "192.168.1.999"
port = 23
username = 'ubnt'
password = 'ubnt'

loggedIn = False

client = tcpclient.TcpClient(ip, port, username, password)
response = client.send_command('ls\r\n')
print (response)
response = client.send_command('cd /dev\r\n')
print (response)
response = client.send_command('ls\r\n')
print (response)

client.sign_out()
