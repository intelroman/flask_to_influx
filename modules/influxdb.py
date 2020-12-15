from influxdb import InfluxDBClient
from modules.config import influx

client = InfluxDBClient(host=influx['host'], port=influx['port'], username=influx['username'], password=influx['password'])
client = client.switch_database(influx['db'])

def push_data(data):
    try:
        client.write_points(data)
        Success = True
    except:
        print ("Log the failure")
        Success = False
    return Success