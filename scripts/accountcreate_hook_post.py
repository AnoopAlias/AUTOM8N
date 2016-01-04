#!/usr/bin/env python


import yaml
import sys
import json
import cuisine
import subprocess


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
cpaneluserhome = mydict["homedir"]
cpaneldomain = mydict["domain"]
cpdomainyaml = "/var/cpanel/userdata/" + cpaneluser + "/" + cpaneldomain
cpaneldomain_data_stream = open(cpdomainyaml, 'r')
yaml_parsed_cpaneldomain = yaml.safe_load(cpaneldomain_data_stream)
cpanel_ipv4 = yaml_parsed_cpaneldomain.get('ip')
for server in serverlist:
    connect_server_dict = cluster_data_yaml_parsed.get(server)
    connect_ip = connect_server_dict.get("connect")
    cuisine.connect(connect_ip)
    cuisine.user_create_linux(cpaneluser, home=cpaneluserhome)
    ipmap_dict = connect_server_dict.get("ipmap")
    remote_domain_ip = ipmap_dict.get(cpanel_ipv4)
    subprocess.call(installation_path+"/scripts/cluster_dns_setup.pl add "+cpaneldomain+" "+remote_domain_ip, shell=True)
print("1 nDeploy:clusteraccountcreate:"+cpaneluser)
