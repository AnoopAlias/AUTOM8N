#!/usr/bin/env python


import sys
import subprocess
import os
import platform
import psutil
import signal
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


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


# This hook script is supposed to be called after account creation by cPanel
installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
# Loading the json in on stdin send by cPanel
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]

#  Run hook only if I am root
if os.getuid() == 0:
    # If nDeploy cluster is enabled we need to add users,DNS entry for the same
    if os.path.exists(cluster_config_file):
        if os.path.isfile(installation_path+"/conf/skip_geodns"):
            subprocess.call(installation_path + "/scripts/cluster_dns_ensure_user.py "+cpaneluser, shell=True)
        else:
            subprocess.call(installation_path + "/scripts/cluster_gdnsd_ensure_user.py "+cpaneluser, shell=True)
        subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
        sighupnginx()
        print("1 nDeploy:clusteraccountrestore:"+cpaneluser)
    else:
        # We just need to generate config for the local machine
        subprocess.call(installation_path+"/scripts/generate_config.py "+cpaneluser, shell=True)
        sighupnginx()
        print("1 nDeploy:accountrestore:"+cpaneluser)
else:
    print("1 nDeploy:accountrestore:NoPrivilege:Restore"+cpaneluser)
