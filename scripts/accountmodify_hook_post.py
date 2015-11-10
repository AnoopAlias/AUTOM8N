#!/usr/bin/env python


import yaml
import sys
import json
import os
import signal
import time
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
nginx_dir = "/etc/nginx/sites-enabled/"


# Function defs
def remove_php_fpm_pool(user_name):
    """Remove the php-fpm pools of deleted accounts"""
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        for php_path in list(php_backends_dict.values()):
            phppool_file = php_path + "/etc/php-fpm.d/" + user_name + ".conf"
            if os.path.islink(phppool_file):
                os.remove(phppool_file)
    os.remove("/opt/fpmsockets/"+user_name+".sock")
    return



cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]
if os.path.isfile(installation_path+"/lock/todel_"+cpaneluser):
    fhandle = open(installation_path+"/lock/todel_"+cpaneluser,'r')
    mylines = fhandle.read().splitlines()
    for line in mylines:
        os.remove(line)
    fhandle.close()
    os.remove(installation_path+"/lock/todel_"+cpaneluser)
if cpaneluser != cpanelnewuser:    
    remove_php_fpm_pool(cpaneluser)
subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
subprocess.call("/opt/nDeploy/scripts/apache_php_config_generator.py "+cpanelnewuser, shell=True)
subprocess.call("/opt/nDeploy/scripts/init_backends.pl --action=reload", shell=True)
subprocess.call("/opt/nDeploy/scripts/reload_nginx.sh", shell=True)
print(("1 nDeploy:postmodify:"+cpanelnewuser))
