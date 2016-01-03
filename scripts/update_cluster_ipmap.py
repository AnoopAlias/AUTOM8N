#!/usr/bin/env python


import yaml
import argparse
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"


# Function defs


def update_ip_map(server, iphere, ipthere):
    cluster_data_yaml = open(cluster_config_file, 'r')
    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    cluster_data_yaml.close()
    if cluster_data_yaml_parsed:
        if server in cluster_data_yaml_parsed.keys():
            connect_server_dict = cluster_data_yaml_parsed.get(server)
            ipmap_dict = connect_server_dict.get("ipmap")
            ipmap_dict[iphere] = ipthere
            with open(cluster_config_file, 'w') as yaml_file:
                yaml_file.write(yaml.dump(cluster_data_yaml_parsed, default_flow_style=False))
            yaml_file.close()
        else:
            print(server+" is not present in the cluster")
    else:
        print("Invalid cluster data")

parser = argparse.ArgumentParser(description="Register an nginX config profile for nDeploy")
parser.add_argument("slave_hostname")
parser.add_argument("ip_here")
parser.add_argument("remote_ip")
args = parser.parse_args()
server_key = args.slave_hostname
ip_here = args.ip_here
remote_ip = args.remote_ip
if os.path.isfile(cluster_config_file):
    update_ip_map(server_key, ip_here, remote_ip)
else:
    print("nDeploy cluster is not setup")
