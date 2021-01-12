from netaddr import IPNetwork, iprange_to_cidrs  # pip install netaddr

import socket


##########
# Validate IP address List and return list with Valid IP addresses
########

def ValidateIpList(IPs):
    import socket

    ValidIPs = []

    for IP in IPs:

        try:
            socket.inet_aton(IP)
            ValidIPs.append(IP)
        except:
            pass

    return ValidIPs


###############
# IP List Tranform
#######

# Transform CIDR to IP List
def cidr2ip(subnet):
    ip_list = []
    for ip in IPNetwork(subnet):
        ip_list.append(str(ip))
    return ip_list


# Transform IP Range to CIDR
def range2cidr(subnet):
    range = subnet.replace(" ", "")  # print range
    startip = range.split("-")[0]
    endip = range.split("-")[1]
    cidrs = iprange_to_cidrs(startip, endip)
    return cidrs


# Transform CIDR to IP Range
def cidr2range(subnet):
    ip_list = []
    for ip in IPNetwork(subnet):
        ip_list.append(str(ip))

    IPrange = str(ip_list[0] + " - " + ip_list[int(len(ip_list) - 1)])

    return IPrange


# Transform IP list to Range
def int2dot(intip):
    return '.'.join([str((intip >> x * 8) & 0xFF) for x in [3, 2, 1, 0]])


def dot2int(dotip):
    return reduce(lambda r, x: int(x) + (r << 8), dotip.split('.'), 0)


def iplist2range(range):
    if not range:
        return []
    orig = sorted(map(dot2int, range))
    end, start = zip(*[x for x in zip(orig, orig[1:]) if x[0] + 1 != x[1]]) or ((), ())
    start = [int2dot(orig[0])] + map(int2dot, start)
    end = map(int2dot, end) + [int2dot(orig[-1])]
    return zip(start, end)


##############
# Sort IP List
#########
def SortIP(IPList):
    ips = [socket.inet_pton(socket.AF_INET, ip) for ip in set(IPList)]
    ips.sort()
    return [socket.inet_ntop(socket.AF_INET, ip) for ip in ips]


##############
# IP List to Range
#########
def IPListRange(IPList):
    IPListRange = []
    for range in iplist2range(set(IPList)):
        rg = str(range[0] + " - " + range[1])
        IPListRange.append(rg)
    return IPListRange


##############
# IP List to CIDR
#########
def IPListCIDR(IPList):
    IPListCIDR = []
    IPListRange = []
    for range in iplist2range(set(IPList)):
        rg = str(range[0] + " - " + range[1])
        IPListRange.append(rg)
        for ip in range2cidr(rg):
            IPListCIDR.append(ip)
    return IPListCIDR