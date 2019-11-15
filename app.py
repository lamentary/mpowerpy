import tcpclient 
from mDevice import mDevice
from mRelay import mRelay

port = 23
username = 'ubnt'
password = 'ubnt'

loggedIn = False

mp8Client = tcpclient.TcpClient('192.168.1.217', port, username, password)
mpminiClinet = tcpclient.TcpClient('192.168.1.215', port, username, password)

mp8 = mDevice(mp8Client)
mpmini = mDevice(mpminiClinet)

print (mp8.relays)
print (mpmini.relays)
