#!/usr/bin/env python3


import pwd
import subprocess

with open("/etc/domainusers", 'r') as domainusers:
    for line in domainusers:
        cpaneluser, domain = line.split(":")
        user_info = pwd.getpwnam(cpaneluser)
        cpaneluserhome = user_info.pw_dir
        cpanelusershell = user_info.pw_shell
        cpaneluseruid = user_info.pw_uid
        cpanelusergid = user_info.pw_gid
        subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m group -a "name='+cpaneluser+' gid='+cpanelusergid+'"', shell=True)
        subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m user -a "name='+cpaneluser+' uid='+cpaneluseruid+' group='+cpaneluser+' home='+cpaneluserhome+' shell='+cpanelusershell+'"', shell=True)
