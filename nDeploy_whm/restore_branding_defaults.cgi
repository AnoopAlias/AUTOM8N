#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import yaml
import subprocess


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


if form.getvalue('restore_defaults') == 'enabled':
    yaml_parsed_ndeploy_control_branding_conf = {'brand': 'AUTOM8N', 'brand_logo': 'xtendweb.png', 'brand_group': 'NGINX AUTOMATION', 'brand_anchor': 'A U T O M 8 N', 'brand_link': 'https://autom8n.com/'}
    with open(branding_file, 'w') as ndeploy_control_branding_conf:
        yaml.dump(yaml_parsed_ndeploy_control_branding_conf, ndeploy_control_branding_conf, default_flow_style=False)

    subprocess.call(installation_path+"/scripts/setup_brand.sh", shell=True)
    commoninclude.print_success('The nDeploy branding configuration has been restored to defaults.')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
