#!/usr/bin/env python3
  
import json
import os
import yaml
import fileinput
import sys
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


if __name__ == "__main__":
    if os.path.isfile(installation_path+"/conf/nDeploy-cluster/hosts"):
        with open(installation_path+"/conf/nDeploy-cluster/hosts", 'r') as hosts_file:
            yaml_parsed_hosts = yaml.safe_load(hosts_file)
        for host in yaml_parsed_hosts['all']['children']['ndeployslaves']['hosts'].keys():
            ssh_port = yaml_parsed_hosts['all']['children']['ndeployslaves']['hosts'][host].get('ansible_port')
            subprocess.call('for dir in $(cat /etc/userdatadomains|awk -F"==" \'{print $5}\'); do rsync -av -u -x -e "ssh -p '+ssh_port+'" ${dir}/ root@'+host+':${dir}/; done', shell=True)
