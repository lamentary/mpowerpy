import sys
import urllib, urllib.request
from http import cookies
import json

class Requester:
    cookie_value = 'AIROS_SESSIONID=01234567890123456789012345678902'    

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def login(self, attempt=1):
        data = urllib.parse.urlencode({'username': '{}'.format(self.username), 'password': '{}'.format(self.password)}).encode('ascii')
        url = "http://{}/login.cgi".format(self.ip)
        
        print('Forming login request')  
        req = urllib.request.Request(url, data=data)
        req.add_header('Cookie', self.cookie_value)
        print(req)

        print('Sending login request')
        resp = urllib.request.urlopen(req)
        html = resp.read()

        if ': Controls</title>' not in html.decode('ascii') and attempt < 3:
            print('Unable to login after {} attempts. Trying again'.format(attempt))
            attempt = attempt + 1
            self.login(attempt)
        
        if (': Controls</title>' in html.decode('ascii')):
            print('Login successful\n{}'.format(html.decode('ascii')))
            print('Login complete')
            return True
        else:
            print('Unable to login')
            print(html.decode('ascii'))
            return False

    def get_general_info(self, relay=0, params = ''):
        url = "http://{}/sensors".format(self.ip)

        if (relay > 0):
            url = url + '/{}'.format(relay)

        if (len(params) > 0):
            url = url + '/{}'.format(params)

        return self.send_request(url)

    def change_relay_state(self, relay = 1, new_state = 0):
        url = "http://{0}/sensors/{1}".format(self.ip, relay)  
        data = urllib.parse.urlencode({'relay': '{}'.format(new_state)}).encode('ascii')
        return self.send_request(url, 'PUT', data)

    def send_request(self, url, method='GET', data = None, attempt = 1):
        try:
            if (attempt > 3):
                json = {'status': 'failed', 'reason': 'ERROR: Unable to complete request.  Verify device name/ip, login credentials, and that the device is connected to the network'}
                return json

            req = urllib.request.Request(url, method=method)
            req.add_header('Cookie', self.cookie_value)

            if (data is not None):
                print('Data contains a value, sending request with data')
                resp = urllib.request.urlopen(req, data=data, timeout=60)
            else:
                print('Data is null, sending request only')
                resp = urllib.request.urlopen(req, timeout=60)

            json = resp.read().decode('ascii')
            return json
        except urllib.error.HTTPError as err:
            if (err.code == 302):
                self.login()
                attempt = attempt + 1
                print('Resending request to {0} (method={1} data={2} attempt={3})'.format(url, method, data, attempt))
                return self.send_request(url, method, data, attempt)
            else:
                print(err)
        except urllib.error.URLError as err:
            err_args = err.args[0]
            if (err_args.errno == 10060):
                attempt = attempt + 1
                print('Resending request to {0} (method={1} data={2} attempt={3})'.format(url, method, data, attempt))
                return self.send_request(url, method, data, attempt)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            json = {'status': 'failed', 'reason': 'ERROR: Unable to complete request. {}'.format(sys.exc_info()[0])}
            return json            

if __name__ == "__main__":
    rqr = Requester("192.168.1.217", "ubnt", "ubnt")
    print(rqr.get_general_info())
