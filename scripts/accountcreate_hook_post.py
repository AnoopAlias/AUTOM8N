#!/usr/bin/env python


import yaml
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
    cluster_data_yaml = open(cluster_config_file, 'r')
    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    cluster_data_yaml.close()
    serverlist = cluster_data_yaml_parsed.keys()
    cpaneluserhome = mydict["homedir"]
    cpaneldomain = mydict["domain"]
    cpdomainyaml = "/var/cpanel/userdata/" + cpaneluser + "/" + cpaneldomain
    cpaneldomain_data_stream = open(cpdomainyaml, 'r')
    yaml_parsed_cpaneldomain = yaml.safe_load(cpaneldomain_data_stream)
    cpanel_ipv4 = yaml_parsed_cpaneldomain.get('ip')
    subprocess.call('ansible ndeploycluster -m user -a "name='+cpaneluser+' home='+cpaneluserhome+'"', shell=True)
    for server in serverlist:
        connect_server_dict = cluster_data_yaml_parsed.get(server)
        ipmap_dict = connect_server_dict.get("ipmap")
        remote_domain_ip = ipmap_dict.get(cpanel_ipv4)
        subprocess.call(installation_path+"/scripts/cluster_dns_setup.pl add "+cpaneldomain+" "+remote_domain_ip, shell=True)
    print("1 nDeploy:clusteraccountcreate:"+cpaneluser)
else:
    subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
    print("1 nDeploy:accountcreate:"+cpaneluser)
