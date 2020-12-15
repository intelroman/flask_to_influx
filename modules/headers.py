import datetime, re
#This module will check http headers for altering data.

def headers_check(header, value):
    otgas = {}
    '''
    If ctime or Ctime key is provided in the header we will try to match'it the following format
    YYYY-mm-ddTHH:MM:SSZ if is successtul the time in measurement will be changed with the value
    provided in the Ctime/ctime key this way we can pass thru the header client time and not use
    server time.
    curl -H "ctime: $(date +%Y-%m-%dT%H:%M:%SZ)"
    '''
    if value == 'Ctime' and value in header.keys():
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        try:
            datetime.datetime.strptime(header.get(value), time_format)
            return header.get(value) 
        except ValueError:
            print("This is the incorrect date string format. It should be YYYY-MM-DD")
    
    if value == 'Measurement' and value in header.keys():
        return header.get(value)
    '''
    As server we can't get hostname easy, this header key will help to add hostname.
    curl -H "Chostname: $(hostname)"
    '''
    if value == 'Chostname' and value in header.keys():
        return header.get(value)
    '''
    If in the header there are keys stating with
    Otags- Otags_ otags- otags_
    we pars and create tag for each key base by keyname and the value.
    This way we can add more info in the tags.
    '''
    if 'Otags' in value:
        for i in header.keys():
            if re.match('^Otags-', i):
                otgas.update({ re.sub('^Otags-','',i).lower() : header.get(i)})
        return otgas
    else:
        pass
