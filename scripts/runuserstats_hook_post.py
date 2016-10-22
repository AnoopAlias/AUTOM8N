#!/usr/bin/env python


import sys
import json
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
maindomain = mydict["maindomain"]
cpaneluser = mydict["user"]
os.utime(installation_path+"/domain-data/"+maindomain, None)
print(("1 nDeploy::RunUserStat::"+cpaneluser))
