from datetime import datetime
from flask import request
import random, string
#Current time on server cuurent time
ctime = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

#Client ip 
clientip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

#Example: https://pynative.com/python-generate-random-string/
def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str