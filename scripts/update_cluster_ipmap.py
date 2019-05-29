#!/usr/bin/env python


import yaml
import argparse
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


parser = argparse.ArgumentParser(description="create/update nDeploy-cluster mapfile")
parser.add_argument("mapfile")
parser.add_argument("hostname")
parser.add_argument("selector")
parser.add_argument("key")
parser.add_argument("value")
args = parser.parse_args()
mapfile = args.mapfile
hostname = args.hostname
selector = args.selector
key = args.key
value = args.value
cluster_config_file = installation_path+"/conf/"+mapfile+".yaml"
if os.path.isfile(cluster_config_file):
    cluster_data_yaml = open(cluster_config_file, 'r')
    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    cluster_data_yaml.close()
    if cluster_data_yaml_parsed:
        if hostname in cluster_data_yaml_parsed.keys():
            connect_server_dict = cluster_data_yaml_parsed.get(hostname)
            if selector == 'ipmap':
                if 'ipmap' in connect_server_dict:
                    ipmap_dict = connect_server_dict.get("ipmap")
                    ipmap_dict[key] = value
                else:
                    connect_server_dict['ipmap'] = {key: value}
            elif selector == 'dnsmap':
                if 'dnsmap' in connect_server_dict:
                    dnsmap_dict = connect_server_dict.get("dnsmap")
                    dnsmap_dict[key] = value
                else:
                    connect_server_dict['dnsmap'] = {key: value}
            elif selector == 'mainip':
                    connect_server_dict['mainip'] = key
            with open(cluster_config_file, 'w') as yaml_file:
                yaml_file.write(yaml.dump(cluster_data_yaml_parsed, default_flow_style=False))
        else:
            if selector == 'ipmap':
                mydict = {hostname: {'ipmap': {key: value}}}
            elif selector == 'dnsmap':
                mydict = {hostname: {'dnsmap': {key: value}}}
            elif selector == 'mainip':
                mydict = {hostname: {'mainip': key}}
            cluster_data_yaml_parsed.update(mydict)
            with open(cluster_config_file, 'w') as yaml_file:
                yaml_file.write(yaml.dump(cluster_data_yaml_parsed, default_flow_style=False))
    else:
        print("Invalid cluster data")
else:
    if selector == 'ipmap':
        mydict = {hostname: {'ipmap': {key: value}}}
    elif selector == 'dnsmap':
        mydict = {hostname: {'dnsmap': {key: value}}}
    elif selector == 'mainip':
        mydict = {hostname: {'mainip': key}}
    with open(cluster_config_file, 'w') as cluster_conf:
        cluster_conf.write(yaml.dump(mydict, default_flow_style=False))
