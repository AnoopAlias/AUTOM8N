#!/usr/bin/env python

import httplib
import re
import subprocess
import os
import platform
import yaml
import psutil


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
php_secure_mode_file = installation_path+"/conf/secure-php-enabled"
backend_config_file = installation_path+"/conf/backends.yaml"


def is_page_available(host, path="/pingphpfpm"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        False.
    """
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        if re.match("^[23]\d\d$", str(conn.getresponse().status)):
            return True
    except StandardError:
        return None


if __name__ == "__main__":
    if not os.path.isfile(php_secure_mode_file):
        backend_data_yaml = open(backend_config_file, 'r')
        backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        backend_data_yaml.close()
        if "PHP" in backend_data_yaml_parsed:
            installed_php_count = len(backend_data_yaml_parsed["PHP"].keys())
        else:
            installed_php_count = 0

        running_process_count = 0
        for myprocess in psutil.process_iter():
            # Workaround for Python 2.6
            if platform.python_version().startswith('2.6'):
                myexe = myprocess.cmdline
            else:
                myexe = myprocess.cmdline()
            if 'php-fpm: master process (/opt/nDeploy/conf/php-fpm.conf)' in myexe:
                running_process_count = running_process_count + 1
        if running_process_count == installed_php_count:
            php_status = True
        else:
            php_status = False
    if not is_page_available('localhost', "/pingphpfpm") or not php_status:
        subprocess.call('service ndeploy_backends restart', shell=True)
