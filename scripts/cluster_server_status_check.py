#!/usr/bin/env python

import os
import yaml
import httplib
import re
from hashlib import md5


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


def is_page_available(host, path="/"):
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
    if os.path.isfile("/opt/geodns-nDeploy/dns-data/geodns_cluster.yaml"):  # get the cluster ipmap
        cluster_config_file = "/opt/geodns-nDeploy/dns-data/geodns_cluster.yaml"
        cluster_data_yaml = open(cluster_config_file, 'r')
        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
        cluster_data_yaml.close()
        serverlist = cluster_data_yaml_parsed.keys()
    else:
        serverlist = []
    # We generate md5(concat list of down servers)
    serverlist.sort()
    server_down = []
    for server in serverlist:
        if not is_page_available(server, "/nginx-status"):
            server_down.append(server)
    server_down_uniq = "".join(server_down)
    the_cluster_key = md5(server_down_uniq.encode("utf-8")).hexdigest()
    print(the_cluster_key)
