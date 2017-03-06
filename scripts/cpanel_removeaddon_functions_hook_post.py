#!/usr/bin/env python


import sys
import json
import subprocess
import os
import shutil
import yaml

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_dir = "/etc/nginx/sites-enabled/"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
hook_output = mydict["output"]
hook_output_dict = hook_output[0]
status = hook_output_dict["result"]
if status == 1:
    hookargs = mydict["args"]
    hookargs_subdomain = hookargs["subdomain"]
    conf_sub_domain = hookargs_subdomain.replace("_", ".", 1)
    silentremove(installation_path+"/domain-data/"+conf_sub_domain)
    silentremove(nginx_dir+conf_sub_domain+".conf")
    silentremove(nginx_dir+conf_sub_domain+".include")
    if os.path.isfile(cluster_config_file):
        with open(cluster_config_file, 'r') as cluster_data_yaml:
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
        for server in cluster_data_yaml_parsed.keys():
            silentremove("/etc/nginx/"+server+"/"+conf_sub_domain+".conf")
            silentremove("/etc/nginx/"+server+"/"+conf_sub_domain+".include")
    if os.path.exists('/var/resin/hosts/'+conf_sub_domain):
        shutil.rmtree('/var/resin/hosts/'+conf_sub_domain)
    subprocess.Popen("/usr/sbin/nginx -s reload", shell=True)
    print(("1 nDeploy:cPaneltrigger:RemoveAddon:"+conf_sub_domain))
else:
    print(("0 nDeploy:cPaneltrigger:SkipHook"))
