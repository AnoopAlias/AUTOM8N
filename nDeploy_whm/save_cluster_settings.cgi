#!/usr/bin/python

import commoninclude
import cgi
import cgitb
from requests import get
import yaml


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ansible_inventory_file = "/opt/nDeploy/conf/nDeploy-cluster/hosts"

cgitb.enable()


form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')


if form.getvalue('action'):
    if form.getvalue('action') == "setup":
        master_ipdata = get('http://ip-api.com/json/'+form.getvalue('master_main_ip')).json()
        slave_ipdata = get('http://ip-api.com/json/'+form.getvalue('slave_main_ip')).json()
        master_lat = master_ipdata.get('lat')
        master_lon = master_ipdata.get('lon')
        slave_lat = slave_ipdata.get('lat')
        slave_lon = slave_ipdata.get('lon')
        inventory = {}
        # master
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['ansible_port'] = form.getvalue('master_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['mainip'] = form.getvalue('master_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dbip'] = form.getvalue('master_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dbmode'] = 'readconnroute'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['dns'] = 'geodns'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['latitude'] = master_lat
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['longitude'] = master_lon
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['repo'] = 'ndeploy'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploymaster', {}).setdefault('hosts', {})[form.getvalue('master_hostname')]['server_id'] = 1
        # dbslave
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['ansible_port'] = form.getvalue('slave_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['mainip'] = form.getvalue('slave_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbip'] = form.getvalue('slave_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbmode'] = 'rwsplit'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dns'] = 'geodns'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['latitude'] = slave_lat
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['longitude'] = slave_lon
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['repo'] = 'ndeploy'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['server_id'] = 2
        # slave
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')] = {}
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['ansible_port'] = form.getvalue('slave_ssh_port')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['mainip'] = form.getvalue('slave_main_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbip'] = form.getvalue('slave_db_ip')
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dbmode'] = 'rwsplit'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['dns'] = 'geodns'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['latitude'] = slave_lat
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['longitude'] = slave_lon
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeployslaves', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['repo'] = 'ndeploy'
        inventory.setdefault('all', {}).setdefault('children', {}).setdefault('ndeploydbslave', {}).setdefault('hosts', {})[form.getvalue('slave_hostname')]['server_id'] = 2

        with open(ansible_inventory_file, 'w') as ansible_inventory:
            yaml.dump(inventory, ansible_inventory, default_flow_style=False)

commoninclude.print_success('Cluster settings saved')

print('</body>')
print('</html>')
