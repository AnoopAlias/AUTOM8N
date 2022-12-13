#!/usr/bin/env python3

import re
import os
import yaml
import socket
import subprocess
import psutil
import platform

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

if __name__ == "__main__":
    subprocess.call('chattr -i /etc/apache2/conf/httpd.conf', shell=True)
    if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
        cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
        cluster_data_yaml = open(cluster_config_file, 'r')
        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
        cluster_data_yaml.close()
    myhostname = socket.gethostname()
    cluster_dict = cluster_data_yaml_parsed.get(myhostname)
    cluster_dict_ipmap = cluster_dict.get('ipmap')
    for key in cluster_dict_ipmap.keys():
        value = cluster_dict_ipmap.get(key)
        with open('/etc/apache2/conf/httpd.conf', 'r+', encoding="utf-8") as apache_conf:
            theconf = apache_conf.read()
            newconf = re.sub(key+':', value+':', theconf)
            apache_conf.seek(0)
            apache_conf.write(newconf)
            apache_conf.truncate()
    httpd_status = False
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if '/usr/sbin/httpd' in mycmdline:
            httpd_status = True
            break
    if httpd_status:
        subprocess.call(['/usr/sbin/apachectl', 'graceful'])
    else:
        subprocess.call('systemctl restart httpd', shell=True)
    subprocess.call('chattr +i /etc/apache2/conf/httpd.conf', shell=True)
