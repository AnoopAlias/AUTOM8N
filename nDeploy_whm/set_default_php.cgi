#!/usr/bin/env python3

import cgi
import cgitb
import yaml
from commoninclude import print_simple_header, print_simple_footer, print_success, print_error, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('phpversion'):
    backend_config_file = installation_path+"/conf/backends.yaml"
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()

    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        required_version_path = php_backends_dict.get(form.getvalue('phpversion'))
        userdata_dict = {'PHP': {form.getvalue('phpversion'): required_version_path}}
        with open(installation_path+"/conf/preferred_php.yaml", 'w') as yaml_file:
            yaml.dump(userdata_dict, yaml_file, default_flow_style=False)
        print_success('Default PHP for Autoswitch set to '+form.getvalue('phpversion')+'!')
    else:
        print_error('No Native PHP installed!')

else:
    print_forbidden()

print_simple_footer()
