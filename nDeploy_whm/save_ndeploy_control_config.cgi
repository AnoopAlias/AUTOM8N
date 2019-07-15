#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import yaml
import os


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ndeploy_config_file = installation_path+"/conf/ndeploy_control.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('breadcrumb_active_color'):

    # Read in ndeploy control configuration if it exists
    if os.path.isfile(ndeploy_config_file):
    	with open(ndeploy_config_file, 'r') as ndeploy_control_config:
            yaml_parsed_ndeploy_control_config = yaml.safe_load(ndeploy_control_config)
    
        yaml_parsed_ndeploy_control_config['breadcrumb_active_color'] = form.getvalue('breadcrumb_active_color')
    
    with open(ndeploy_config_file, 'w') as ndeploy_control_config:
            yaml.dump(yaml_parsed_ndeploy_control_config, ndeploy_control_config, default_flow_style=False)

    commoninclude.print_success('nDeploy Control configuration has been updated.')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
