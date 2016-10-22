#!/usr/bin/env python


import sys
import json
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
nginx_dir = "/etc/nginx/sites-enabled/"


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]
subprocess.call("/usr/sbin/nginx -s reload")
subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
print(("1 nDeploy:postmodify:"+cpanelnewuser))
