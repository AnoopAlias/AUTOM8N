#!/usr/bin/env python


import sys
import subprocess
import os
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


# This hook script is supposed to be called after account creation by cPanel
installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
# Loading the json in on stdin send by cPanel
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
# If nDeploy cluster is enabled we need to add users,DNS entry for the same
if os.path.exists(cluster_config_file):
    cpaneluserhome = mydict["homedir"]
    cpaneldomain = mydict["domain"]
    # Calling ansible ad-hoc command to create users across the cluster
    # Using subprocess.call here as we are not in a hurry and no async call is required
    subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpaneluser+' home='+cpaneluserhome+'"', shell=True)
    subprocess.call(installation_path + "/scripts/cluster_dns_ensure_user.py "+cpaneluser, shell=True)
    subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
    print("1 nDeploy:clusteraccountcreate:"+cpaneluser)
else:
    # We just need to generate config for the local machine
    subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
    print("1 nDeploy:accountcreate:"+cpaneluser)
