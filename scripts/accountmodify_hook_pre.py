#!/usr/bin/env python


import sys
import os
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


# This hook script is called by cPanel before an account is modified
# We are intrested in username and main-domain name modifications
installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

# Get data send by cPanel on stdin
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]

if cpanelnewuser != cpaneluser:
    # we copy the associated  userdata file for the user for post hook stage
    with open("/var/cpanel/userdata/" + cpaneluser + "/main.cache", 'r') as userdata:
        userdata_json = json.load(userdata)
    # remove any stale userdata tmp files
    silentremove(installation_path+"/lock/"+cpaneluser+".userdata")
    with open(installation_path+"/lock/"+cpaneluser+".userdata", 'w') as tempuserdata:
        json.dump(userdata_json, tempuserdata)
print(("1 nDeploy:modify:pre:"+cpaneluser))
