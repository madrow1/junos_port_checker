from jnpr.junos import Device
from jnpr.junos.op.ethport import EthPortTable
from jnpr.junos.op.phyport import PhyPortTable
from jnpr.junos.op.vlan import VlanTable,VlanView
from jnpr.junos.exception import ConnectError,ConnectTimeoutError
from getpass import getpass
from jnpr.junos.factory.factory_loader import FactoryLoader
import sys,json,yaml,os,time

def read_json_config(file):
    f = open(file)
    json_file = json.load(f)
    return json_file

def conn_test(hostname,username,junos_pass,start_time):
    vars = {'junos_login' :{'host' : hostname, "user" : username}}
    dev = Device(host=hostname,user=username,passwd=junos_pass)
    try:
        dev.open()
        return True
    except ConnectTimeoutError:
        end_time = time.time() - start_time
        log(vars, check_con=False, end_time=end_time)
        return False, exit()

def log(vars,check_con,end_time):
        to_log = "\nHost: ", vars["junos_login"]["host"], " User: ", vars["junos_login"]["user"]
        if check_con == True:
             log_con = " \nConnection successful "
        else:
             log_con = " \nConnection failed "

        time_taken = "\nTime to execute: %s " % end_time 

        with open('port_log.txt', 'a') as log:
             log.writelines(to_log)
             log.writelines(log_con)
             log.writelines(time_taken)

#def get_facts(vars):
#    dev = Device(host=vars["junos_login"]["host"], user=vars["junos_login"]["user"], passwd=vars["junos_login"]["password"], use_filter=True) 
    #print(dev.facts['hostname'])
#    print(dev.facts)

def check_eth_status(vars):
    port_yml = """
---
PortTable:
  get: interfaces/interface
  view: PortView
PortView:
  fields:
   name: name
   unit: unit/name
   vlan: unit/family/ethernet-switching/storm-control/profile-name
   vlan-id: unit/vlan-id
   inet_address: unit/family/inet/address/name
VlanTable:
  rpc: get-vlan-information
  item: l2ng-l2ald-vlan-instance-group
  key: l2ng-l2rtb-vlan-name
  view: VlanView
VlanView:
  fields:
   name: l2ng-l2rtb-name
   interfaces: l2ng-l2rtb-vlan-member/l2ng-l2rtb-vlan-member-interface
   mode: l2ng-l2rtb-vlan-member/l2ng-l2rtb-vlan-member-interface-mode
    """

    globals().update(FactoryLoader().load(yaml.load(port_yml, Loader=yaml.FullLoader)))    

    with Device(host=vars["junos_login"]["host"], user=vars["junos_login"]["user"], passwd=vars["junos_login"]["password"], use_filter=True) as dev:
        eth_stat = EthPortTable(dev)
        eth_stat.get()
        port_stat = PortTable(dev)
        port_stat.get()
        vlan_stat = VlanTable(dev)
        vlan_stat.get()

    for port in eth_stat.keys():
        print("Port: {0}".format(port))
        print("Operational state is : {0}".format(eth_stat[port]['oper']))
        print("IP address is: {0}".format(port_stat[port]['inet_address']))
        print("The VLAN-id for this port is: {0}".format(port_stat[port]['vlan-id']))
        #print("Packets-in are : {0}".format(eth_stat[port]['rx_packets']))
        #print("Packets-out are : {0}".format(eth_stat[port]['tx_packets']))









