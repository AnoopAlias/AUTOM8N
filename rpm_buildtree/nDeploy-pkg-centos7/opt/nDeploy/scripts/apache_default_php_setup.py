#!/usr/bin/env python

import yaml

__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"

template_file = installation_path+"/conf/user_data.yaml.tmpl"
backend_config_file = installation_path+"/conf/backends.yaml"
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()
if "PHP" in backend_data_yaml_parsed:
    print("Please choose one default PHP version from the list below")
    php_backends_dict = backend_data_yaml_parsed["PHP"]
    for versions_defined in list(php_backends_dict.keys()):
        print(versions_defined)
    required_version = str(raw_input("Provide the exact desired version string here and press ENTER: "))
    userdata_dict = {'PHP' : required_version}
    with open(template_file, 'w') as yaml_file:
        yaml_file.write(yaml.dump(userdata_dict, default_flow_style=False))
    yaml_file.close()
else:
    print("ERROR : You need atleast one PHP backends defined for setting default PHP -FPM for Apache httpd")
