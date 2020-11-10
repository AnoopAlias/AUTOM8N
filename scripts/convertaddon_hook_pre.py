#!/usr/bin/env python3


import sys
import json

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
theaddon = mydict["domain"]

# we copy the associated subdomain data from /etc/userdatadomains.json
with open('/etc/userdatadomains.json', 'r') as userdatadomains:
    userdatadom = json.load(userdatadomains)
addondata = userdatadom.get(theaddon)
theaddon_dict = {theaddon: addondata}
with open(installation_path+"/lock/"+theaddon, 'w') as tempuserdata:
    json.dump(theaddon_dict, tempuserdata)
