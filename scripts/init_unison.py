#!/usr/bin/env python

import argparse
import subprocess
import os
import yaml

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"


# Function defs


def control_unison(trigger):
    if os.path.isfile(cluster_config_file) and os.path.isfile(homedir_config_file):
        if trigger == "start":
            with open(cluster_config_file, 'r') as cluster_data_yaml:
                cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            with open(homedir_config_file, 'r') as homedir_data_yaml:
                homedir_data_yaml_parsed = yaml.safe_load(homedir_data_yaml)
            homedir_list = homedir_data_yaml_parsed.get('homedir')
            for server in cluster_data_yaml_parsed.keys():
                for myhome in homedir_list:
                    proc = subprocess.Popen("/usr/bin/nice -n 19 /usr/bin/ionice -c3 /usr/bin/unison "+myhome+"_"+server, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        elif trigger == "stop":
            subprocess.call("killall unison", shell=True)
        elif trigger == "reload":
            subprocess.call("killall unison", shell=True)
            with open(cluster_config_file, 'r') as cluster_data_yaml:
                cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            with open(homedir_config_file, 'r') as homedir_data_yaml:
                homedir_data_yaml_parsed = yaml.safe_load(homedir_data_yaml)
            homedir_list = homedir_data_yaml_parsed.get('homedir')
            for server in cluster_data_yaml_parsed.keys():
                for myhome in homedir_list:
                    proc = subprocess.Popen("/usr/bin/nice -n 19 /usr/bin/ionice -c3 /usr/bin/unison "+myhome+"_"+server, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        else:
            return


parser = argparse.ArgumentParser(description="Start/Stop unison")
parser.add_argument("control_command")
args = parser.parse_args()
trigger = args.control_command
control_unison(trigger)
