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
import socket
from itertools import combinations, chain
from hashlib import md5

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


# Function defs

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def cluster_ensure_zone(zone_name, domain_ip, serverlist, cluster_data_yaml_parsed, xtendweb_dns_cluster):
    """Function that create a geoDNS zone from the cPanel DNS API"""
    remote_mx = False
    with open('/etc/remotedomains') as mx_excludes:
        for line in mx_excludes:
            if str(line).rstrip() == zone_name:
                remote_mx = True
                break
    for the_uniq_key in xtendweb_dns_cluster.keys():
        # Lets get the settings and base label done first
        the_geozone = {}
        the_geozone["ttl"] = 60
        the_geozone["max_hosts"] = 1
        the_geozone["closest"] = True
        the_geozone["data"] = {}
        # init the NS,MX,A,TXT for zone itself
        the_geozone["data"][""] = {}
        the_geozone["data"][""]["ns"] = []
        the_geozone["data"][""]["mx"] = []
        the_geozone["data"][""]["a"] = []
        the_geozone["data"][""]["txt"] = []
        # Add local MX(ignore MX data from WHMAPI )
        if not remote_mx:
            myhostname = socket.gethostname()
            the_geozone_mx = {}
            the_geozone_mx["mx"] = myhostname
            the_geozone_mx["preference"] = 0
            the_geozone["data"][""]["mx"].append(the_geozone_mx)
            for server in cluster_data_yaml_parsed.keys():
                the_geozone_mx = {}
                the_geozone_mx["mx"] = server
                the_geozone_mx["preference"] = 10
                the_geozone["data"][""]["mx"].append(the_geozone_mx)
        # Add additional A record for ["data"][""]
        for server in cluster_data_yaml_parsed.keys():
            if server in xtendweb_dns_cluster[the_uniq_key]:
                print(server+" is in "+str(xtendweb_dns_cluster[the_uniq_key]))
                connect_server_dict = cluster_data_yaml_parsed.get(server)
                ipmap_dict = connect_server_dict.get("dnsmap")
                remote_domain_ipv4 = ipmap_dict.get(domain_ip)
                the_geozone["data"][""]["a"].append([remote_domain_ipv4, "10"])
        # Parse cPanel DNS data
        zonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+zone_name, shell=True, stdout=subprocess.PIPE)
        zone_datafeed = zonedump.stdout.read()
        zonedump_parsed = json.loads(zone_datafeed)
        thezone = zonedump_parsed['data']['zone'][0]
        resource_record = thezone['record']
        # Pass1 - We create the dicts/list needed for pass2
        for rr in resource_record:
            if "name" in rr.keys():
                if rr["name"] != zone_name+".":
                    # Currently we handle only  A, TXT and CNAME here
                    if rr["type"] == "A":
                        the_geozone["data"][rr["name"].replace("."+zone_name+".", "")] = {}
                        the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["a"] = []
                    elif rr["type"] == "TXT":
                        try:
                            the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["txt"] = []
                        except KeyError:
                            the_geozone["data"][rr["name"].replace("."+zone_name+".", "")] = {}
                            the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["txt"] = []
                    elif rr["type"] == "CNAME":
                        the_geozone["data"][rr["name"].replace("."+zone_name+".", "")] = {}
        # Pass2 - Here we add the actual resource records to geoDNS
        for rr in resource_record:
            if "name" in rr.keys():
                # NS
                if rr["type"] == "NS":
                    the_geozone["data"][""]["ns"].append(rr["nsdname"])
                # MX (remote)
                elif rr["type"] == "MX" and remote_mx:
                    the_geozone_mx = {}
                    the_geozone_mx["mx"] = rr["exchange"]
                    the_geozone_mx["preference"] = rr["preference"]
                    the_geozone["data"][""]["mx"].append(the_geozone_mx)
                # A
                elif rr["type"] == "A":
                    if rr["name"] == zone_name+".":
                        if socket.gethostname() in xtendweb_dns_cluster[the_uniq_key]:
                            the_geozone["data"][""]["a"].append([rr["address"], "10"])
                    else:
                        # Handle case of additional subdomains except cPanel ones like ftp,cpanel,whm etc
                        if rr["name"].startswith(("ftp.", "webdisk.", "whm.", "cpcalendars.", "cpcontacts.", "webmail.", "cpanel.")):
                            the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["a"].append([rr["address"], "10"])
                        else:
                            if socket.gethostname() in xtendweb_dns_cluster[the_uniq_key]:
                                the_geozone["data"][rr["name"].replace("."+zone_name+".", "")]["a"].append([rr["address"], "10"])
                            for server in cluster_data_yaml_parsed.keys():
                                if server in xtendweb_dns_cluster[the_uniq_key]:
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
                # Add any other RR Types we need to handle here
        # Since the JSON data is now ready, lets write it to the zone file
        with open("/opt/geodns-nDeploy/dns-data/"+the_uniq_key+"/"+zone_name+".json", 'w') as myzonefile:
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
        # Generate the slave server list in cluster and make it available globally
        if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):  # get the cluster ipmap
            cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
        else:
            cluster_data_yaml_parsed = {}
        # Prepare a python dict that has a uniq key for each powerset in a list of all servers
        if os.path.isfile("/opt/geodns-nDeploy/dns-data/geodns_cluster.yaml"):  # get the cluster ipmap
            cluster_config_file = "/opt/geodns-nDeploy/dns-data/geodns_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            geocluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            serverlist = geocluster_data_yaml_parsed.keys()
        else:
            serverlist = []
        # We generate md5(concat list of down servers)
        serverlist.sort()
        the_cluster_powerset = powerset(serverlist)
        xtendweb_dns_cluster = {}
        for the_hostlist_tuple in the_cluster_powerset:
            if the_hostlist_tuple:
                the_cluster_uniq = "".join(the_hostlist_tuple)
                the_cluster_key = md5(the_cluster_uniq.encode("utf-8")).hexdigest()
                xtendweb_dns_cluster[the_cluster_key] = the_hostlist_tuple
                if not os.path.exists("/opt/geodns-nDeploy/dns-data/"+the_cluster_key):
                    os.makedirs("/opt/geodns-nDeploy/dns-data/"+the_cluster_key)
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
        cluster_ensure_zone(main_domain, maindomain_ip, serverlist, cluster_data_yaml_parsed, xtendweb_dns_cluster)
        # iterate over the addon-domain and add DNS RR for it
        for the_addon_domain in addon_domains_dict.keys():
            with open("/var/cpanel/userdata/"+cpaneluser+"/"+addon_domains_dict.get(the_addon_domain)+".cache") as addondomain_data_stream:
                addondomain_data_stream_parsed = json.load(addondomain_data_stream)
            addondomain_ip = addondomain_data_stream_parsed.get('ip')
            cluster_ensure_zone(the_addon_domain, addondomain_ip, serverlist, cluster_data_yaml_parsed, xtendweb_dns_cluster)
        # iterate over parked domains and add DNS RR for it . IP being that of main domain
        for the_parked_domain in parked_domains:
            cluster_ensure_zone(the_parked_domain, maindomain_ip, serverlist, cluster_data_yaml_parsed, xtendweb_dns_cluster)
