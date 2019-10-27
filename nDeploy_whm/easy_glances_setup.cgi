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
__status__ = "Production"


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

if form.getvalue('run_installer') == 'enabled':

    if os.path.isfile('/etc/nginx/conf.d/glances.password'):

        procExe = subprocess.Popen('echo "*** Previous Glances credentials detected. Reinstalling latest Glances using current credentials ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/easy_glances_setup.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Glances has been reinstalled using existing credentials ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        
        commoninclude.print_success('Glances reinstalled!')        

    elif form.getvalue('glances_pass') != None:

        procExe = subprocess.Popen('echo "*** Glances is being set up using glances::'+form.getvalue('glances_pass')+' for credentials. Please keep this data for your records. ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/easy_glances_setup.sh '+form.getvalue('glances_pass')+' >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Glances has been reinstalled using existing the new credentials ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        
        commoninclude.print_success('Glances installed!')        

    else:
        commoninclude.print_warning('Try again with credentials!')
    
elif form.getvalue('remove_glances_creds') == 'enabled':
    os.remove('/etc/nginx/conf.d/glances.password')
    commoninclude.print_success('Glances credentials reset!')

else:
    commoninclude.print_forbidden()

print('    </body>')
print('</html>')
