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
__status__ = "Production"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
branding_file = installation_path+"/conf/branding.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('brand_logo') and form.getvalue('brand_group') and form.getvalue('brand') and form.getvalue('brand_anchor') and form.getvalue('brand_link'):

    # Read in branding configuration if it exists
    if os.path.isfile(branding_file):
    	with open(branding_file, 'r') as ndeploy_control_branding_conf:
            yaml_parsed_ndeploy_control_branding_conf = yaml.safe_load(ndeploy_control_branding_conf)
    
        yaml_parsed_ndeploy_control_branding_conf['brand_logo'] = form.getvalue('brand_logo')
        yaml_parsed_ndeploy_control_branding_conf['brand_group'] = form.getvalue('brand_group')
        yaml_parsed_ndeploy_control_branding_conf['brand'] = form.getvalue('brand')
        yaml_parsed_ndeploy_control_branding_conf['brand_anchor'] = form.getvalue('brand_anchor')
        yaml_parsed_ndeploy_control_branding_conf['brand_link'] = form.getvalue('brand_link')
    else:
    	yaml_parsed_ndeploy_control_branding_conf = {'brand': 'AUTOM8N', 'brand_logo': 'xtendweb.png', 'brand_group': 'NGINX AUTOMATION', 'brand_anchor': 'A U T O M 8 N', 'brand_link': 'https://autom8n.com/'}

    with open(branding_file, 'w') as ndeploy_control_branding_conf:
            yaml.dump(yaml_parsed_ndeploy_control_branding_conf, ndeploy_control_branding_conf, default_flow_style=False)

    commoninclude.print_success('Branding configuration has been updated.')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
