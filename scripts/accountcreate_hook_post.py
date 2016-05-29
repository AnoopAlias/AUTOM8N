#!/usr/bin/env python


import sys
import json
import subprocess
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
if os.path.exists(cluster_config_file):
    cpaneluserhome = mydict["homedir"]
    cpaneldomain = mydict["domain"]
    subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpaneluser+' home='+cpaneluserhome+'"', shell=True)
    subprocess.call(installation_path + "/scripts/cluster_dns_ensure_user.py "+cpaneluser, shell=True)
    subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
    subprocess.call(installation_path+"/scripts/apache_php_config_generator.py "+cpaneluser, shell=True)
    print("1 nDeploy:clusteraccountcreate:"+cpaneluser)
else:
    subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
    subprocess.call(installation_path+"/scripts/apache_php_config_generator.py "+cpaneluser, shell=True)
    print("1 nDeploy:accountcreate:"+cpaneluser)
