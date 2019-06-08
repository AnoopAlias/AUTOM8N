#!/usr/bin/python

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

if form.getvalue('mode'):
        if form.getvalue('mode') == 'restart':
                run_cmd = subprocess.Popen(installation_path+'/scripts/fix_unison_filesync.py restart', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print('<i class="fas fa-thumbs-up"></i>')
                print('<p>Soft Restart Complete</p>')
                print('<samp>')
                while True:
                    line = run_cmd.stdout.readline()
                    if not line:
                        break
                    print(line+'<br>')
                print('</samp>')
        elif form.getvalue('mode') == 'reset':
                run_cmd = subprocess.Popen(installation_path+'/scripts/fix_unison_filesync.py reset', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                print('<p>Hard Restart Complete</p>')
                print('<samp>')
                while True:
                    line = run_cmd.stdout.readline()
                    if not line:
                        break
                    print(line+'<br>')
                print('</samp>')
else:
	print('<i class="fas fa-exclamation"></i>')
	print('<p>Forbidden</p>')

print('</body>')
print('</html>')
