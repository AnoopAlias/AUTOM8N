#!/usr/bin/env python

import commoninclude
import cgitb
import subprocess
import cgi
import psutil
import os
import yaml

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
xtendweb_installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"


cgitb.enable()
form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('mode') and form.getvalue('unit') and form.getvalue('cpu') and form.getvalue('memory') and form.getvalue('blockio'):
    if form.getvalue('mode') == 'service':
        myservice = form.getvalue('unit')+".service"
        if form.getvalue('cpu') == '25':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=256', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=256"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        if form.getvalue('cpu') == '50':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=512', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=512"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('cpu') == '75':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=768', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=768"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('cpu') == '100':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=1024', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=1024"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        if form.getvalue('blockio') == '25':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=250', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=250"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        if form.getvalue('blockio') == '50':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=500', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=500"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('blockio') == '75':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=750', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=750"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('blockio') == '100':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=1000', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=1000"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        mymem = psutil.virtual_memory().total
        mem_quarter = float(mymem) * 0.25
        mem_threequarter = float(mymem) * 0.75
        mem_half = float(mymem) / 2.0
        if form.getvalue('memory') == '25':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_quarter)), shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_quarter))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        if form.getvalue('memory') == '50':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_half)), shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_half))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('memory') == '75':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_threequarter)), shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_threequarter))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('memory') == '100':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(mymem), shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mymem))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUAccounting=yes', shell=True)
        subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOAccounting=yes', shell=True)
        subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryAccounting=yes', shell=True)
        subprocess.call('/usr/bin/systemctl daemon-reload', shell=True)
        if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
            with open(os.devnull, 'w') as FNULL:
                subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl daemon-reload"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    elif form.getvalue('mode') == 'user':

        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        myservice = 'ndeploy_hhvm@'+form.getvalue('unit')+".service"
        if form.getvalue('cpu') == '25':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=256', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=256"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        if form.getvalue('cpu') == '50':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=512', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=512"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('cpu') == '75':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=768', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=768"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('cpu') == '100':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=1024', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=1024"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        if form.getvalue('blockio') == '25':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=250', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=250"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        if form.getvalue('blockio') == '50':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=500', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=500"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('blockio') == '75':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=750', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=750"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('blockio') == '100':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=1000', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=1000"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        mymem = psutil.virtual_memory().total
        mem_quarter = float(mymem) * 0.25
        mem_threequarter = float(mymem) * 0.75
        mem_half = float(mymem) / 2.0
        if form.getvalue('memory') == '25':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_quarter)), shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_quarter))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        if form.getvalue('memory') == '50':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_half)), shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_half))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('memory') == '75':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_threequarter)), shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_threequarter))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        elif form.getvalue('memory') == '100':
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(mymem), shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mymem))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUAccounting=yes', shell=True)
        subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOAccounting=yes', shell=True)
        subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryAccounting=yes', shell=True)
        subprocess.call('/usr/bin/systemctl daemon-reload', shell=True)
        if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
            with open(os.devnull, 'w') as FNULL:
                subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl daemon-reload"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        for backend_name in list(php_backends_dict.keys()):
            myservice = backend_name+'@'+form.getvalue('unit')+".service"
            if form.getvalue('cpu') == '25':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=256', shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=256"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            if form.getvalue('cpu') == '50':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=512', shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=512"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            elif form.getvalue('cpu') == '75':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=768', shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=768"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            elif form.getvalue('cpu') == '100':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=1024', shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUShares=1024"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            if form.getvalue('blockio') == '25':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=250', shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=250"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            if form.getvalue('blockio') == '50':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=500', shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=500"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            elif form.getvalue('blockio') == '75':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=750', shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=750"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            elif form.getvalue('blockio') == '100':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=1000', shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=1000"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            mymem = psutil.virtual_memory().total
            mem_quarter = float(mymem) * 0.25
            mem_threequarter = float(mymem) * 0.75
            mem_half = float(mymem) / 2.0
            if form.getvalue('memory') == '25':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_quarter)), shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_quarter))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            if form.getvalue('memory') == '50':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_half)), shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_half))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            elif form.getvalue('memory') == '75':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_threequarter)), shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mem_threequarter))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            elif form.getvalue('memory') == '100':
                subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(mymem), shell=True)
                if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                    with open(os.devnull, 'w') as FNULL:
                        subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+str(int(mymem))+'"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUAccounting=yes', shell=True)
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOAccounting=yes', shell=True)
            subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryAccounting=yes', shell=True)
            subprocess.call('/usr/bin/systemctl daemon-reload', shell=True)
            if os.path.isfile('/opt/nDeploy/conf/ndeploy_cluster.yaml'):
                with open(os.devnull, 'w') as FNULL:
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' CPUAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' BlockIOAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl set-property '+myservice+' MemoryAccounting=yes"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
                    subprocess.Popen('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "/usr/bin/systemctl daemon-reload"', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    commoninclude.print_success('Resource limits saved')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
