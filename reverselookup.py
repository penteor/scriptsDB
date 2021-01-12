import socket, os

# [TODO] - add MultiThreading
# NUM_THREADS = os.cpu_count()

# Reverse Lookup for each IP
def ReverseLookup(IPs):
    ValidDomains = []
    AllIPs = len(IPs)
    for IP in IPs:
        try:
            Check1 = IP.replace('.','-')
            Check2 = "-".join(str(entry) for entry in IP.split('.')[::-1])
            Check3 = ".".join(str(entry) for entry in IP.split('.')[::-1])

            Results = socket.gethostbyaddr(str(IP))
            if (Check1 not in Results[0]) and (Check2 not in Results[0]) and (Check3 not in Results[0]):
                    ValidDomains.append(Results[0])


        except socket.error:
            print("No Results")

        AllIPs = AllIPs - 1
        print("[*] Remaining IPs: " + str(AllIPs))

    return ValidDomains

def replace_strings(string):
    chars = [" ", "\r", "\n"]
    for char in chars:
        string = string.replace(char, '')
    return string

def read_file(FileName):
    OpenFile = open(FileName, 'r')
    IPs = [replace_strings(IP) for IP in OpenFile.readlines()]
    return IPs

def write_file(FileName, Data):
    Lines = [IP + str('\n') for IP in Data]
    OpenFile = open(FileName, 'w')
    OpenFile.writelines(Lines)
    OpenFile.close()

FileName = './results/IPS.lst'
IPs = read_file(FileName)
ReverseLookup = ReverseLookup(IPs)
write_file('./results/reverse.lookup', ReverseLookup)