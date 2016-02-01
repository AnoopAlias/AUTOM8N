#!/usr/bin/env python


import pwd
import subprocess

with open("/etc/domainusers", 'r') as domainusers:
    for line in domainusers:
        cpaneluser, domain = line.split(":")
        user_info = pwd.getpwnam(cpaneluser)
        cpaneluserhome = user_info.pw_dir
        subprocess.call('ansible ndeploycluster -m user -a "name='+cpaneluser+' home='+cpaneluserhome+'"', shell=True)
        
