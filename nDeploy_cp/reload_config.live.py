#!/usr/bin/python

import os
import time
import yaml
import cgi
import cgitb
from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, print_success, print_error, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

close_cpanel_liveapisock()
form = cgi.FieldStorage()

print_simple_header()


if form.getvalue('domain'):

    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):

        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        
        # Delay Ajax end so watcher reloads before we refresh otherwise we see invalid status
        time.sleep(2)       
        print_success('Nginx configuration successfully reloaded!')
    else:
        print_error('Domain-data file I/O error!')

else:
    print_forbidden()

print_simple_footer()
