#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess

__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')


if form.getvalue('rebuild_brand') == 'enabled':
    subprocess.call(installation_path+"/scripts/setup_brand.sh", shell=True)
    commoninclude.print_success('Branding Configuration has been updated in WHM and cPanel.')
else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
