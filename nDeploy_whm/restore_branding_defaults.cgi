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
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('    <head>')
print('    </head>')
print('    <body>')

if form.getvalue('restore_defaults') == 'enabled':
    yaml_parsed_ndeploy_control_branding_conf = {'brand': 'AUTOM8N', 'brand_logo': 'xtendweb.png', 'brand_group': 'NGINX AUTOMATION'}
    with open(branding_file, 'w') as ndeploy_control_branding_conf:
        yaml.dump(yaml_parsed_ndeploy_control_branding_conf, ndeploy_control_branding_conf, default_flow_style=False)

    procExe = subprocess.Popen('echo "*** Reverting to default branding configuration ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    procExe = subprocess.Popen(installation_path+'/scripts/setup_brand.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    procExe = subprocess.Popen('echo "*** Branding configuration reverted ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
            
    commoninclude.print_success('Branding configuration restored to default')

else:
    commoninclude.print_forbidden()

print('    </body>')
print('</html>')
