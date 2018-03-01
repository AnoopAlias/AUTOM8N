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


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


# Function defs

def cluster_ensure_zone(zone_name, *serverlist):
    """Function that create a geoDNS zone from the cPanel DNS API"""
    # Lets get the settings and base label done first
    the_geozone = {}
    the_geozone["ttl"] = 60
    the_geozone["max_hosts"] = 1
    the_geozone["closest"] = True
    the_geozone["data"] = {}
    # GeoDNS inbuilt health check. Doesnt work as of now
    # health_check = {}
    # health_check["type"] = "tcp"
    # health_check["frequency"] = 15
    # health_check["retry_time"] = 5
    # health_check["retries"] = 2
    # health_check["timeout"] = 3
    # health_check["port"] = 80
    # Lets populate the data dict with rr data output from cPanel DNS API
    the_geozone["data"][""] = {}
    # the_geozone["data"][""]["health"] = health_check
    zonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+zone_name, shell=True, stdout=subprocess.PIPE)
    zone_datafeed = zonedump.stdout.read()
    zonedump_parsed = json.loads(zone_datafeed)
    thezone = zonedump_parsed['data']['zone'][0]
    resource_record = thezone['record']
    the_geozone["data"][""]["ns"] = []
    the_geozone["data"][""]["mx"] = []
    the_geozone["data"][""]["a"] = []
    # Add additional A record for the cluster
    for server in serverlist:
        connect_server_dict = cluster_data_yaml_parsed.get(server)
        ipmap_dict = connect_server_dict.get("dnsmap")
        remote_domain_ipv4 = ipmap_dict.get(domain_ip)
        the_geozone["data"][""]["a"].append([remote_domain_ipv4, "10"])
    the_geozone["data"][""]["txt"] = []
    # Initialize the rr.zone.ext type dicts
    for rr in resource_record:
        if rr["type"] == "A":
            if rr["name"] != zone_name+".":
                the_geozone["data"][rr["name"].replace("."+zone_name+".", "")] = {}
                the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["a"] = []
        elif rr["type"] == "TXT":
            if rr["name"] != zone_name+".":
                try:
                    the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["txt"] = []
                except KeyError:
                    the_geozone["data"][rr["name"].replace("."+zone_name+".", "")] = {}
                    the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["txt"] = []
        elif rr["type"] == "CNAME":
            the_geozone["data"][rr["name"].replace("."+zone_name+".", "")] = {}
    # Populate the Json data structure
    for rr in resource_record:
        # Lets deal with NS records first
        if rr["type"] == "NS":
            the_geozone["data"][""]["ns"].append(rr["nsdname"])
        elif rr["type"] == "MX":
            the_geozone_mx = {}
            the_geozone_mx["mx"] = rr["exchange"]
            the_geozone_mx["preference"] = rr["preference"]
            the_geozone["data"][""]["mx"].append(the_geozone_mx)
        elif rr["type"] == "A":
            if rr["name"] == zone_name+".":
                the_geozone_a = []
                the_geozone_a.append(rr["address"])
                the_geozone_a.append("10")  # weight
                the_geozone["data"][""]["a"].append(the_geozone_a)
            else:
                the_geozone_additional_a = []
                the_geozone_additional_a.append(rr["address"])
                the_geozone_additional_a.append("10")  # weight
                the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["a"].append(the_geozone_additional_a)
                # Add additional A record for the cluster
                if not rr["name"].startswith(("webdisk.", "whm.", "cpcalendars.", "cpcontacts.", "webmail.", "cpanel.")):
                    for server in serverlist:
                        connect_server_dict = cluster_data_yaml_parsed.get(server)
                        ipmap_dict = connect_server_dict.get("dnsmap")
                        remote_domain_ipv4 = ipmap_dict.get(domain_ip)
                        the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["a"].append([remote_domain_ipv4, "10"])
        elif rr["type"] == "TXT":
            if rr["name"] == zone_name+".":
                the_geozone["data"][""]["txt"].append(rr["txtdata"])
            else:
                the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["txt"].append(rr["txtdata"])
        elif rr["type"] == "CNAME":
            the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["cname"] = rr["cname"]+"."
    # Lets write the zone to a JSON file
    with open("/opt/geodns-nDeploy/conf/"+zone_name+".json", 'w') as myzonefile:
        json.dump(the_geozone, myzonefile)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="add additional DNS A and MX resource record for cluster")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    # if user is not in /etc/passwd we dont proceed any further
    try:
        pwd.getpwnam(cpaneluser)
    except KeyError:
        sys.exit(0)
    else:
        # Generate the server list in cluster and make it available globally
        if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):  # get the cluster ipmap
            cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            serverlist = cluster_data_yaml_parsed.keys()
        else:
            serverlist = []
        # Try loading the main userdata cache file
        cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
        with open(cpuserdatajson) as cpaneluser_data_stream:
            json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
        main_domain = json_parsed_cpaneluser.get('main_domain')
        parked_domains = json_parsed_cpaneluser.get('parked_domains')
        addon_domains_dict = json_parsed_cpaneluser.get('addon_domains')     # So we know which addon is mapped to which sub-domain
        sub_domains = json_parsed_cpaneluser.get('sub_domains')
        # Begin DNS RR addition .Do it first for the main domain
        with open("/var/cpanel/userdata/"+cpaneluser+"/"+main_domain+".cache") as maindomain_data_stream:
            maindomain_data_stream_parsed = json.load(maindomain_data_stream)
        maindomain_ip = maindomain_data_stream_parsed.get('ip')
        print('=============='+main_domain+'===============')
        cluster_ensure_zone(main_domain, *serverlist)
        print('=============='+main_domain+'===============')
        # iterate over the addon-domain and add DNS RR for it
        for the_addon_domain in addon_domains_dict.keys():
            with open("/var/cpanel/userdata/"+cpaneluser+"/"+addon_domains_dict.get(the_addon_domain)+".cache") as addondomain_data_stream:
                addondomain_data_stream_parsed = json.load(addondomain_data_stream)
            addondomain_ip = addondomain_data_stream_parsed.get('ip')
            print('=============='+the_addon_domain+'===============')
            cluster_ensure_zone(the_addon_domain, *serverlist)
            print('=============='+the_addon_domain+'===============')
        # iterate over sub-domains and add DNS RR if its not a linked sub-domain for addon-domain
        for the_sub_domain in sub_domains:
            if the_sub_domain not in addon_domains_dict.values():
                print('=============='+the_sub_domain+'===============')
                #cluster_ensure_zone(main_domain, the_sub_domain, maindomain_ip)
                print('=============='+the_sub_domain+'===============')
        # iterate over parked domains and add DNS RR for it . IP being that of main domain
        for the_parked_domain in parked_domains:
            print('=============='+the_parked_domain+'===============')
            cluster_ensure_zone(the_parked_domain, *serverlist)
            print('=============='+the_parked_domain+'===============')