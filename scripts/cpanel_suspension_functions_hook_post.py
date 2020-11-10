#!/usr/bin/env python3


import sys
import json
import subprocess
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
print(("1 nDeploy:cPaneltrigger::Suspension:"+cpaneluser))
