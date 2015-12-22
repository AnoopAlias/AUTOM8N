#!/usr/bin/env python


import yaml
import argparse
import subprocess
import os
import signal
import time
import pwd


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
            conf_list = os.listdir("/opt/nDeploy/php-fpm.d")
            for filename in conf_list:
                user, extension = filename.split('.')
                try:
                    pwd.getpwnam(user)
                except KeyError:
                    os.remove("/opt/nDeploy/php-fpm.d/"+filename)
                else:
                    pass
            subprocess.call("sysctl -q -w net.core.somaxconn=4096", shell=True)
            subprocess.call("sysctl -q -w vm.max_map_count=131070", shell=True)
            for path in list(php_backends_dict.values()):
                if os.path.isfile(path+"/sbin/php-fpm"):
                    php_fpm_bin = path+"/sbin/php-fpm"
                else:
                    php_fpm_bin = path+"/usr/sbin/php-fpm"
                subprocess.call(php_fpm_bin+" --prefix "+path+" --fpm-config "+php_fpm_config, shell=True)
        elif trigger == "stop":
            for path in list(php_backends_dict.values()):
                php_fpm_pid = path+"/var/run/php-fpm.pid"
                if os.path.isfile(php_fpm_pid):
                    with open(php_fpm_pid) as f:
                        mypid = f.read()
                    f.close()
                    try:
                        os.kill(int(mypid), signal.SIGQUIT)
                        time.sleep(3)  # Give enough time for all child process to exit
                    except OSError:
                        break
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
