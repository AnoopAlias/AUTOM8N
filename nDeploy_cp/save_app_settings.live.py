#!/usr/bin/python

import commoninclude
import os
import yaml
import cgi
import cgitb
import sys
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


cgitb.enable()

commoninclude.close_cpanel_liveapisock()
form = cgi.FieldStorage()


print_simple_header()


if form.getvalue('domain') and form.getvalue('backend') and form.getvalue('backendversion') and form.getvalue('apptemplate'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend')
    mybackendversion = form.getvalue('backendversion')
    myapptemplate = form.getvalue('apptemplate')
    profileyaml = installation_path + "/domain-data/" + mydomain
    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        mybackend_dict = backend_data_yaml_parsed.get(mybackend)
        mybackendpath = mybackend_dict.get(mybackendversion)
    else:
        commoninclude.print_error('Error: backend data file i/o error')
        sys.exit(0)
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        # Ok lets save everything to the domain-data file
        yaml_parsed_profileyaml['backend_category'] = mybackend
        yaml_parsed_profileyaml['backend_path'] = mybackendpath
        yaml_parsed_profileyaml['backend_version'] = mybackendversion
        yaml_parsed_profileyaml['apptemplate_code'] = myapptemplate

        # Lets deal with settings that are mutually exclusive
        if 'redis' in myapptemplate:
            yaml_parsed_profileyaml['pagespeed'] = 'disabled'
            yaml_parsed_profileyaml['mod_security'] = 'disabled'
            print('<div class="alert alert-danger">Turned off pagespeed and mod_security options as they are incompatible with Full Page cache. The cache will not work if you turn on these options</div>')
        if '5029' in myapptemplate:
            yaml_parsed_profileyaml['set_expire_static'] = 'disabled'
            yaml_parsed_profileyaml['gzip'] = 'disabled'
            yaml_parsed_profileyaml['brotli'] = 'disabled'
            print('<div class="alert alert-danger">Turned off gzip, brotli and set_expire_static options as they are incompatible with Wordpress Total Cache generated nginx.conf. The config will not work if you turn on these options</div>')
        if 'noextra' in myapptemplate:
            yaml_parsed_profileyaml['set_expire_static'] = 'disabled'
            yaml_parsed_profileyaml['gzip'] = 'disabled'
            yaml_parsed_profileyaml['brotli'] = 'disabled'
            print('<div class="alert alert-danger">Turned off gzip, brotli and set_expire_static options as they are incompatible with the template generated nginx.conf. The config will not work if you turn on these options</div>')
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        commoninclude.print_success('Upstream settings saved')
    else:
        commoninclude.print_error('domain-data file i/o error')
else:
    commoninclude.print_forbidden()

print_simple_footer()
