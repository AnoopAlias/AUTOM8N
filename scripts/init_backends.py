#!/usr/bin/env python


import yaml
import argparse
import subprocess
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
php_fpm_config = installation_path+"/conf/php-fpm.conf"


# Function defs


def control_php_fpm(trigger):
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        if trigger == "start":
            subprocess.call("sysctl -q -w net.core.somaxconn=4096", shell=True)
            for path in list(php_backends_dict.values()):
                php_fpm_bin = path+"/sbin/php-fpm"
                php_fpm_conf_d = path+"/etc/fpm.d"
                if not os.path.exists(php_fpm_conf_d):
                    os.mkdir(php_fpm_conf_d)
                    t_file = installation_path+"/conf/php-fpm.pool.tmpl"
                    o_file = php_fpm_conf_d+"/nobody.conf"
                    sed_string = 'sed "s/CPANELUSER/nobody/g" '
                    subprocess.call(sed_string+t_file+' > '+o_file, shell=True)
                subprocess.call(php_fpm_bin+" --fpm-config "+php_fpm_config, shell=True)
        elif trigger == "stop":
            for path in list(php_backends_dict.values()):
                php_fpm_pid = path+"/var/run/php-fpm.pid"
                subprocess.call("kill -9 $(cat "+php_fpm_pid+")", shell=True)
        else:
            return


backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()


parser = argparse.ArgumentParser(description="Start/Stop various nDeploy backends")
parser.add_argument("control_command")
args = parser.parse_args()
trigger = args.control_command
control_php_fpm(trigger)
