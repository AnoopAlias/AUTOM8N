#!/usr/bin/env python


import sys
import json
import subprocess
import os
import platform
import psutil
import signal


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"


def nginxreload():
    with open(os.devnull, 'w') as FNULL:
        subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


def safenginxreload():
    nginx_status = False
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if '/usr/sbin/nginx' in mycmdline and 'reload' in mycmdline:
            nginx_status = True
            break
    if not nginx_status:
        with open(os.devnull, 'w') as FNULL:
            subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


def sighupnginx():
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
            nginxpid = myprocess.pid
            os.kill(nginxpid, signal.SIGHUP)


cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
domainname = mydict["domain"]


with open("/etc/userdatadomains.json", "r") as userdatadomains:
    json_parsed_userdata = json.load(userdatadomains)
cpaneluserdata = json_parsed_userdata.get(domainname)
cpaneluser = cpaneluserdata[0]

subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)
sighupnginx()
print(("1 nDeploy:WHMTLStrigger:"+cpaneluser))
