#!/usr/bin/env python


import yaml
import argparse
import subprocess
import os


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"


# Function defs


def remove_php_fpm_pool(user_name):
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        for php_path in list(php_backends_dict.values()):
            phppool_file = php_path + "/etc/fpm.d/" + user_name + ".conf"
            if os.path.isfile(phppool_file):
                os.remove(phppool_file)
                subprocess.call("kill -USR2 `cat " + php_path + "/var/run/php-fpm.pid`", shell=True)
    return


parser = argparse.ArgumentParser(description="Remove various backend files on account termination")
parser.add_argument("username")
args = parser.parse_args()
user_name = args.username
remove_php_fpm_pool(user_name)
