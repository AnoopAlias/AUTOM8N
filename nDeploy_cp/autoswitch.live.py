#!/usr/bin/python

import commoninclude
import os
import cgi
import cgitb
import subprocess
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


cgitb.enable()

cpaneluser = os.environ["USER"]
commoninclude.close_cpanel_liveapisock()
form = cgi.FieldStorage()


print_simple_header()


switch_cmd = '/opt/nDeploy/scripts/auto_config.py '+cpaneluser+' setconfig'
myswitcher = subprocess.Popen(switch_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
print('<ul class="list-unstyled text-left">')
while True:
    line = myswitcher.stdout.readline()
    if not line:
        break
    print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
print('</ul>')

print_simple_footer()
