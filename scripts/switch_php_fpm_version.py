#!/usr/bin/env python

import subprocess
import yaml
import argparse


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

# Function defs
def update_apache_backend(user_name, backend_category, backend_name):
	userdata_file = installation_path+"/user-data/"+user_name
	backend_data_yaml_parsed = {backend_category: backend_name}
	with open(userdata_file,'w')as yaml_file:
		yaml_file.write(yaml.dump(backend_data_yaml_parsed, default_flow_style=False))
	yaml_file.close()


parser = argparse.ArgumentParser(description="Switch a apache php-fpm version")
parser.add_argument("CPANELUSER")
parser.add_argument("backend_category")
parser.add_argument("backend_name")
args = parser.parse_args()

update_apache_backend(args.CPANELUSER, args.backend_category, args.backend_name)
subprocess.call(installation_path+"/scripts/apache_php_config_generator.py "+args.CPANELUSER, shell=True)