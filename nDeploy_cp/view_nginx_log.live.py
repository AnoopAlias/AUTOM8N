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
cpanelhome = os.environ["HOME"]
commoninclude.close_cpanel_liveapisock()
form = cgi.FieldStorage()

print_simple_header()

nginx_log = cpanelhome+"/logs/nginx.log"
if os.path.isfile(nginx_log):
    tail_cmd = '/usr/bin/tail -20 '+nginx_log
    run_tail_cmd = subprocess.Popen(tail_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    print('<ul class="list-unstyled text-left">')
    while True:
        line = run_tail_cmd.stdout.readline()
        if not line:
            break
        print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
    print('</ul>')
else:
    commoninclude.print_error('NGINX log file is not present')

print_simple_footer()
