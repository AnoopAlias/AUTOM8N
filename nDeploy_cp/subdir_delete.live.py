#!/usr/bin/env python3

import commoninclude
import os
import yaml
import cgi
import cgitb
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


cgitb.enable()

commoninclude.close_cpanel_liveapisock()
form = cgi.FieldStorage()


print_simple_header()


if form.getvalue('domain') and form.getvalue('thesubdir'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    thesubdir = form.getvalue('thesubdir')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        subdir_apps_dict = yaml_parsed_profileyaml.get('subdir_apps')
        if thesubdir in list(subdir_apps_dict.keys()):
            del subdir_apps_dict[thesubdir]
        else:
            commoninclude.print_error('The SubDir is not configured')
        yaml_parsed_profileyaml['subdir_apps'] = subdir_apps_dict
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        commoninclude.print_success('Successfully removed sub-directory')
    else:
        commoninclude.print_error('domain-data file i/o error')
else:
    commoninclude.print_forbidden()

print_simple_footer()
