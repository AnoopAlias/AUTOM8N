#!/usr/bin/env python


import sys
import subprocess
import os
try:
    import simplejson as json
except ImportError:
    import json
from commoninclude import sighupnginx


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

#  Run hook only if I am root
if os.getuid() == 0:
    # If nDeploy cluster is enabled we need to add users,DNS entry for the same
    if os.path.exists(cluster_config_file):
        if os.path.isfile(installation_path+"/conf/skip_geodns"):
            subprocess.call(installation_path + "/scripts/cluster_dns_ensure_user.py "+cpaneluser, shell=True)
        else:
            subprocess.call(installation_path + "/scripts/cluster_gdnsd_ensure_user.py "+cpaneluser, shell=True)
        subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
        sighupnginx()
        print("1 nDeploy:clusteraccountrestore:"+cpaneluser)
    else:
        # We just need to generate config for the local machine
        subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
        sighupnginx()
        print("1 nDeploy:accountrestore:"+cpaneluser)
else:
    print("1 nDeploy:accountrestore:NoPrivilege:Restore"+cpaneluser)
