#!/usr/bin/env python


import sys
import json
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
hook_args = mydict["args"]
cpaneluser = hook_args["user"]
subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)  # Assuming escalateprivilege is enabled
print(("1 nDeploy:cPaneltrigger::Suspension:"+cpaneluser))
