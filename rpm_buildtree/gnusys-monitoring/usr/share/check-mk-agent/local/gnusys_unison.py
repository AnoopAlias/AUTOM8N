#!/usr/bin/env python


import os
import psutil
import yaml


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"


if os.path.isfile(cluster_config_file):
    filesync_fail_count = 0
    status = []
    with open(cluster_config_file, 'r') as cluster_data_yaml:
        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    for servername in cluster_data_yaml_parsed.keys():
        filesync_ok = False
        for myprocess in psutil.process_iter():
            mycmdline = myprocess.cmdline()
            if '/usr/bin/unison' in mycmdline and servername in mycmdline:
                filesync_ok = True
            else:
                pass
        if not filesync_ok:
            filesync_fail_count = filesync_fail_count+1
            status.append(servername+":FAIL")
    if filesync_fail_count > 0:
        print("2 unison - "+str(status))
    else:
        print("0 unison - OK")
