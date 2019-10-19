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
    yaml_parsed_ndeploy_control_config['ndeploy_theme_color'] = form.getvalue('ndeploy_theme_color')
    yaml_parsed_ndeploy_control_config['primary_color'] = form.getvalue('primary_color')
    yaml_parsed_ndeploy_control_config['logo_url'] = form.getvalue('logo_url')
    yaml_parsed_ndeploy_control_config['app_email'] = form.getvalue('app_email')
 
if form.getvalue('ndeploy_theme_color') and \
    form.getvalue('primary_color') and \
	form.getvalue('logo_url') and \
	form.getvalue('app_email'):

    # Read in ndeploy control configuration if it exists
    if os.path.isfile(ndeploy_control_file):
        with open(ndeploy_control_file, 'r') as ndeploy_control_config:
            yaml_parsed_ndeploy_control_config = yaml.safe_load(ndeploy_control_config)

        # Check if theme style selection is different from what is currently saved
        if yaml_parsed_ndeploy_control_config['ndeploy_theme_color'] != form.getvalue('ndeploy_theme_color'):

            # Check if the primary color is not being asked to be changed as well, if it is, let them make the changes
            if yaml_parsed_ndeploy_control_config['primary_color'] == form.getvalue('primary_color'):

                # If dark theme, default to light primary color
                if form.getvalue('ndeploy_theme_color') == "dark":
                    yaml_parsed_ndeploy_control_config['primary_color'] = "#EDEDED"
                else:
                    yaml_parsed_ndeploy_control_config['primary_color'] = "#121212"

                # Set remaining aesthetics settings
                yaml_parsed_ndeploy_control_config['ndeploy_theme_color'] = form.getvalue('ndeploy_theme_color')
                yaml_parsed_ndeploy_control_config['logo_url'] = form.getvalue('logo_url')
                yaml_parsed_ndeploy_control_config['app_email'] = form.getvalue('app_email')

            else:
                ndeploy_control_data()

        else:
            ndeploy_control_data()

        with open(ndeploy_control_file, 'w') as ndeploy_control_config:
                yaml.dump(yaml_parsed_ndeploy_control_config, ndeploy_control_config, default_flow_style=False)

        commoninclude.print_success('The nDeploy aesthetics configuration has been updated.')

    # Create the desired config if one doesn't exist
    else:
        yaml_parsed_ndeploy_control_config = {}

        ndeploy_control_data()

        # If switching to dark theme without changing primary color as well
        if form.getvalue('ndeploy_theme_color') == "dark" and form.getvalue('primary_color') == "#121212":
            yaml_parsed_ndeploy_control_config['primary_color'] = "#EDEDED"

    	with open(ndeploy_control_file, 'w+') as ndeploy_control_config:
            yaml.dump(yaml_parsed_ndeploy_control_config, ndeploy_control_config, default_flow_style=False)

        commoninclude.print_success('The nDeploy aesthetics configuration has been created.')        

else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
