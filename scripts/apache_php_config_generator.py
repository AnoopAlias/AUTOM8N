#!/usr/bin/env python

import yaml
import os
import sys
import argparse
from generate_config import php_profile_set
import subprocess

__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"

class PhpFpmConfig:
    def __init__(self,cpaneluser):
        self.username = cpaneluser

    def configure(self):
        if os.path.isfile(installation_path+"/conf/user_data.yaml.tmpl"):
            userdatayaml = installation_path+"/user-data/"+self.username
            if os.path.isfile(userdatayaml):
                userdatayaml_data_stream = open(userdatayaml,'r')
                yaml_parsed_userdata = yaml.safe_load(userdatayaml_data_stream)
                userdatayaml_data_stream.close()
                myversion = yaml_parsed_userdata.get('PHP')
                backend_config_file = installation_path+"/conf/backends.yaml"
                backend_data_yaml = open(backend_config_file, 'r')
                backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
                backend_data_yaml.close()
                if "PHP" in backend_data_yaml_parsed:
                    php_backends_dict = backend_data_yaml_parsed["PHP"]
                    php_path = php_backends_dict.get(myversion)
                    php_profile_set(self.username, myversion, php_path)
                    path_to_socket = php_path + "/var/run/" + self.username + ".sock"
                    if os.path.islink("/opt/fpmsockets/"+self.username+".sock"):
                        os.remove("/opt/fpmsockets/"+self.username+".sock")
                        os.symlink(path_to_socket, "/opt/fpmsockets/"+self.username+".sock")
                    else:
                        os.symlink(path_to_socket, "/opt/fpmsockets/"+self.username+".sock")
                else:
                    print("ERROR:: PHP Backends missing")
            else:
                subprocess.call("cp "+installation_path+"/conf/user_data.yaml.tmpl "+userdatayaml, shell=True)
                subprocess.call("chown "+self.username+":"+self.username+" "+userdatayaml, shell=True)
                self.configure()
        else:
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set PHP-FPM socket for cpanel user to be used with Apache HTTPD")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    if os.path.isfile(installation_path+"/conf/user_data.yaml.tmpl"):
        myconfig = PhpFpmConfig(cpaneluser)
        myconfig.configure()
    else:
        sys.exit(0)
