#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"

installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('action'):
    print('<ul class="list-unstyled text-left">')
    if form.getvalue('action') == 'installborg':
        run_cmd = subprocess.Popen(installation_path+'/scripts/easy_borg_setup.sh', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        print('<samp>')
        while True:
            line = run_cmd.stdout.readline()
            if not line:
                break
            print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
        print('</samp>')
    else:
        commoninclude.print_forbidden()
else:
    commoninclude.print_forbidden()
print('</body>')
print('</html>')
