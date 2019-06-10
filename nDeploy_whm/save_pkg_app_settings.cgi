#!/usr/bin/python

import cgi
import cgitb
import os
import yaml
import sys


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
default_domain_data_file = installation_path+'/conf/domain_data_default.yaml'
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


def print_forbidden():
    print(('<i class="fas fa-exclamation"></i><p>Forbidden</p>'))


def print_error(themessage):
    print(('<i class="fas fa-exclamation"></i><p>'+themessage+'</p>'))


def print_success(themessage):
    print(('<i class="fas fa-thumbs-up"></i><p>'+themessage+'</p>'))


cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('cpanelpkg') and form.getvalue('backend') and form.getvalue('backendversion') and form.getvalue('apptemplate'):
    if form.getvalue('cpanelpkg') == 'default':
        pkgdomaindata = installation_path+'/conf/domain_data_default_local.yaml'
    else:
        pkgdomaindata = installation_path+'/conf/domain_data_default_local_'+form.getvalue('cpanelpkg')+'.yaml'
    mybackend = form.getvalue('backend')
    mybackend = form.getvalue('backend')
    mybackendversion = form.getvalue('backendversion')
    myapptemplate = form.getvalue('apptemplate')
    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        mybackend_dict = backend_data_yaml_parsed.get(mybackend)
        mybackendpath = mybackend_dict.get(mybackendversion)
    else:
        print_error('Error: backend data file i/o error')
        sys.exit(0)
    if os.path.isfile(pkgdomaindata):
        # Get all config settings from the domains domain-data config file
        with open(pkgdomaindata, 'r') as profileyaml_data_stream:
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
            print('<div class="alert alert-danger"><i class="fas fa-exclamation"></i> Turned off pagespeed and mod_security options as they are incompatible with Full Page cache. The cache will not work if you turn on these options</div>')
        if '5029' in myapptemplate:
            yaml_parsed_profileyaml['set_expire_static'] = 'disabled'
            yaml_parsed_profileyaml['gzip'] = 'disabled'
            yaml_parsed_profileyaml['brotli'] = 'disabled'
            print('<div class="alert alert-danger"><i class="fas fa-exclamation"></i> Turned off gzip, brotli and set_expire_static options as they are incompatible with Wordpress Total Cache generated nginx.conf. The config will not work if you turn on these options</div>')
        with open(pkgdomaindata, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        print_success('Upstream settings Saved')
else:
    print_forbidden()

print('</body>')
print('</html>')
