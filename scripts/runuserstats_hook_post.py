#!/usr/bin/env python


import sys
import json
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
maindomain = mydict["maindomain"]
cpaneluser = mydict["user"]
os.utime(installation_path+"/domain-data/"+maindomain, None)
print(("1 nDeploy::RunUserStat::"+cpaneluser))
