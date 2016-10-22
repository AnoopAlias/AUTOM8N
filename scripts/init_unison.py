#!/usr/bin/env python

import argparse
import subprocess
import os

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ndeploy_slaves_file = installation_path+"/conf/ndeploy_cluster_slaves"


# Function defs


def control_unison(trigger):
    if os.path.isfile(ndeploy_slaves_file):
        if trigger == "start":
            with open(ndeploy_slaves_file) as slavelist:
                for line in slavelist:
                    proc = subprocess.Popen("/usr/bin/unison "+line, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        elif trigger == "stop":
            subprocess.call("killall unison", shell=True)
        elif trigger == "reload":
            subprocess.call("killall unison", shell=True)
            with open(ndeploy_slaves_file) as slavelist:
                for line in slavelist:
                    proc = subprocess.Popen("/usr/bin/unison "+line, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        else:
            return


parser = argparse.ArgumentParser(description="Start/Stop unison")
parser.add_argument("control_command")
args = parser.parse_args()
trigger = args.control_command
control_unison(trigger)
