#!/usr/bin/env python


import yaml
import argparse
import subprocess
import os
import sys
import pwd


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


# Function defs


def cluster_ensure_arecord(user_name, domain_name):
    """Function that adds necessary A record of slave server given a domain name"""
    cpdomainyaml = "/var/cpanel/userdata/" + user_name + "/" + domain_name
    cpaneldomain_data_stream = open(cpdomainyaml, 'r')
    yaml_parsed_cpaneldomain = yaml.safe_load(cpaneldomain_data_stream)
    domain_sname = yaml_parsed_cpaneldomain.get('servername')
    domain_ip = yaml_parsed_cpaneldomain.get('ip')
    for server in serverlist:
                connect_server_dict = cluster_data_yaml_parsed.get(server)
                ipmap_dict = connect_server_dict.get("ipmap")
                remote_domain_ipv4 = ipmap_dict.get(domain_ip)
                subprocess.call(installation_path+"/scripts/cluster_dns_setup.pl add "+domain_sname+" "+remote_domain_ipv4, shell=True)


# End Function defs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenerate nginX and app server configs for cpanel user")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER

    try:
        pwd.getpwnam(cpaneluser)
    except KeyError:
        sys.exit(0)
    else:
        cpuserdatayaml = "/var/cpanel/userdata/" + cpaneluser + "/main"
        try:
            cpaneluser_data_stream = open(cpuserdatayaml, 'r')
        except IOError:
            sys.exit(0)
        yaml_parsed_cpaneluser = yaml.safe_load(cpaneluser_data_stream)
        if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
            cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            serverlist = cluster_data_yaml_parsed.keys()

            main_domain = yaml_parsed_cpaneluser.get('main_domain')
            # parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   #This data is irrelevant as parked domain list is in ServerAlias
            # addon_domains = yaml_parsed_cpaneluser.get('addon_domains')     #This data is irrelevant as addon is mapped to a subdomain
            sub_domains = yaml_parsed_cpaneluser.get('sub_domains')
            cluster_ensure_arecord(cpaneluser, main_domain)  # Generate conf for main domain

            for domain_in_subdomains in sub_domains:
                cluster_ensure_arecord(cpaneluser, domain_in_subdomains)  # Generate conf for sub domains which takes care of addon as well
        else:
            sys.exit(0)
