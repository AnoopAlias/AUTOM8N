#!/usr/bin/python

import cgi
import cgitb
import yaml
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

if form.getvalue('restore_defaults') == 'enabled':
    yaml_parsed_ndeploy_control_branding_conf = {'brand': 'AUTOM8N', 'brand_logo': 'xtendweb.png', 'brand_group': 'NGINX AUTOMATION'}
    with open(branding_file, 'w') as ndeploy_control_branding_conf:
        yaml.dump(yaml_parsed_ndeploy_control_branding_conf, ndeploy_control_branding_conf, default_flow_style=False)

    terminal_call(installation_path+'/scripts/setup_brand.sh', 'Reverting branding to defaults...', 'Branding has been reverted to default!')
    print_success('Branding has been reverted to default!')

else:
    print_forbidden()

print_simple_footer()
