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
if "web_vhost_name" in mydict:
    domainname = mydict["web_vhost_name"]
else:
    domainname = mydict["domain_set_name"]
with open("/etc/userdatadomains.json", "r") as userdatadomains:
    json_parsed_userdata = json.load(userdatadomains)
cpaneluserdata = json_parsed_userdata.get(domainname)
cpaneluser = cpaneluserdata[0]

subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)
sighupnginx()
print(("1 nDeploy:WHMTLSAutoSSLtrigger:"+cpaneluser))
