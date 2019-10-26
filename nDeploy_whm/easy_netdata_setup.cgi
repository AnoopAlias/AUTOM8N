#!/bin/python

import commoninclude
import cgi
import cgitb
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

    if os.path.isfile('/etc/nginx/conf.d/netdata.password'):

        procExe = subprocess.Popen('echo "*** Previous Netdata credentials detected. Reinstalling latest Netdata using current credentials ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/easy_netdata_setup.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Netdata has been reinstalled using existing credentials ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        
        commoninclude.print_success('Netdata reinstalled!')        
        
    elif form.getvalue('netdata_pass') != None:

        procExe = subprocess.Popen('echo "*** Netdata is being set up using netdata::'+form.getvalue('netdata_pass')+' for credentials. Please keep this data for your records. ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/easy_netdata_setup.sh '+form.getvalue('netdata_pass')+' >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Netdata has been reinstalled using existing the new credentials ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        
        commoninclude.print_success('Netdata installed!')        

    else:
        commoninclude.print_warning('Try again with credentials!')
    
elif form.getvalue('remove_netdata_creds') == 'enabled':
    os.remove('/etc/nginx/conf.d/netdata.password')
    commoninclude.print_success('Netdata credentials reset!')

else:
    commoninclude.print_forbidden()

print('    </body>')
print('</html>')
