#!/usr/bin/env python


import sys
import json
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
cpaneluser = mydict["user"]
subprocess.call('ansible ndeploycluster -m user -a "name='+cpaneluser+' state=absent remove=yes"', shell=True)
subprocess.call('ansible ndeploycluster -m file -a "path='+installation_path+'/php-fpm.d/'+cpaneluser+'.conf state=absent"', shell=True)
subprocess.call('ansible ndeploycluster -m shell -a "'+installation_path+'/scripts/init_backends.py reload"', shell=True)
print("1 nDeploy:clusteraccountdelete:"+cpaneluser)
