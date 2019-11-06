#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import psutil
import platform
import os
import subprocess
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

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
            if not os.path.isfile('/opt/nDeploy/conf/disable_autokill_malware'):

                # We should build this out more with more detections, then we can
                # add it to Term along with current toast setup. - Budd
                subprocess.call('killall -9 -u '+myusername, shell=True)
                print('STATUS: <kbd>killed</kbd><br>')
            print('PID: <kbd>'+str(mypid)+'</kbd><br>')
            print('USER: <kbd>'+myusername+'</kbd><br>')
            print('COMMANDLINE: <kbd>'+str(mycmdline)+'</kbd><br>')
            print('EXE: <kbd>'+myexe+'</kbd>')
            print('<hr>')
if not malware:
    commoninclude.print_success('No suspicious processes found!')

print_simple_footer()
