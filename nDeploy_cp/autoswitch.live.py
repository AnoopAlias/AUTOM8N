#!/usr/bin/python

import os
import socket
import cgi
import cgitb
import subprocess



__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


cpaneluser = os.environ["USER"]
close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

switch_cmd = '/opt/nDeploy/scripts/auto_config.py '+cpaneluser+' setconfig'
myswitcher = subprocess.Popen(switch_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
print('<ul class="list-unstyled text-left">')
while True:
    line = myswitcher.stdout.readline()
    if not line:
        break
    print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
print('</ul>')

print('</body>')
print('</html>')
