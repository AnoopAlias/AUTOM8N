#!/usr/bin/env python3

import os
import yaml
import cgi
import cgitb
import sys
from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, print_success, print_error, print_forbidden, terminal_call


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"

cgitb.enable()

close_cpanel_liveapisock()
form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('domain') and form.getvalue('backend') and form.getvalue('backendversion') and form.getvalue('apptemplate') and form.getvalue('thesubdir'):

    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend')
    mybackendversion = form.getvalue('backendversion')
    myapptemplate = form.getvalue('apptemplate')
    thesubdir = form.getvalue('thesubdir')
    profileyaml = installation_path + "/domain-data/" + mydomain

    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        mybackend_dict = backend_data_yaml_parsed.get(mybackend)
        mybackendpath = mybackend_dict.get(mybackendversion)
    else:
        print_error('Backend data file I/O error!')
        sys.exit(0)
    if os.path.isfile(profileyaml):

        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        subdir_apps_dict = yaml_parsed_profileyaml.get('subdir_apps')
        if thesubdir in list(subdir_apps_dict.keys()):
            the_subdir_dict = subdir_apps_dict.get(thesubdir)
        else:
            the_subdir_dict = {}

        # Ok lets save everything to the domain-data file
        the_subdir_dict['backend_category'] = mybackend
        the_subdir_dict['backend_path'] = mybackendpath
        the_subdir_dict['backend_version'] = mybackendversion
        the_subdir_dict['apptemplate_code'] = myapptemplate

        # Lets deal with settings that are mutually exclusive
        if 'redis' in myapptemplate:
            the_subdir_dict['pagespeed'] = 'disabled'
            the_subdir_dict['waf'] = 'disabled'
            terminal_call('','Note: Turned off pagespeed and waf options as they are incompatible with Full Page cache. The cache will not work if you turn on these options!')
        if 'noextra' in myapptemplate:
            the_subdir_dict['set_expire_static'] = 'disabled'
            the_subdir_dict['gzip'] = 'disabled'
            the_subdir_dict['brotli'] = 'disabled'
            terminal_call('','Note: Turned off gzip, brotli and set_expire_static options as they are incompatible with the template generated nginx.conf. The config will not work if you turn on these options!')

        subdir_apps_dict[thesubdir] = the_subdir_dict
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        print_success('Sub-directory app settings saved!')

    else:
        print_error('Domain-data file I/O error!')
else:
    print_forbidden()

print_simple_footer()
