#!/usr/bin/python

import cgi
import cgitb
import subprocess
import os
from commoninclude import sighupnginx, print_success, print_nontoast_error


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('ddos'):
    if form.getvalue('ddos') == 'enable':
        os.rename("/etc/nginx/conf.d/dos_mitigate_systemwide.disabled", "/etc/nginx/conf.d/dos_mitigate_systemwide.enabled")
        sighupnginx()
        # Do this clusterwide if we are on a cluster
        if os.path.isfile(cluster_config_file):
            the_raw_cmd_slave = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"mv /etc/nginx/conf.d/dos_mitigate_systemwide.disabled /etc/nginx/conf.d/dos_mitigate_systemwide.enabled && nginx -s reload\"'
            run_cmd = subprocess.Popen(the_raw_cmd_slave, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        print_success('Nginx DDOS mitigation is now enabled.')
        if os.path.isfile(cluster_config_file):
            print('<ul class="list-unstyled text-left">')
            while True:
                line = run_cmd.stdout.readline()
                if not line:
                        break
                print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
            print('</ul>')
    elif form.getvalue('ddos') == 'disable':
        os.rename("/etc/nginx/conf.d/dos_mitigate_systemwide.enabled", "/etc/nginx/conf.d/dos_mitigate_systemwide.disabled")
        sighupnginx()
        # Do this clusterwide if we are on a cluster
        if os.path.isfile(cluster_config_file):
            the_raw_cmd_slave = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"mv /etc/nginx/conf.d/dos_mitigate_systemwide.enabled /etc/nginx/conf.d/dos_mitigate_systemwide.disabled && nginx -s reload\"'
            run_cmd = subprocess.Popen(the_raw_cmd_slave, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        print_success('Nginx DDOS mitigation is now disabled.')
        if os.path.isfile(cluster_config_file):
            print('<ul class="list-unstyled text-left">')
            while True:
                line = run_cmd.stdout.readline()
                if not line:
                        break
                print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
            print('</ul>')
else:
    print_nontoast_error('<h3>Forbidden!</h3>Though shall not Pass!')

print('</body>')
print('</html>')