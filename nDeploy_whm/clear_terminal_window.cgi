#!/usr/bin/python

import cgi
import cgitb
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


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

terminal_call('echo "Terminal has been cleared..." > '+whm_terminal_log)

print_simple_footer()
