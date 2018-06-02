#!/usr/bin/env python

import httplib
import re
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


def is_page_available(host, path="/nginx_status"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        False.
    """
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        if re.match("^[23]\d\d$", str(conn.getresponse().status)):
            return True
    except StandardError:
        return None


if __name__ == "__main__":
    if os.path.isfile("/opt/nDeploy/conf/ndeploy_master.yaml"):  # get the cluster master
        cluster_master_file = "/opt/nDeploy/conf/ndeploy_master.yaml"
        cluster_master_yaml = open(cluster_master_file, 'r')
        cluster_master_yaml_parsed = yaml.safe_load(cluster_master_yaml)
        cluster_master_yaml.close()
        cluster_master = cluster_master_yaml_parsed.keys()[0]
        if is_page_available(cluster_master, "/nginx_status"):
            subprocess.Popen(['/usr/bin/systemctl', 'stop', 'nginx.service'])
        else:
            subprocess.Popen(['/usr/bin/systemctl', 'start', 'nginx.service'])
