#!/usr/bin/python

import cgi
import cgitb
import yaml
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Production"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
branding_file = installation_path+"/conf/branding.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

def ndeploy_branding_data():
    yaml_parsed_ndeploy_control_branding_conf['brand_logo'] = form.getvalue('brand_logo')
    yaml_parsed_ndeploy_control_branding_conf['brand_group'] = form.getvalue('brand_group')
    yaml_parsed_ndeploy_control_branding_conf['brand'] = form.getvalue('brand')

if form.getvalue('brand_logo') and form.getvalue('brand_group') and form.getvalue('brand'):
    # Read in branding configuration if it exists
    if os.path.isfile(branding_file):
        with open(branding_file, 'r') as ndeploy_control_branding_conf:
            yaml_parsed_ndeploy_control_branding_conf = yaml.safe_load(ndeploy_control_branding_conf)

        ndeploy_branding_data()

        with open(branding_file, 'w') as ndeploy_control_branding_conf:
                yaml.dump(yaml_parsed_ndeploy_control_branding_conf, ndeploy_control_branding_conf, default_flow_style=False)

        terminal_call(installation_path+'/scripts/setup_brand.sh', 'Updating branding configuration...', 'Branding configuration updated!')
        print_success('The branding configuration has been updated.')

    # Create the desired config if one doesn't exist
    else:
        yaml_parsed_ndeploy_control_branding_conf = {}

        ndeploy_branding_data()

        with open(branding_file, 'w+') as ndeploy_control_branding_conf:
            yaml.dump(yaml_parsed_ndeploy_control_branding_conf, ndeploy_control_branding_conf, default_flow_style=False)

        terminal_call(installation_path+'/scripts/setup_brand.sh', 'Creating branding configuration...', 'Branding configuration created!')
        print_success('The branding configuration has been created.')

else:
    print_forbidden()

print_simple_footer()
