#!/usr/bin/env python


import sys
import json
import subprocess
import os
import shutil

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
theaddon = mydict["domain"]
conversionstatus = mydict["status"]

if conversionstatus == 1:
    # we find the associated subdomain from /etc/userdatadomains.json copied in pre script
    with open(installation_path+"/lock/"+theaddon, 'r') as userdatadomains:
        userdatadom = json.load(userdatadomains)
    addondata = userdatadom.get(theaddon)
    addonconfigdom = addondata[3]
    silentremove(installation_path+"/domain-data/"+addonconfigdom)
    silentremove(nginx_dir+addonconfigdom+".conf")
    silentremove(nginx_dir+addonconfigdom+".include")
    silentremove(nginx_dir+addonconfigdom+".nxapi.wl")
    if os.path.isfile(installation_path+"/conf/ndeploy_cluster_slaves"):
        with open(installation_path+"/conf/ndeploy_cluster_slaves") as cluster_slave_list:
            for server in cluster_slave_list:
                silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+addonconfigdom+".conf")
                silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+addonconfigdom+".include")
                silentremove("/etc/nginx/"+server.replace('\n', '')+"/"+addonconfigdom+".nxapi.wl")
    if os.path.exists('/var/resin/hosts/'+addonconfigdom):
        shutil.rmtree('/var/resin/hosts/'+addonconfigdom)
    subprocess.Popen("/usr/sbin/nginx -s reload", shell=True)
    silentremove(installation_path+"/lock/"+theaddon)
    print(("1 nDeploy:cPaneltrigger:ConevrtAddon:"+addonconfigdom))
else:
    silentremove(installation_path+"/lock/"+theaddon)
    print(("0 nDeploy:SkipHook:ConevrtAddon:"+addonconfigdom))
