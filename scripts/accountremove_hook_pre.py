#!/usr/bin/env python


import sys
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


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]

# we copy the associated  userdata file for the user for post hook stage
with open("/var/cpanel/userdata/" + cpaneluser + "/main.cache", 'r') as userdata:
    userdata_json = json.load(userdata)
with open(installation_path+"/lock/"+cpaneluser+".userdata", 'w') as tempuserdata:
    json.dump(userdata_json, tempuserdata)
print(("1 nDeploy:remove:pre:"+cpaneluser))
