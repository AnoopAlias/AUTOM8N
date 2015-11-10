#!/usr/bin/env python

import subprocess
import yaml
import argparse
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"

# Function defs
def update_apache_backend(user_name, backend_category, backend_name):
	userdata_file = installation_path+"/user-data/"+user_name
	backend_data_yaml_parsed = {backend_category: backend_name}
	with open(userdata_file,'w')as yaml_file:
		yaml_file.write(yaml.dump(backend_data_yaml_parsed, default_flow_style=False))
	yaml_file.close()

def remove_old_phpfpm_pool(user_name):
    """Remove old php-fpm pool """
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        for php_path in list(php_backends_dict.values()):
            phppool_link = php_path + "/etc/php-fpm.d/" + user_name + ".conf"
            if os.path.islink(phppool_link):
                os.remove(phppool_link)
    if os.path.islink("/opt/fpmsockets/"+user_name+".sock"):
        os.remove("/opt/fpmsockets/"+user_name+".sock")
    return

parser = argparse.ArgumentParser(description="Switch a apache php-fpm version")
parser.add_argument("CPANELUSER")
parser.add_argument("backend_category")
parser.add_argument("backend_name")
args = parser.parse_args()

update_apache_backend(args.CPANELUSER, args.backend_category, args.backend_name)
remove_old_phpfpm_pool(args.CPANELUSER)
subprocess.call(installation_path+"/scripts/apache_php_config_generator.py "+args.CPANELUSER, shell=True)