#!/usr/bin/env python


import yaml
import argparse
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"


# Function defs


def update_backend(action, backend_category, backend_name, backend_path):
    if not os.path.isfile(backend_config_file):
        open(backend_config_file, 'a').close()
    with open(backend_config_file, 'r') as backend_data_yaml:
        backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    if backend_data_yaml_parsed:
        if backend_category in backend_data_yaml_parsed:
            branch_dict = backend_data_yaml_parsed[backend_category]
            if action == 'add':
                branch_dict[backend_name] = backend_path
            elif action == 'del':
                try:
                    del branch_dict[backend_name]
                except KeyError:
                    pass
            with open(backend_config_file, 'w')as yaml_file:
                yaml_file.write(yaml.dump(backend_data_yaml_parsed, default_flow_style=False))
            yaml_file.close()
        else:
            backend_data_yaml_parsed[backend_category] = {backend_name: backend_path}
            with open(backend_config_file, 'w')as yaml_file:
                yaml_file.write(yaml.dump(backend_data_yaml_parsed, default_flow_style=False))
            yaml_file.close()
    else:
        data_dict = {backend_category: {backend_name: backend_path}}
        with open(backend_config_file, 'w')as yaml_file:
            yaml_file.write(yaml.dump(data_dict, default_flow_style=False))
        yaml_file.close()


parser = argparse.ArgumentParser(description="Register a proxy/application backend for nDeploy")
parser.add_argument("action")
parser.add_argument("backend_category")
parser.add_argument("backend_name")
parser.add_argument("backend_path")
args = parser.parse_args()
action = args.action
b_cat = args.backend_category
b_name = args.backend_name
b_path = args.backend_path
update_backend(action, b_cat, b_name, b_path)
