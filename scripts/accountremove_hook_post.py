#!/usr/bin/env python


import yaml
import sys
import json
import cuisine


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
cluster_data_yaml = open(cluster_config_file, 'r')
cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
cluster_data_yaml.close()
serverlist = cluster_data_yaml_parsed.keys()
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
for server in serverlist:
    connect_server_dict = cluster_data_yaml_parsed.get(server)
    connect_ip = connect_server_dict.get("connect")
    cuisine.connect(connect_ip)
    cuisine.user_remove_linux(cpaneluser, rmhome=True)
    cuisine.run('if [ -f '+installation_path+'/php-fpm.d/'+cpaneluser+'.conf ] ;then rm -f '+installation_path+'/php-fpm.d/'+cpaneluser+'.conf ;fi')
    cuisine.run(installation_path+"/scripts/init_backends.py reload")
print("1 nDeploy:clusteraccountdelete:"+cpaneluser)
