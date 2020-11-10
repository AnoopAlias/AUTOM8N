#!/usr/bin/env python3


import os
import psutil
import yaml
import subprocess
import argparse
import platform


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"


def fix_unison(trigger):
    if os.path.isfile(cluster_config_file):
        if trigger == 'restart':
            filesync_fail_count = 0
            status = []
            with open(cluster_config_file, 'r') as cluster_data_yaml:
                cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            with open(homedir_config_file, 'r') as homedir_data_yaml:
                homedir_data_yaml_parsed = yaml.safe_load(homedir_data_yaml)
            homedir_list = homedir_data_yaml_parsed.get('homedir')
            for servername in list(cluster_data_yaml_parsed.keys()):
                for myhome in homedir_list:
                    filesync_ok = False
                    for myprocess in psutil.process_iter():
                        # Workaround for Python 2.6
                        if platform.python_version().startswith('2.6'):
                            mycmdline = myprocess.cmdline
                        else:
                            mycmdline = myprocess.cmdline()
                        if '/usr/bin/unison' in mycmdline and myhome+'_'+servername in mycmdline:
                            filesync_ok = True
                        else:
                            pass
                    if not filesync_ok:
                        filesync_fail_count = filesync_fail_count+1
                        status.append(myhome+'_'+servername+":FAIL")
            for servername in list(cluster_data_yaml_parsed.keys()):
                filesync_ok = False
                for myprocess in psutil.process_iter():
                    # Workaround for Python 2.6
                    if platform.python_version().startswith('2.6'):
                        mycmdline = myprocess.cmdline
                    else:
                        mycmdline = myprocess.cmdline()
                    if '/usr/bin/unison' in mycmdline and 'phpsessions_'+servername in mycmdline:
                        filesync_ok = True
                    else:
                        pass
                if not filesync_ok:
                    filesync_fail_count = filesync_fail_count+1
                    status.append('phpsessions_'+servername+":FAIL")
            if filesync_fail_count > 0:
                print(("Unison filesync not running for - "+str(status)+" . Trying autofix:"))
                print("Trying an autorepair")
                the_raw_cmd_slave = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"find /root/.unison/ -regextype sed -regex \'/root/.unison/lk[a-f0-9]\\{32\\}\' -delete\"'
                the_raw_cmd_master = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeploymaster -m shell -a \"find /root/.unison/ -regextype sed -regex \'/root/.unison/lk[a-f0-9]\\{32\\}\' -delete\"'
                subprocess.call(the_raw_cmd_slave, shell=True)
                subprocess.call(the_raw_cmd_master, shell=True)
                subprocess.call('service ndeploy_unison restart', shell=True)
        elif trigger == 'reset':
            print("Trying a full reset of the cluster, resync will take sometime")
            subprocess.call('service ndeploy_unison stop', shell=True)
            the_raw_cmd_slave = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"find /root/.unison/ -regextype sed -regex \'/root/.unison/ar[a-f0-9]\\{32\\}\' -delete\"'
            the_raw_cmd_master = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeploymaster -m shell -a \"find /root/.unison/ -regextype sed -regex \'/root/.unison/ar[a-f0-9]\\{32\\}\' -delete\"'
            the_raw_cmd1_slave = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"find /root/.unison/ -regextype sed -regex \'/root/.unison/fp[a-f0-9]\\{32\\}\' -delete\"'
            the_raw_cmd1_master = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeploymaster -m shell -a \"find /root/.unison/ -regextype sed -regex \'/root/.unison/fp[a-f0-9]\\{32\\}\' -delete\"'
            subprocess.call(the_raw_cmd_slave, shell=True)
            subprocess.call(the_raw_cmd_master, shell=True)
            subprocess.call(the_raw_cmd1_slave, shell=True)
            subprocess.call(the_raw_cmd1_master, shell=True)
            subprocess.call('service ndeploy_unison start', shell=True)
    else:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix/Reset unison filesync")
    parser.add_argument("control_command")
    args = parser.parse_args()
    trigger = args.control_command
    fix_unison(trigger)
