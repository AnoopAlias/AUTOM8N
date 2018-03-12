#!/usr/bin/env python

import os
import yaml
import httplib
import re
from hashlib import md5
import json
import subprocess


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
    # We now check the last status of the cluster and sync the respective zone files so geoDNS can pick it up
    the_cluster_status = installation_path+"/conf/cluster_status.json"
    if os.path.isfile(the_cluster_status):
        with open(the_cluster_status) as cluster_status_data_stream:
            json_parsed_cluster_status = json.load(cluster_status_data_stream)
        status = json_parsed_cluster_status.get('status')
        if status == the_cluster_key:
            pass
        else:
            subprocess.Popen(['/usr/bin/rsync', '-a', '/opt/geodns-nDeploy/dns-data/'+the_cluster_key+'/', '/opt/geodns-nDeploy/conf/'])
            my_cluster_status = {}
            my_cluster_status['status'] = the_cluster_key
            # Lets write the status to a JSON file
            with open(the_cluster_status, 'w') as my_status_file:
                json.dump(my_cluster_status, my_status_file)
    else:
        subprocess.Popen(['/usr/bin/rsync', '-a', '/opt/geodns-nDeploy/dns-data/'+the_cluster_key+'/', '/opt/geodns-nDeploy/conf/'])
        my_cluster_status = {}
        my_cluster_status['status'] = the_cluster_key
        # Lets write the status to a JSON file
        with open(the_cluster_status, 'w') as my_status_file:
            json.dump(my_cluster_status, my_status_file)
