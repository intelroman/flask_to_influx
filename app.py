from flask import Flask, request, jsonify, session
from flask_httpauth import  HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from modules.influxdb import push_data
import os, datetime, logging, re,json

'''Confguring lgging system and format'''
from logging.handlers import RotatingFileHandler
logging.basicConfig(
        handlers=[RotatingFileHandler('logs/applogs.log', maxBytes = 20000000, backupCount=5)],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getcwd()+'/db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class User(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(80),
                         unique=True,
                         nullable=False)
    pw_hash = db.Column(db.String(256),
                        nullable=False)
    token = db.Column(db.String(256))
    def set_password(self, password):
        """Create hashed password."""
        self.pw_hash = generate_password_hash(
            password,
            method='sha256'
        )
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.pw_hash, password)
    def check_token(self, token):
        if self.token == token:
            return True
        else:
            return False
    def set_token(self, lenght):
        from modules.variables import get_random_string
        self.token = get_random_string(lenght)
    def __repr__(self):
        return self.username
#Auth part
#Examples https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
@auth.verify_password
def verify_password(username, password):
    alluser = User.query.filter_by(username = username).first()
    if not alluser or not alluser.check_password(password):
        return False
    return True

@app.route('/users/check', methods=['GET'])
@auth.login_required
def chk_user():
    return jsonify({'data': 'Hello, %s' % auth.username()})

@app.route('/show/headers', methods=['GET','POST'])
def show_headers():
    return jsonify(dict(request.headers))

@app.route('/')
def rootdir():
    return "This is root directory of the influx_http_feed project"

@app.route('/users/list', methods=['GET'])
def lusers():
    alluser = User.query.all()
    return jsonify({'Users' : str(alluser)})
@app.route('/users/list/<user>', methods=['GET'])
def lusers_(user):
    alluser = User.query.filter_by(username=user).first()
    if alluser is None:
        return 'User: \"{}\" not found in database'.format (user)
    else:
        return 'User: \"{}\" found in database'.format (alluser)

@app.route('/users/add/<user>/token', methods=['Post'])
def user_token_add(user):
    alluser = User.query.filter_by(username=user).first()
    if alluser is None:
        return 'User: \"{}\" not found in database'.format (user)
    elif alluser.check_token() is None:
        alluser.set_token(100)
        db.session.add(alluser)
        db.session.commit()
        return 'User: \"{}\" found but don\'t have token create toke'.format (user)
    else:
        return 'User: \"{}"\ have token only admin can reset your token in database'
'''
Linux base curl:
data=$(cat /proc/net/dev); curl --location --request POST 'http://<ip>:5000/linux/proc_net_dev' --header 'Content-Type: application/json' --header 'Accept: application/json'  --data-raw "$data"
'''
@app.route('/linux/proc_net_dev', methods = ['POST'])
def proc_net_dev():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    import modules.linux.proc_net_dev as net
    data = request.data.decode('utf-8')
    print(request.headers)
    net_dev = net.pars(data)
    infdata = net.to_influx(net_dev)
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

'''
Working with file in postman .. need to figure out why curl is not working.
'''
@app.route('/linux/file/proc_net_dev', methods = ['POST'])
def file_proc_net_dev():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    if 'file' not in request.files:
        return "File need a file"
    elif request.files['file'].filename in {'proc_net_dev', 'dev'}:
        data = request.files['file'].read()[0:].decode('utf-8')
    else:
        return "Be sure you use /proc/net/dev or dev file"
    import modules.linux.proc_net_dev as net
    from modules.influxdb import push_data
    net_dev = net.pars(data)
    infdata = net.to_influx(net_dev)
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

'''
Linux base curl:
data=$(cat /proc/net/arp); curl --location --request POST 'http://<ip>:5000/linux/proc_net_arp' --header 'Content-Type: application/json' --header 'Accept: application/json'  --data-raw "$data"
'''
@app.route('/linux/proc_net_arp', methods = ['POST'])
def proc_net_arp():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    import modules.linux.proc_net_arp as arp
    data = request.data.decode('utf-8')
    net_arp = arp.pars(data)
    infdata = arp.to_influx(net_arp)
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

'''
Working with file in postman .. need to figure out why curl is not working.
'''
@app.route('/linux/file/proc_net_arp', methods = ['POST'])
def file_proc_net_arp():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    if 'file' not in request.files:
        return "need a file"
    elif request.files['file'].filename in {'proc_net_arp', 'arp'}:
        data = request.files['file'].read()[0:].decode('utf-8')
    else:
        return "Be sure you use /proc/net/arp or arp file"
    import modules.linux.proc_net_arp as arp
    net_arp = arp.pars(data)
    infdata = arp.to_influx(net_arp)
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

'''
Linux base curl:
data=$(cat /proc/meminfo); curl --location --request POST 'http://<ip>:5000/linux/proc_meminfo' --header 'Content-Type: application/json' --header 'Accept: application/json'  --data-raw "$data"
'''
@app.route('/linux/proc_meminfo', methods = ['POST'])
def proc_meminfo():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    import modules.linux.proc_meminfo as meminfo
    import modules.to_influx as influx
    data = request.data.decode('utf-8')
    mem = meminfo.pars(data, "meminfo")
    infdata = influx.to_influx(mem, "meminfo")
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

'''
Working with file in postman .. need to figure out why curl is not working.
'''
@app.route('/linux/file/proc_meminfo', methods = ['POST'])
def file_proc_meminfo():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    if 'file' not in request.files:
        return "need a file"
    elif request.files['file'].filename in {'proc_meminfo', 'meminfo'}:
        data = request.files['file'].read()[0:].decode('utf-8')
    else:
        return "Be sure you use /proc/net/meminfo or meminfo file"
    import modules.linux.proc_meminfo as meminfo
    import modules.to_influx as influx 
    mem = meminfo.pars(data, "meminfo")
    infdata = influx.to_influx(mem, "meminfo")
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

'''
Linux base curl:
data=$(cat /proc/vmstat); curl --location --request POST 'http://<ip>:5000/linux/proc_vmstat' --header 'Content-Type: application/json' --header 'Accept: application/json'  --data-raw "$data"
'''
@app.route('/linux/proc_vmstat', methods = ['POST'])
def proc_vmstats():
    logging.info('Starting prcessing %s for ip %s ', request.path, request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    import modules.linux.proc_vmstat as vmstat
    import modules.to_influx as influx 
    data = request.data.decode('utf-8')
    vmstat_ = vmstat.pars(data, "vmstat")
    infdata = influx.to_influx(vmstat_, "vmstat")
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

@app.route('/linux/proc_uptime', methods = ['POST'])
def proc_uptime():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    import modules.linux.proc_uptime as uptime
    import modules.to_influx as influx 
    data = request.data.decode('utf-8')
    uptime_ = uptime.pars(data, "uptime")
    infdata = influx.to_influx(uptime_, "uptime")
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})
'''
Linux base curl:
data=$(cat /proc/diskstats); curl --location --request POST 'http://<ip>:5000/linux/proc_diskstats?tags=0,1,2&vals=3,4,5,6,7,8,9,10,11,12,13' --header 'Content-Type: application/json' --header 'Accept: application/json'  --data-raw "$data"
For the tags and values see:
https://www.kernel.org/doc/Documentation/ABI/testing/procfs-diskstats
'''
@app.route('/linux/proc_diskstats', methods = ['POST'])
def linux_disk():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    from modules.args import chk_arg 
    from modules.linux.proc_diskstats import pars
    from modules.to_influx import to_influx_valstags as influx
    tag_list = chk_arg('tags')
    vals_list = chk_arg('vals')
    data = request.data.decode('utf-8')
    diskstats = pars(data, "diskstats", tag_list, vals_list)
    infdata = influx(diskstats, "diskstats")
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

@app.route('/json/raw', methods = ['POST'])
def json_raw():
    logging.info ('Starting prcessing %s for ip %s ', request.path, (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    '''
    Influx format data: https://github.com/influxdata/influxdb-python
    [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "value": 0.64
            }
        }
    ]
    '''
    if request.content_type != 'application/json':
        logging.error ('%s %s has no application/json in the header as content type', (request.environ.get('HTTP_X_REAL_IP', request.remote_addr)), request.path)
        return jsonify ({"Error": "Expecting Json"}), 403
    data = request.get_json()
    import modules.to_influx as influx 
    infdata = influx.to_influx(data, "raw")
    from modules.influxdb import push_data
    return jsonify ({"Status": push_data(infdata)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)