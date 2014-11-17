#!/usr/bin/env python


import yaml
import argparse


installation_path = "/opt/nDeploy" #Absolute Installation Path
profile_config_file = installation_path+"/conf/profiles.yaml"


#Function defs


def update_profile(backend_category, profile_code, profile_description):
    profile_data_yaml = open(profile_config_file,'r')
    profile_data_yaml_parsed = yaml.safe_load(profile_data_yaml)
    profile_data_yaml.close()
    if profile_data_yaml_parsed:
	if backend_category in profile_data_yaml_parsed:
	    branch_dict = profile_data_yaml_parsed[backend_category]
	    branch_dict[profile_code] = profile_description
	    with open(profile_config_file, 'w') as yaml_file:
		yaml_file.write(yaml.dump(profile_data_yaml_parsed, default_flow_style=False))
            yaml_file.close()
	else:
	    profile_data_yaml_parsed[backend_category] = {profile_code : profile_description }
	    with open(profile_config_file, 'w') as yaml_file:
		yaml_file.write(yaml.dump(profile_data_yaml_parsed , default_flow_style=False))
            yaml_file.close()
    else:
        data_dict = {backend_category :{ profile_code  : profile_description }}
	with open(profile_config_file,'w')as yaml_file:
	    yaml_file.write(yaml.dump(data_dict , default_flow_style=False))
	yaml_file.close()


parser = argparse.ArgumentParser(description = "Register an nginX config profile for nDeploy")
parser.add_argument("backend_category")
parser.add_argument("profile_code")
parser.add_argument("profile_description_in_doublequotes")
args = parser.parse_args()
b_cat = args.backend_category
p_code = args.profile_code
p_desc = args.profile_description_in_doublequotes
update_profile(b_cat,p_code,p_desc)
