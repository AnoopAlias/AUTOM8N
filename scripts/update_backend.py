#!/usr/bin/env python

import yaml
import argparse

installation_path = "/opt/nDeploy" #Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"

#Function defs
def update_backend(backend_category,backend_name,backend_path):
	backend_data_yaml = open(backend_config_file,'r')
	backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
	backend_data_yaml.close()
	if backend_data_yaml_parsed:
		if backend_data_yaml_parsed.has_key(backend_category):
			branch_dict = backend_data_yaml_parsed[backend_category]
			branch_dict[backend_name] = backend_path
			with open(backend_config_file,'w')as yaml_file:
				yaml_file.write(yaml.dump(backend_data_yaml_parsed , default_flow_style=False))
		else:
			backend_data_yaml_parsed[backend_category] = {backend_name : backend_path }
			with open(backend_config_file,'w')as yaml_file:
				yaml_file.write(yaml.dump(backend_data_yaml_parsed , default_flow_style=False))
	else:
		data_dict = {backend_category :{ backend_name  : backend_path }}
		with open(backend_config_file,'w')as yaml_file:
			yaml_file.write(yaml.dump(data_dict , default_flow_style=False))
	yaml_file.close()


parser = argparse.ArgumentParser(description = "Register a proxy/application backend for Xstack")
parser.add_argument("backend_category")
parser.add_argument("backend_name")
parser.add_argument("backend_path")
args = parser.parse_args()
b_cat = args.backend_category
b_name = args.backend_name
b_path = args.backend_path
update_backend(b_cat,b_name,b_path)
