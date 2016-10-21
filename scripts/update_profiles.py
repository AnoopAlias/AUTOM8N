#!/usr/bin/env python


import yaml
import argparse
import os
import sys

__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


# Function defs


def update_profile(action, user, scope, backend_category, file_name, profile_description):
    if user == 'root':
        if scope == 'main':
            profile_config_file = installation_path+"/conf/apptemplates.yaml"
        elif scope == 'subdir':
            profile_config_file = installation_path+"/conf/apptemplates_subdir.yaml"
        else:
            print("scope must be main / subdir")
            sys.exit(1)
    else:
        if scope == 'main':
            profile_config_file = installation_path+"/conf/"+user+"_apptemplates.yaml"
        elif scope == 'subdir':
            profile_config_file = installation_path+"/conf/"+user+"_apptemplates_subdir.yaml"
        else:
            print("scope must be main / subdir")
            sys.exit(1)
    if not os.path.isfile(profile_config_file):
        open(profile_config_file, 'a').close()
    with open(profile_config_file, 'r') as profile_data_yaml:
        profile_data_yaml_parsed = yaml.safe_load(profile_data_yaml)
    if profile_data_yaml_parsed:
        if backend_category in profile_data_yaml_parsed:
            branch_dict = profile_data_yaml_parsed[backend_category]
            if action == 'add':
                branch_dict[file_name] = profile_description
            elif action == 'del':
                try:
                    del branch_dict[file_name]
                except KeyError:
                    pass
            with open(profile_config_file, 'w') as yaml_file:
                yaml_file.write(yaml.dump(profile_data_yaml_parsed, default_flow_style=False))
        else:
            profile_data_yaml_parsed[backend_category] = {file_name: profile_description}
            with open(profile_config_file, 'w') as yaml_file:
                yaml_file.write(yaml.dump(profile_data_yaml_parsed, default_flow_style=False))
    else:
        data_dict = {backend_category: {file_name: profile_description}}
        with open(profile_config_file, 'w')as yaml_file:
            yaml_file.write(yaml.dump(data_dict, default_flow_style=False))


parser = argparse.ArgumentParser(description="Register an nginX config profile for nDeploy")
parser.add_argument("action")
parser.add_argument("user")
parser.add_argument("scope")
parser.add_argument("backend_category")
parser.add_argument("file_name")
parser.add_argument("application_description_in_doublequotes")
args = parser.parse_args()
action = args.action
user = args.user
scope = args.scope
b_cat = args.backend_category
f_code = args.file_name
p_desc = args.application_description_in_doublequotes
update_profile(action, user, scope, b_cat, f_code, p_desc)
