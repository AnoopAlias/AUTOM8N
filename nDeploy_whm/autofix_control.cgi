#!/bin/python

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

if form.getvalue('autofix_status'):

    if form.getvalue('autofix_status') == 'simple':
        procExe = subprocess.Popen('echo "*** Attempting Simple Nginx AutoFix ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/attempt_autofix.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** Nginx AutoFix Completed ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        commoninclude.print_success('Nginx AutoFix Complete!')

    elif form.getvalue('autofix_status') == 'phpfpm':
        procExe = subprocess.Popen('echo "*** Attempting AutoFix of PHP Application Server ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/init_backends.py autofix >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo "*** PHP Application Server AutoFix Completed ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        commoninclude.print_success('PHP-FPM AutoFix Complete!')

else:
    commoninclude.print_forbidden()

print('    </body>')
print('</html>')
