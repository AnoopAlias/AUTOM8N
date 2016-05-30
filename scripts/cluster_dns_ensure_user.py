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


def cluster_ensure_arecord(zone_name, hostname, domain_ip):
    """Function that adds necessary A record of slave server"""
    for server in serverlist:
                connect_server_dict = cluster_data_yaml_parsed.get(server)
                ipmap_dict = connect_server_dict.get("ipmap")
                remote_domain_ipv4 = ipmap_dict.get(domain_ip)
                subprocess.call("/usr/local/cpanel/bin/whmapi1 addzonerecord domain="+zone_name+" type=A class=IN name="+hostname+". address="+remote_domain_ipv4,shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="add additional DNS A resource record for cluster")
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

        if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):  # get the cluster ipmap
            cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            serverlist = cluster_data_yaml_parsed.keys()

            main_domain = yaml_parsed_cpaneluser.get('main_domain')
            parked_domains = yaml_parsed_cpaneluser.get('parked_domains')
            addon_domains = yaml_parsed_cpaneluser.get('addon_domains')
            sub_domains = yaml_parsed_cpaneluser.get('sub_domains')

            # Add DNS for main_domain
            maindomain_datayaml = "/var/cpanel/userdata/"+cpaneluser+"/"+main_domain
            if os.path.isfile(maindomain_datayaml):
                maindomain_data_stream = open(maindomain_datayaml, 'r')
                yaml_parsed_maindomain = yaml.safe_load(maindomain_data_stream)
                maindomain_ip = yaml_parsed_maindomain.get('ip')
                cluster_ensure_arecord(main_domain, main_domain, maindomain_ip)

            # Add DNS for sub_domains
            for domain_in_subdomains in sub_domains:
                subdomain_datayaml = "/var/cpanel/userdata/"+cpaneluser+"/"+domain_in_subdomains
                if os.path.isfile(subdomain_datayaml):
                    subdomain_data_stream = open(subdomain_datayaml, 'r')
                    yaml_parsed_subdomain = yaml.safe_load(subdomain_data_stream)
                    subdomain_ip = yaml_parsed_subdomain.get('ip')
                    cluster_ensure_arecord(main_domain, domain_in_subdomains, subdomain_ip)

            # Add DNS for parked_domains
            for domain_in_parkeddomains in parked_domains:
                parkeddomain_datayaml = "/var/cpanel/userdata/"+cpaneluser+"/"+domain_in_parkeddomains
                if os.path.isfile(parkeddomain_datayaml):
                    parkeddomain_data_stream = open(parkeddomain_datayaml, 'r')
                    yaml_parsed_parkeddomain = yaml.safe_load(parkeddomain_data_stream)
                    parkeddomain_ip = yaml_parsed_parkeddomain.get('ip')
                    cluster_ensure_arecord(domain_in_parkeddomains, domain_in_parkeddomains, parkeddomain_ip)

            # Add DNS for addon_domains
            if addon_domains.keys():
                for addondom in addon_domains.keys():
                    domain_in_addondomains = addon_domains.get(addondom)
                    addondomain_datayaml = "/var/cpanel/userdata/"+cpaneluser+"/"+domain_in_addondomains
                    if os.path.isfile(addondomain_datayaml):
                        addondomain_data_stream = open(addondomain_datayaml, 'r')
                        yaml_parsed_addondomain = yaml.safe_load(addondomain_data_stream)
                        addondomain_ip = yaml_parsed_addondomain.get('ip')
                        cluster_ensure_arecord(addondom, addondom, addondomain_ip)
        else:
            sys.exit(0)
