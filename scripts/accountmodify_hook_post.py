#!/usr/bin/env python

import os
import sys
import subprocess
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


# This script is supposed to be called by cPanel after an account is modified
# All we need to do is call config generator with the new username as arg
installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
nginx_dir = "/etc/nginx/sites-enabled/"

# Get the values send by cPanel in stdin
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
# Assuming someone changed the cPanel username
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]
# Calling the config generate script for the user
if cpanelnewuser != cpaneluser:
    subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
    if os.path.exists(cluster_config_file):
        cpaneluserhome = mydict["homedir"]
        # Calling ansible ad-hoc command to remove / create users across the cluster
        # Using subprocess.call here as no async call is required
        subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpaneluser+' state=absent remove=yes"', shell=True)
        # Create the new user
        subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpanelnewuser+' home='+cpaneluserhome+'"', shell=True)
        subprocess.call(installation_path + "/scripts/cluster_dns_ensure_user.py "+cpanelnewuser, shell=True)
        subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
    print(("1 nDeploy:postmodify:"+cpanelnewuser))
else:
    subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)
    print(("1 nDeploy:postmodify:"+cpaneluser))
