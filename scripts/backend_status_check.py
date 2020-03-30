#!/usr/bin/env python

import httplib
import re
import subprocess
import os
import yaml


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
            php_backends_dict = backend_data_yaml_parsed["PHP"]
            for name, path in php_backends_dict.items():
                statuspage = "/"+name
                if not is_page_available('localhost', statuspage):
                    subprocess.call('service ndeploy_backends restart', shell=True)
                    print(name+" PHP-FPM master process is not running")
