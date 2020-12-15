import re
from flask import request
from pprint import pprint as pp
#This module pars linux /proc/net/dev format file.
# Inter-|   Receive                                                |  Transmit
#  face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
#     lo: 215295621  296030    0    0    0     0          0         0 215295621  296030    0    0    0     0       0          0
#  ens33: 384468197  607432    0    0    0     0          0         0 107432459  201560    0    0    0     0       0          0

def pars(data):
    rdata = {}
    for i in data.split("\n"):
        i = re.sub(" +", " ", i)
        i = re.sub("(:|^ )", "", i)
        cols = ['Interface','RX bytes','RX pakets','RX errors','RX drops','RX fifo','RX frame','RX compressed','RX multicast','TX bytes','TX packets','TX errors','TX drop','TX fifo','TX colls', 'TX carrier','TX compressed']
        if i.startswith('Inter-|') or i.startswith('face |'):
            pass
        else:
            intname = ''
            for x,y in enumerate(i.split(" ")):
                if x == 0:
                    rdata.update({y : {}})
                    intname = y
                elif x > 0:
                    rdata[intname].update({ cols[x]: int(y)})
    return rdata

def to_influx(net_dev):
    Measurement = 'proc_net_dev'
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
    for i in net_dev.keys():
        iface = i
        tags.update({'ip': clientip, 'interface': i, "hostname" : Chostname})
        influx_data.append({'measurement': Measurement,
                            'tags': tags,
                            'time': ctime,
                            'fields': net_dev.get(i)
            })
    return influx_data