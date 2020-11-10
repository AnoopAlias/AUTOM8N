#!/usr/bin/env python3


import sys
import os
import subprocess
import pwd
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

# Get data send by cPanel on stdin
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
user_shell = pwd.getpwnam(cpaneluser).pw_shell
# new_shell = mydict["new_shell"]
# current_shell = mydict["current_shell"]
if os.path.exists(cluster_config_file):
    # Calling ansible ad-hoc command to modify users across the cluster
    # Using subprocess.call here as we are not in a hurry and no async call is required
    subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpaneluser+' home='+cpaneluserhome+' shell='+user_shell+'"', shell=True)
print(("1 nDeploy:clustermodifyshell:"+cpaneluser))
