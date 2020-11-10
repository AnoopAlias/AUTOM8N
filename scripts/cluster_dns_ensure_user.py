#!/usr/bin/env python3

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


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


# Function defs

def cluster_ensure_arecord(zone_name, hostname, domain_ip, *serverlist, **cluster_data_yaml_parsed):
    """Function that adds necessary A record of slave server"""
    skip_flag = False
    if os.path.isfile(installation_path+"/conf/dnscluster.exclude"):
        with open(installation_path+"/conf/dnscluster.exclude") as excludes:
            for line in excludes:
                if str(line).rstrip() == hostname:
                    skip_flag = True
    if not skip_flag:
        # Lets add additional A records for the round-robin
        for server in serverlist:
            connect_server_dict = cluster_data_yaml_parsed.get(server)
            ipmap_dict = connect_server_dict.get("dnsmap")
            remote_domain_ipv4 = ipmap_dict.get(domain_ip)
            zonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+zone_name, shell=True, stdout=subprocess.PIPE)
            zone_datafeed = zonedump.stdout.read()
            zonedump_parsed = json.loads(zone_datafeed)
            thezone = zonedump_parsed['data']['zone'][0]
            resource_record = thezone['record']
            for rr in resource_record:
                if rr['type'] == 'A':
                    if rr['name'] == hostname+"." and rr['address'] == remote_domain_ipv4:
                        subprocess.call("/usr/local/cpanel/bin/whmapi1 removezonerecord zone="+zone_name+" line="+str(rr['Line']), shell=True)
            if not os.path.isfile(installation_path+"/conf/DECLUSTER_DNSZONE"):
                subprocess.call("/usr/local/cpanel/bin/whmapi1 addzonerecord domain="+zone_name+" ttl=300 type=A class=IN name="+hostname+". address="+remote_domain_ipv4, shell=True)
            zonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+zone_name, shell=True, stdout=subprocess.PIPE)
            zone_datafeed = zonedump.stdout.read()
            zonedump_parsed = json.loads(zone_datafeed)
            thezone = zonedump_parsed['data']['zone'][0]
            resource_record = thezone['record']
            for rr in resource_record:
                if rr['type'] == 'CNAME':
                    if rr['name'] == 'mail.'+hostname+"." and rr['cname'] == hostname:
                        subprocess.call("/usr/local/cpanel/bin/whmapi1 removezonerecord zone="+zone_name+" line="+str(rr['Line']), shell=True)
                        subprocess.call("/usr/local/cpanel/bin/whmapi1 addzonerecord domain="+zone_name+" ttl=300 type=A class=IN name=mail."+hostname+". address="+domain_ip, shell=True)

    return


def cluster_ensure_mxrecord(zone_name, *serverlist):
    """Function that adds necessary MX record"""
    skip_flag = False
    if os.path.isfile(installation_path+"/conf/dnscluster.exclude"):
        with open(installation_path+"/conf/dnscluster.exclude") as excludes:
            for line in excludes:
                if str(line).rstrip() == zone_name:
                    skip_flag = True
                    break
    if not skip_flag:
        # Lets setup correct MX records for localdomains
        mx_skip_flag = False
        with open('/etc/remotedomains') as mx_excludes:
            for line in mx_excludes:
                if str(line).rstrip() == zone_name:
                    mx_skip_flag = True
                    break
        if not mx_skip_flag:
            zonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+zone_name, shell=True, stdout=subprocess.PIPE)
            zone_datafeed = zonedump.stdout.read()
            zonedump_parsed = json.loads(zone_datafeed)
            thezone = zonedump_parsed['data']['zone'][0]
            resource_record = thezone['record']
            # Get the count of MX records
            mxcount = 0
            for rr in resource_record:
                if rr['type'] == 'MX':
                    mxcount += 1
            if mxcount > 0:
                for item in range(1, (mxcount+1)):
                    zonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+zone_name, shell=True, stdout=subprocess.PIPE)
                    zone_datafeed = zonedump.stdout.read()
                    zonedump_parsed = json.loads(zone_datafeed)
                    thezone = zonedump_parsed['data']['zone'][0]
                    resource_record = thezone['record']
                    for rr in resource_record:
                        if rr['type'] == 'MX':
                            subprocess.call("/usr/local/cpanel/bin/whmapi1 removezonerecord zone="+zone_name+" line="+str(rr['Line']), shell=True)
                            break
            if not os.path.isfile(installation_path+"/conf/DECLUSTER_DNSZONE"):
                myhostname = socket.gethostname()
                subprocess.call("/usr/local/cpanel/bin/whmapi1 addzonerecord domain="+zone_name+" ttl=300 type=MX class=IN name="+zone_name+". preference=0 exchange="+myhostname+".", shell=True)
                print(("/usr/local/cpanel/bin/whmapi1 addzonerecord domain="+zone_name+" ttl=300 type=MX class=IN name="+zone_name+". preference=0 exchange="+myhostname+"."))
                for server in serverlist:
                    subprocess.call("/usr/local/cpanel/bin/whmapi1 addzonerecord domain="+zone_name+" ttl=300 type=MX class=IN name="+zone_name+". preference=100 exchange="+server+".", shell=True)
            else:
                subprocess.call("/usr/local/cpanel/bin/whmapi1 addzonerecord domain="+zone_name+" ttl=300 type=MX class=IN name="+zone_name+". preference=0 exchange="+zone_name+".", shell=True)
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
            serverlist = list(cluster_data_yaml_parsed.keys())
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
        cluster_ensure_arecord(main_domain, main_domain, maindomain_ip, *serverlist, **cluster_data_yaml_parsed)
        cluster_ensure_mxrecord(main_domain, *serverlist)
        # iterate over the addon-domain and add DNS RR for it
        for the_addon_domain in list(addon_domains_dict.keys()):
            with open("/var/cpanel/userdata/"+cpaneluser+"/"+addon_domains_dict.get(the_addon_domain)+".cache") as addondomain_data_stream:
                addondomain_data_stream_parsed = json.load(addondomain_data_stream)
            addondomain_ip = addondomain_data_stream_parsed.get('ip')
            cluster_ensure_arecord(the_addon_domain, the_addon_domain, addondomain_ip, *serverlist, **cluster_data_yaml_parsed)
            cluster_ensure_mxrecord(the_addon_domain, *serverlist)
        # iterate over sub-domains and add DNS RR if its not a linked sub-domain for addon-domain
        for the_sub_domain in sub_domains:
            if the_sub_domain not in list(addon_domains_dict.values()):
                cluster_ensure_arecord(main_domain, the_sub_domain, maindomain_ip, *serverlist, **cluster_data_yaml_parsed)
        # iterate over parked domains and add DNS RR for it . IP being that of main domain
        for the_parked_domain in parked_domains:
            cluster_ensure_arecord(the_parked_domain, the_parked_domain, maindomain_ip, *serverlist, **cluster_data_yaml_parsed)
            cluster_ensure_mxrecord(the_parked_domain, *serverlist)
