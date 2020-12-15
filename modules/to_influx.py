from flask import request
def to_influx(data, measurement):
    Measurement = measurement
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
    for i in data.keys():
        info = i
        tags.update({'ip': clientip, 'obj_info': i, "hostname" : Chostname})
        influx_data.append({'measurement': Measurement,
                            'tags': tags,
                            'time': ctime,
                            'fields': data.get(i)
            })
    return influx_data

def to_influx_valstags(data, measurement):
    Measurement = measurement
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
    for i in data.keys():
        info = i
        for x in data[i]:
            tags.update({'ip': clientip, 'obj_info': i, "hostname" : Chostname})
            tags.update(x.get("tags"))
            influx_data.append({'measurement': Measurement,
                                'tags': tags,
                                'time': ctime,
                                'fields': x.get("vals")
                })
    return influx_data