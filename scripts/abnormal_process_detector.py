#!/usr/bin/env python

import psutil
import platform
import os
import subprocess

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


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
            subprocess.call('killall -9 -u '+myusername, shell=True)
            print(('PID:'+str(mypid)+',USER:'+myusername+',COMMANDLINE:'+str(mycmdline)+',EXE:'+myexe))
