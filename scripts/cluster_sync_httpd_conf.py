#!/usr/bin/env python

import re
import os
import yaml
import socket

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


if __name__ == "__main__":
    if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
        cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
        cluster_data_yaml = open(cluster_config_file, 'r')
        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
        cluster_data_yaml.close()
    myhostname = socket.gethostname()
    cluster_dict = cluster_data_yaml_parsed.get(myhostname)
    cluster_dict_ipmap = cluster_dict.get('ipmap')
    with open('/etc/apache2/conf/httpd.conf', 'rw') as apache_conf:
        theconf = apache_conf.read()
    print(multiple_replace(cluster_dict_ipmap, theconf))
