#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess
from commoninclude import print_simple_header, print_simple_footer


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

print_simple_header()

if form.getvalue('run_installer') == 'enabled':
    procExe = subprocess.Popen('echo "*** Rebuilding Native PHP ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    procExe = subprocess.Popen(installation_path+'/scripts/easy_php_setup.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    procExe = subprocess.Popen('echo "*** Native PHP Support has been rebuilt ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procExe.wait()
    commoninclude.print_success('Native PHP Rebuilt!')

else:
    commoninclude.print_forbidden()

print_simple_footer()
