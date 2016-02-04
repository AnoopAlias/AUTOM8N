#!/usr/bin/env python


import yaml
import subprocess
import os
import sys


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_bin = "/usr/sbin/nginx"


# Function defs

def php_profile_set(user_name, php_path):
    """Function to setup php-fpm pool for user and reload the master php-fpm"""
    phppool_file = installation_path + "/php-fpm.d/" + user_name + ".conf"
    if not os.path.isfile(phppool_file):
        sed_string = 'sed "s/CPANELUSER/' + user_name + '/g" ' + installation_path + '/conf/php-fpm.pool.tmpl > ' + phppool_file
        subprocess.call(sed_string, shell=True)
        subprocess.call(installation_path+"/scripts/init_backends.py reload", shell=True)
        return
    else:
        return


def nginx_server_reload():
    """Function to reload nginX config"""
    subprocess.call(nginx_bin + " -s reload", shell=True)
    return


# End Function defs


if __name__ == "__main__":
    num_args = int(len(sys.argv))
    for arg_pos in range(1, num_args):
        if os.path.isfile(sys.argv[arg_pos]):
            profileyaml_data_stream = open(sys.argv[arg_pos], 'r')
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
            profileyaml_data_stream.close()
            profile_category = yaml_parsed_profileyaml.get('backend_category')
            if profile_category == "PHP":
                phpversion = yaml_parsed_profileyaml.get('backend_version')
                php_path = yaml_parsed_profileyaml.get('backend_path')
                user_name = yaml_parsed_profileyaml.get('user')
                php_profile_set(user_name, phpversion, php_path)
