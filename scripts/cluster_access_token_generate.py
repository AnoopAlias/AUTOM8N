#!/usr/bin/env python

try:
    import simplejson as json
except ImportError:
    import json
import subprocess

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


# Function defs
output_file = '/root/xtendweb_accesshash_temp'
tokendump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json api_token_create token_name=xtendwebdns acl=all", shell=True, stdout=subprocess.PIPE)
token_datafeed = tokendump.stdout.read()
tokendump_parsed = json.loads(token_datafeed)
if tokendump_parsed['metadata']['result'] == 1:
    thetoken = tokendump_parsed['data']['token']
    with open(output_file, "w") as text_file:
        text_file.write(thetoken)
else:
    print("access token already exist")
