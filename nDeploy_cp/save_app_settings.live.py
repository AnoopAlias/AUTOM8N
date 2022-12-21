#!/usr/bin/env python3

import os
import time
import yaml
import cgi
import cgitb
import sys
# from autom8ntaskq import regen_nginx_conf
from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, print_success, print_error, print_forbidden, terminal_call


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
cpaneluser = os.environ["USER"]

cgitb.enable()

close_cpanel_liveapisock()
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
        print_error('Error: Backend data file I/O error!')
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
            yaml_parsed_profileyaml['waf'] = 'disabled'
            terminal_call('','Note: Turned off pagespeed and waf options as they are incompatible with Full Page cache. The cache will not work if you turn on these options!')
        if '5029' in myapptemplate or 'w3tc' in myapptemplate:
            yaml_parsed_profileyaml['set_expire_static'] = 'disabled'
            yaml_parsed_profileyaml['gzip'] = 'disabled'
            yaml_parsed_profileyaml['brotli'] = 'disabled'
            terminal_call('','Note: Turned off gzip, brotli and set_expire_static options as they are incompatible with Wordpress Total Cache generated nginx.conf. The config will not work if you turn on these options!')
        if 'noextra' in myapptemplate:
            yaml_parsed_profileyaml['set_expire_static'] = 'disabled'
            yaml_parsed_profileyaml['gzip'] = 'disabled'
            yaml_parsed_profileyaml['brotli'] = 'disabled'
            terminal_call('','Note: Turned off gzip, brotli and set_expire_static options as they are incompatible with the template generated nginx.conf. The config will not work if you turn on these options!')
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)

        # regen_nginx_conf.delay(cpaneluser)

        # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Upstream settings saved!')

    else:
        print_error('Domain-data file I/O error!')
else:
    print_forbidden()

print_simple_footer()
