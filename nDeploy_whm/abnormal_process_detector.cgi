#!/usr/bin/python

import cgi
import cgitb
import psutil
import platform
import os
import yaml
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

malware = False
user_list = os.listdir("/var/cpanel/users")
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
        myexe = myprocess.exe
        myusername = myprocess.username
        mypid = myprocess.pid
        mystatus = myprocess.status
    else:
        mycmdline = myprocess.cmdline()
        myexe = myprocess.exe()
        myusername = myprocess.username()
        mystatus = myprocess.status()
        mypid = myprocess.pid
    if myusername in user_list and mystatus != 'zombie':
        if not myexe.endswith(("/usr/libexec/openssh/sftp-server")) and (myexe.startswith(("/usr/bin/perl", "/home")) or myexe == '/'):
            malware = True
            if os.path.isfile('/opt/nDeploy/conf/autokill_malware'):
                subprocess.call('killall -9 -u '+myusername, shell=True)
                print('STATUS: <kbd>killed</kbd><br>')
            print('PID: <kbd>'+str(mypid)+'</kbd><br>')
            print('USER: <kbd>'+myusername+'</kbd><br>')
            print('COMMANDLINE: <kbd>'+str(mycmdline)+'</kbd><br>')
            print('EXE: <kbd>'+myexe+'</kbd>')
            print('<hr>')
if not malware:
	print('<i class="fas fa-exclamation"></i>')
	print('<p class="mb-0">No suspicious process found</p>')

print('</body>')
print('</html>')
