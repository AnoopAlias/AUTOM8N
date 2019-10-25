#!/bin/python

import commoninclude
import cgi
import cgitb
import yaml
import os
import subprocess


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('    <head>')
print('    </head>')
print('    <body>')

if form.getvalue('plugin_status') == 'enable':
    procExe = subprocess.Popen('echo "*** Enabling Plugin ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    procExe = subprocess.Popen(installation_path+'/scripts/cpanel-nDeploy-setup.sh enable >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    procExe = subprocess.Popen('echo "*** Plugin Enabled ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    print('Plugin Enabled!')
    
elif form.getvalue('plugin_status') == 'disable':
    procExe = subprocess.Popen('echo "*** Disabling Plugin ****" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    procExe = subprocess.Popen(installation_path+'/scripts/cpanel-nDeploy-setup.sh disable >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    procExe = subprocess.Popen('echo "*** Plugin Disabled ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    print('Plugin Disabled!')

else:
    commoninclude.print_forbidden()

print('</body>')
print('</html>')
