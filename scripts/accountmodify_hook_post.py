#!/usr/bin/env python


import yaml
import sys
import json
import os
import signal
import time
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
nginx_dir = "/etc/nginx/sites-enabled/"


# Function defs
def remove_php_fpm_pool(user_name):
    """Remove the php-fpm pools of deleted accounts"""
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        for php_path in list(php_backends_dict.values()):
            phppool_file = installation_path + "/php-fpm.d/" + user_name + ".conf"
            php_fpm_config = installation_path+"/conf/php-fpm.conf"
            if os.path.isfile(php_path+"/sbin/php-fpm"):
                php_fpm_bin = php_path+"/sbin/php-fpm"
            else:
                php_fpm_bin = php_path+"/usr/sbin/php-fpm"
            if os.path.isfile(phppool_file):
                os.remove(phppool_file)
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
                        subprocess.call(php_fpm_bin+" --fpm-config "+php_fpm_config, shell=True)
                    try:
                        os.kill(int(newpid), 0)
                    except OSError:
                        subprocess.call(php_fpm_bin+" --fpm-config "+php_fpm_config, shell=True)
                    else:
                        return True
            else:
                subprocess.call(php_fpm_bin+" --fpm-config "+php_fpm_config, shell=True)
    return

cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpanelnewuser = mydict["newuser"]
cpaneluser = mydict["user"]
maindomain = mydict["domain"]
if os.path.isfile(installation_path+"/lock/todel_"+cpaneluser):
    fhandle = open(installation_path+"/lock/todel_"+cpaneluser,'r')
    mylines = fhandle.read().splitlines()
    for line in mylines:
        try:
            os.remove(line)
        except OSError:
            pass
    fhandle.close()
    os.remove(installation_path+"/lock/todel_"+cpaneluser)
if cpaneluser != cpanelnewuser:
    remove_php_fpm_pool(cpaneluser)
subprocess.call("/usr/sbin/nginx -s reload", shell=True)
subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpanelnewuser, shell=True)
subprocess.call("/opt/nDeploy/scripts/apache_php_config_generator.py "+cpanelnewuser, shell=True)
print(("1 nDeploy:postmodify:"+cpanelnewuser))
