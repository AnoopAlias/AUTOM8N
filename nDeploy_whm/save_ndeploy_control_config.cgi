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
ndeploy_control_file = installation_path+"/conf/ndeploy_control.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

def ndeploy_control_data():
    yaml_parsed_ndeploy_control_config['breadcrumb_active_color'] = form.getvalue('breadcrumb_active_color')
    yaml_parsed_ndeploy_control_config['heading_background_color'] = form.getvalue('heading_background_color')
    yaml_parsed_ndeploy_control_config['heading_foreground_color'] = form.getvalue('heading_foreground_color')
    yaml_parsed_ndeploy_control_config['heading_height'] = form.getvalue('heading_height')
    yaml_parsed_ndeploy_control_config['header_button_color'] = form.getvalue('header_button_color')
    yaml_parsed_ndeploy_control_config['icon_height'] = form.getvalue('icon_height')
    yaml_parsed_ndeploy_control_config['icon_width'] = form.getvalue('icon_width')
    yaml_parsed_ndeploy_control_config['logo_not_icon'] = form.getvalue('logo_not_icon')
    yaml_parsed_ndeploy_control_config['logo_width'] = form.getvalue('logo_width')
    yaml_parsed_ndeploy_control_config['logo_height'] = form.getvalue('logo_height')
    yaml_parsed_ndeploy_control_config['logo_url'] = form.getvalue('logo_url')
    yaml_parsed_ndeploy_control_config['app_email'] = form.getvalue('app_email')
    yaml_parsed_ndeploy_control_config['body_background_color'] = form.getvalue('body_background_color')
    yaml_parsed_ndeploy_control_config['text_color'] = form.getvalue('text_color')
    yaml_parsed_ndeploy_control_config['card_color'] = form.getvalue('card_color')
 
if form.getvalue('breadcrumb_active_color') and \
	form.getvalue('heading_background_color') and \
	form.getvalue('heading_foreground_color') and \
	form.getvalue('heading_height') and \
	form.getvalue('header_button_color') and \
	form.getvalue('icon_height') and \
	form.getvalue('logo_not_icon') and \
	form.getvalue('logo_width') and \
	form.getvalue('logo_height') and \
	form.getvalue('logo_url') and \
	form.getvalue('app_email') and \
	form.getvalue('body_background_color') and \
	form.getvalue('text_color') and \
	form.getvalue('card_color'):

    # Read in ndeploy control configuration if it exists
    if os.path.isfile(ndeploy_control_file):
    	with open(ndeploy_control_file, 'r') as ndeploy_control_config:
    	    yaml_parsed_ndeploy_control_config = yaml.safe_load(ndeploy_control_config)

    	ndeploy_control_data()

        with open(ndeploy_control_file, 'w') as ndeploy_control_config:
                yaml.dump(yaml_parsed_ndeploy_control_config, ndeploy_control_config, default_flow_style=False)

        commoninclude.print_success('nDeploy Control configuration has been updated.')

        # Create the desired config if one doesn't exist
    if not os.path.isfile(ndeploy_control_file):
        yaml_parsed_ndeploy_control_config = {}

        ndeploy_control_data()

    	with open(ndeploy_control_file, 'w+') as ndeploy_control_config:
            yaml.dump(yaml_parsed_ndeploy_control_config, ndeploy_control_config, default_flow_style=False)

        commoninclude.print_success('nDeploy Control configuration has been created.')        

else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
