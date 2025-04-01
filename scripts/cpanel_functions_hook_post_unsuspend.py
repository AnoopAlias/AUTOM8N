#!/usr/bin/env python3


import sys
import json
import subprocess
import os
from commoninclude import sighupnginx


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
hook_args = mydict["args"]
cpaneluser = hook_args["user"]
subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)  # Assuming escalateprivilege is enabled
sighupnginx()
if os.path.exists(cluster_config_file):
    subprocess.call("systemctl restart maxscale", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeploymaster -m shell -a "systemctl restart maxscale"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print(("1 nDeploy:cPaneltrigger:"+cpaneluser))
