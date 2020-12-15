import re
from flask import request
#This module pars linux /proc/net/dev format file.
# IP address       HW type     Flags       HW address            Mask     Device
# 192.168.188.1    0x1         0x2         00:50:56:c0:00:08     *        ens33
# 192.168.188.2    0x1         0x2         00:50:56:fe:a0:07     *        ens33

def pars(data):
    rdata = {}
    intname = []
    for i in data.split("\n"):
        i = re.sub(" +", " ", i)
        i = re.sub("(:|^ |\r)", "", i)
        if i.startswith('IP address'):
            pass
        else:
            if i.split(" ")[-1] not in intname:
                interface = i.split(" ")[-1]
                intname.append(interface)
                rdata.update({i.split(" ")[-1]: 1})
            else:
                rdata[i.split(" ")[-1]] += 1
    return rdata

def to_influx(net_arp):
    Measurement = 'proc_net_arp'
    tags = {}
    from modules.variables import ctime, clientip
    from modules.headers import headers_check
    if headers_check(request.headers, 'Ctime'):
        ctime = headers_check(request.headers, 'Ctime')
    if headers_check(request.headers, 'Chostname'):
        Chostname = headers_check(request.headers, 'Chostname')
    else:
        Chostname = clientip
    if headers_check(request.headers, 'Measurement'):
        Measurement = headers_check(request.headers, 'Measurement')
    if headers_check(request.headers, 'Otags'):
        tags = headers_check(request.headers, 'Otags')
    influx_data = []
    for i in net_arp.keys():
        iface = i
        tags.update({'ip': clientip, 'interface': i, "hostname" : Chostname})
        influx_data.append({'measurement': Measurement,
                            'tags': tags,
                            'time': ctime,
                            'fields': {'value' : net_arp.get(i)}
            })
    return influx_data