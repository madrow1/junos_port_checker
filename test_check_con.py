from jnpr.junos import Device
from jnpr.junos.exception import ConnectError, ConnectTimeoutError

def conn_test():
    dev = Device(host='192.168.0.28', user='rowan', password='V0ldem0rt')
    try:
        dev.open()
    except ConnectTimeoutError:
        print("Connection timed out")
    

conn_test()