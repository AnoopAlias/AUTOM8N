#!/usr/bin/env python


import sys
import os
import subprocess
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

# Get data send by cPanel on stdin
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
# new_shell = mydict["new_shell"]
# current_shell = mydict["current_shell"]
if os.path.isfile(installation_path+"/conf/chroot-php-enabled"):
    silentremove(installation_path + "/php-fpm.d/" + cpaneluser + ".conf")
    silentremove(installation_path + "/secure-php-fpm.d/" + cpaneluser + ".conf")
    subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)
print(("1 nDeploy:modifyshell:"+cpaneluser))
