#!/usr/bin/env python


import yaml
import subprocess
import os
import signal
import time
import sys


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_bin = "/usr/sbin/nginx"


# Function defs



def nginx_server_reload():
    """Function to reload nginX config"""
    subprocess.call(nginx_bin + " -s reload", shell=True)
    return


def php_profile_set(user_name, phpversion, php_path):
    """Function to setup php-fpm pool for user and restart the master php-fpm"""
    phppool_file = installation_path + "/php-fpm.d/" + user_name + ".conf"
    php_fpm_config = installation_path+"/conf/php-fpm.conf"
    if os.path.isfile(php_path+"/sbin/php-fpm"):
        php_fpm_bin = php_path + "/sbin/php-fpm"
    else:
        php_fpm_bin = php_path + "/usr/sbin/php-fpm"
    if os.path.isfile(phppool_file):
        if os.path.isfile(php_path + "/var/run/php-fpm.pid"):
            with open(php_path + "/var/run/php-fpm.pid") as f:
                mypid = f.read()
            f.close()
            os.kill(int(mypid), signal.SIGUSR2)
            time.sleep(3)
            try:
                with open(php_path + "/var/run/php-fpm.pid") as f:
                    newpid = f.read()
                f.close()
            except IOError:
                subprocess.call(php_fpm_bin+" --prefix "+php_path+" --fpm-config "+php_fpm_config, shell=True)
            try:
                os.kill(int(newpid), 0)
            except OSError:
                subprocess.call(php_fpm_bin+" --prefix "+php_path+" --fpm-config "+php_fpm_config, shell=True)
            else:
                return True
        else:
            subprocess.call(php_fpm_bin+" --prefix "+php_path+" --fpm-config "+php_fpm_config, shell=True)
    else:
        sed_string = 'sed "s/CPANELUSER/' + user_name + '/g" ' + installation_path + '/conf/php-fpm.pool.tmpl > ' + phppool_file
        subprocess.call(sed_string, shell=True)
        if os.path.isfile(php_path + "/var/run/php-fpm.pid"):
            with open(php_path + "/var/run/php-fpm.pid") as f:
                mypid = f.read()
            f.close()
            try:
                os.kill(int(mypid), signal.SIGUSR2)
            except OSError:
                subprocess.call(php_fpm_bin+" --prefix "+php_path+" --fpm-config "+php_fpm_config, shell=True)
            time.sleep(3)
            try:
                with open(php_path + "/var/run/php-fpm.pid") as f:
                    newpid = f.read()
                f.close()
            except IOError:
                subprocess.call(php_fpm_bin+" --prefix "+php_path+" --fpm-config "+php_fpm_config, shell=True)
            try:
                os.kill(int(newpid), 0)
            except OSError:
                subprocess.call(php_fpm_bin+" --prefix "+php_path+" --fpm-config "+php_fpm_config, shell=True)
            else:
                return True
        else:
            subprocess.call(php_fpm_bin+" --prefix "+php_path+" --fpm-config "+php_fpm_config, shell=True)


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
