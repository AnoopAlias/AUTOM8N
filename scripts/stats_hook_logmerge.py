#!/usr/bin/env python

try:
    import simplejson as json
except ImportError:
    import json
import argparse
import subprocess
import os
import sys
import pwd
import yaml
from commoninclude import silentremove


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


# Function defs


def merge_logs(domain, slavelist):
    logmergelist = ['/var/log/nginx/'+domain]
    for server in slavelist:
        logmergelist.append('/var/log/nginx-'+server+'/'+domain)
    subprocess.call('/usr/local/cpanel/3rdparty/bin/logresolvemerge.pl -ignoremissing '+' '.join(logmergelist)+' > /etc/apache2/logs/domlogs/'+domain, shell=True)
    for file in logmergelist:
        silentremove(file)
    logmergelist_ssl = ['/var/log/nginx/'+domain+'-ssl_log']
    for server in slavelist:
        logmergelist_ssl.append('/var/log/nginx-'+server+'/'+domain+'-ssl_log')
    subprocess.call('/usr/local/cpanel/3rdparty/bin/logresolvemerge.pl -ignoremissing '+' '.join(logmergelist)+' > /etc/apache2/logs/domlogs/'+domain+'-ssl_log', shell=True)
    for file in logmergelist_ssl:
        silentremove(file)
    logmergelist_bytes = ['/var/log/nginx/'+domain+'-bytes_log']
    for server in slavelist:
        logmergelist_bytes.append('/var/log/nginx-'+server+'/'+domain+'-bytes_log')
    subprocess.call('/usr/local/cpanel/3rdparty/bin/logresolvemerge.pl -ignoremissing '+' '.join(logmergelist)+' > /etc/apache2/logs/domlogs/'+domain+'-bytes_log', shell=True)
    for file in logmergelist_bytes:
        silentremove(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge domlogs for user")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    # if user is not in /etc/passwd we dont proceed any further
    try:
        pwd.getpwnam(cpaneluser)
    except KeyError:
        sys.exit(0)
    else:
        if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):  # get the cluster ipmap
            cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            serverlist = cluster_data_yaml_parsed.keys()
        else:
            sys.exit(0)
    if os.path.isfile('/opt/nDeploy/conf/CLUSTER_LOG'):
        # Try loading the main userdata cache file
        cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
        with open(cpuserdatajson) as cpaneluser_data_stream:
            json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
        main_domain = json_parsed_cpaneluser.get('main_domain')
        parked_domains = json_parsed_cpaneluser.get('parked_domains')
        addon_domains_dict = json_parsed_cpaneluser.get('addon_domains')     # So we know which addon is mapped to which sub-domain
        sub_domains = json_parsed_cpaneluser.get('sub_domains')
        # Begin config generation .Do it first for the main domain
        merge_logs(main_domain, serverlist)
        # iterate over the addon-domain ,passing the subdomain as the configdomain
        for the_addon_domain in addon_domains_dict.keys():
            merge_logs(addon_domains_dict.get(the_addon_domain), serverlist)
        # iterate over sub-domains and generate config if its not a linked sub-domain for addon-domain
        for the_sub_domain in sub_domains:
            if the_sub_domain not in addon_domains_dict.values():
                if the_sub_domain.startswith("*"):
                    subdom_config_dom = "_wildcard_."+the_sub_domain.replace('*.', '')
                    merge_logs(subdom_config_dom, serverlist)
                else:
                    merge_logs(the_sub_domain, serverlist)
