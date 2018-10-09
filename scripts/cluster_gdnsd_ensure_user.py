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
import grp
import yaml
import socket
import codecs
import tldextract


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


# Function defs


def get_dns_ip(ipaddress):
    if os.path.isfile('/var/cpanel/cpnat'):
        with open('/var/cpanel/cpnat') as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        if content:
            for line in content:
                internalip, externalip = line.split()
                if internalip == ipaddress:
                    dnsip = externalip
                    break
        else:
            dnsip = ipaddress
    else:
        dnsip = ipaddress
    return dnsip


def generate_zone(username, domainname, ipaddress, resourcename, slavelist):
    """Function that generate the gdnsd zone file"""
    zonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+domainname, shell=True, stdout=subprocess.PIPE)
    zone_datafeed = zonedump.stdout.read()
    zonedump_parsed = json.loads(zone_datafeed)
    thezone = zonedump_parsed['data']['zone'][0]
    resource_record = thezone['record']
    gdnsdzone = []
    mx_skip_flag = False
    mx_loop_skip = False
    for rr in resource_record:
        if rr['type'] != ':RAW' or rr['type'] != '$TTL':
            if rr['type'] == 'SOA':
                gdnsdzone.insert(0, '@ SOA '+rr['mname']+'. '+rr['rname']+'. (1 7200 30M 3D 900)\n')
            elif rr['type'] == 'NS':
                gdnsdzone.append(rr['name']+" NS "+rr['nsdname']+".\n")
            elif rr['type'] == "A":
                if rr["name"].startswith(("ftp.", "webdisk.", "whm.", "cpcalendars.", "cpcontacts.", "webmail.", "cpanel.")) or rr["address"] != ipaddress:
                    gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
                else:
                    if rr["name"].rstrip('.') in sub_domains or rr["name"].rstrip('.') == domainname:
                        gdnsdzone.append(rr['name']+' 60 DYNA metafo!'+resourcename+'\n')
                    else:
                        gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
            elif rr['type'] == 'CNAME':
                if rr['name'] == 'mail.'+domainname+"." and rr['cname'] == domainname:
                    gdnsdzone.append(rr['name']+' A '+ipaddress+'\n')
                else:
                    gdnsdzone.append(rr['name']+' CNAME '+rr['cname']+'.\n')
            elif rr['type'] == "MX" and not mx_loop_skip:
                with open('/etc/remotedomains') as mx_excludes:
                    for line in mx_excludes:
                        if str(line).rstrip() == domainname:
                            mx_skip_flag = True
                            break
                if not mx_skip_flag:
                    myhostname = socket.gethostname()
                    gdnsdzone.append(rr['name']+' MX  0 '+myhostname+'.\n')
                    for server in slavelist:
                        gdnsdzone.append(rr['name']+' MX  100 '+server+'.\n')
                    mx_loop_skip = True
                else:
                    gdnsdzone.append(rr['name']+' MX '+rr['preference']+' '+rr['exchange']+'.\n')
            elif rr['type'] == "TXT":
                gdnsdzone.append(rr['name']+' TXT "'+rr['txtdata']+'"\n')
            elif rr['type'] == 'SRV':
                gdnsdzone.append(rr['name']+' SRV '+rr['priority']+' '+rr['weight']+' '+rr['port']+' '+rr['target']+'.\n')
            elif rr['type'] == 'AAAA':
                gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
            else:
                pass
    # Append subzone RR's
    if os.path.isfile('/etc/gdnsd/'+domainname+'_subzone'):
        with open('/etc/gdnsd/'+domainname+'_subzone', "r") as mysubzone:
            json_parsed_subzone = json.load(mysubzone)
            mysubzonelist = json_parsed_subzone.get(domainname)
        for subzonedom in mysubzonelist:
            # Check if its a main domain or parked and parse userdata for main dom
            with open("/etc/userdatadomains.json", "r") as userdatadomains:
                json_parsed_userdata = json.load(userdatadomains)
            if subzonedom in json_parsed_userdata.keys():
                subzonedomdata = json_parsed_userdata.get(subzonedom)
                domaintype = subzonedomdata[2]
                domainuser = subzonedomdata[0]
                if domaintype == 'parked':
                    subzonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+subzonedom, shell=True, stdout=subprocess.PIPE)
                    subzone_datafeed = subzonedump.stdout.read()
                    subzonedump_parsed = json.loads(subzone_datafeed)
                    thezone = subzonedump_parsed['data']['zone'][0]
                    resource_record = thezone['record']
                    mx_skip_flag = False
                    mx_loop_skip = False
                    for rr in resource_record:
                        if rr['type'] != ':RAW' or rr['type'] != '$TTL':
                            if rr['type'] == 'SOA':
                                pass
                            elif rr['type'] == 'NS':
                                gdnsdzone.append(rr['name']+" NS "+rr['nsdname']+".\n")
                            elif rr['type'] == "A":
                                if rr["name"].startswith(("ftp.", "webdisk.", "whm.", "cpcalendars.", "cpcontacts.", "webmail.", "cpanel.")) or rr["address"] != ipaddress:
                                    gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
                                else:
                                    if rr["name"].rstrip('.') in sub_domains or rr["name"].rstrip('.') == subzonedom:
                                        gdnsdzone.append(rr['name']+' 60 DYNA metafo!'+resourcename+'\n')
                                    else:
                                        gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
                            elif rr['type'] == 'CNAME':
                                if rr['name'] == 'mail.'+domainname+"." and rr['cname'] == subzonedom:
                                    gdnsdzone.append(rr['name']+' A '+ipaddress+'\n')
                                else:
                                    gdnsdzone.append(rr['name']+' CNAME '+rr['cname']+'.\n')
                            elif rr['type'] == "MX" and not mx_loop_skip:
                                with open('/etc/remotedomains') as mx_excludes:
                                    for line in mx_excludes:
                                        if str(line).rstrip() == subzonedom:
                                            mx_skip_flag = True
                                            break
                                if not mx_skip_flag:
                                    myhostname = socket.gethostname()
                                    gdnsdzone.append(rr['name']+' MX  0 '+myhostname+'.\n')
                                    for server in slavelist:
                                        gdnsdzone.append(rr['name']+' MX  100 '+server+'.\n')
                                    mx_loop_skip = True
                                else:
                                    gdnsdzone.append(rr['name']+' MX '+rr['preference']+' '+rr['exchange']+'.\n')
                            elif rr['type'] == "TXT":
                                gdnsdzone.append(rr['name']+' TXT "'+rr['txtdata']+'"\n')
                            elif rr['type'] == 'SRV':
                                gdnsdzone.append(rr['name']+' SRV '+rr['priority']+' '+rr['weight']+' '+rr['port']+' '+rr['target']+'.\n')
                            elif rr['type'] == 'AAAA':
                                gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
                            else:
                                pass
                else:
                    subzonedatajson = "/var/cpanel/userdata/" + domainuser + "/main.cache"
                    with open(subzonedatajson) as subzone_data_stream:
                        json_parsed_subzone = json.load(subzone_data_stream)
                    subzone_domains = json_parsed_subzone.get('sub_domains')
                    with open("/var/cpanel/userdata/"+domainuser+"/"+subzonedom+".cache") as subzonedomain_data_stream:
                        subzonedomain_data_stream_parsed = json.load(subzonedomain_data_stream)
                    subzonedomain_ip = subzonedomain_data_stream_parsed.get('ip')
                    subzoneip = get_dns_ip(subzonedomain_ip)
                    subzoneresource = resourcemap[subzonedomain_ip]
                    subzonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+subzonedom, shell=True, stdout=subprocess.PIPE)
                    subzone_datafeed = subzonedump.stdout.read()
                    subzonedump_parsed = json.loads(subzone_datafeed)
                    thezone = subzonedump_parsed['data']['zone'][0]
                    resource_record = thezone['record']
                    mx_skip_flag = False
                    mx_loop_skip = False
                    for rr in resource_record:
                        if rr['type'] != ':RAW' or rr['type'] != '$TTL':
                            if rr['type'] == 'SOA':
                                pass
                            elif rr['type'] == 'NS':
                                gdnsdzone.append(rr['name']+" NS "+rr['nsdname']+".\n")
                            elif rr['type'] == "A":
                                if rr["name"].startswith(("ftp.", "webdisk.", "whm.", "cpcalendars.", "cpcontacts.", "webmail.", "cpanel.")) or rr["address"] != subzoneip:
                                    gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
                                else:
                                    if rr["name"].rstrip('.') in subzone_domains or rr["name"].rstrip('.') == subzonedom:
                                        gdnsdzone.append(rr['name']+' 60 DYNA metafo!'+subzoneresource+'\n')
                                    else:
                                        gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
                            elif rr['type'] == 'CNAME':
                                if rr['name'] == 'mail.'+domainname+"." and rr['cname'] == subzonedom:
                                    gdnsdzone.append(rr['name']+' A '+subzoneip+'\n')
                                else:
                                    gdnsdzone.append(rr['name']+' CNAME '+rr['cname']+'.\n')
                            elif rr['type'] == "MX" and not mx_loop_skip:
                                with open('/etc/remotedomains') as mx_excludes:
                                    for line in mx_excludes:
                                        if str(line).rstrip() == subzonedom:
                                            mx_skip_flag = True
                                            break
                                if not mx_skip_flag:
                                    myhostname = socket.gethostname()
                                    gdnsdzone.append(rr['name']+' MX  0 '+myhostname+'.\n')
                                    for server in slavelist:
                                        gdnsdzone.append(rr['name']+' MX  100 '+server+'.\n')
                                    mx_loop_skip = True
                                else:
                                    gdnsdzone.append(rr['name']+' MX '+rr['preference']+' '+rr['exchange']+'.\n')
                            elif rr['type'] == "TXT":
                                gdnsdzone.append(rr['name']+' TXT "'+rr['txtdata']+'"\n')
                            elif rr['type'] == 'SRV':
                                gdnsdzone.append(rr['name']+' SRV '+rr['priority']+' '+rr['weight']+' '+rr['port']+' '+rr['target']+'.\n')
                            elif rr['type'] == 'AAAA':
                                gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
                            else:
                                pass
    with codecs.open('/etc/gdnsd/zones/'+domainname, "w", 'utf-8') as confout:
        confout.writelines(gdnsdzone)
    gdnsd_uid = pwd.getpwnam('gdnsd').pw_uid
    gdnsd_gid = grp.getgrnam('gdnsd').gr_gid
    os.chown('/etc/gdnsd/zones/'+domainname, gdnsd_uid, gdnsd_gid)
    os.chmod('/etc/gdnsd/zones/'+domainname, 0o660)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate gdnsd zone file")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    # if user is not in /etc/passwd we dont proceed any further
    try:
        pwd.getpwnam(cpaneluser)
    except KeyError:
        sys.exit(0)
    else:
        # Make the ip resource map available
        if os.path.isfile(installation_path+"/conf/ndeploy_master.yaml"):  # get the master ipmap
            cluster_config_file = installation_path+"/conf/ndeploy_master.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            myhostname = socket.gethostname()
            resourcemap = cluster_data_yaml_parsed[myhostname]['dnsmap']
        else:
            sys.exit(0)
        if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):  # get the cluster ipmap
            cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            serverlist = cluster_data_yaml_parsed.keys()
        else:
            sys.exit(0)
        # Try loading the main userdata cache file
        cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
        with open(cpuserdatajson) as cpaneluser_data_stream:
            json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
        main_domain = json_parsed_cpaneluser.get('main_domain')
        parked_domains = json_parsed_cpaneluser.get('parked_domains')
        addon_domains_dict = json_parsed_cpaneluser.get('addon_domains')     # So we know which addon is mapped to which sub-domain
        sub_domains = json_parsed_cpaneluser.get('sub_domains')
        # Begin DNS zone add .Do it first for the main domain
        with open("/var/cpanel/userdata/"+cpaneluser+"/"+main_domain+".cache") as maindomain_data_stream:
            maindomain_data_stream_parsed = json.load(maindomain_data_stream)
        maindomain_ip = maindomain_data_stream_parsed.get('ip')
        ext = tldextract.extract(main_domain)
        if not ext.subdomain:
            generate_zone(cpaneluser, main_domain, get_dns_ip(maindomain_ip), resourcemap[maindomain_ip], serverlist)
        else:
            # Generate subzone map if this is a subzone
            reg_domain = ext.registered_domain
            with open("/etc/userdatadomains.json", "r") as userdatadomains:
                json_parsed_userdata = json.load(userdatadomains)
                if reg_domain in json_parsed_userdata.keys():
                    # Ok this is indeed a subzone
                    # Iterate over all domains and record subzone map
                    cpaneluserdata = json_parsed_userdata.get(reg_domain)
                    origcpaneluser = cpaneluserdata[0]
                    subzone_list = []
                    for mydomain in json_parsed_userdata.keys():
                        newext = tldextract.extract(mydomain)
                        if not newext.subdomain:
                            pass
                        else:
                            newreg_domain = newext.registered_domain
                            if newreg_domain == reg_domain:
                                subzone_list.append(mydomain)
                    subzone_dict = {reg_domain: subzone_list}
                    with open('/etc/gdnsd/'+reg_domain+'_subzone', 'w') as subzone:
                        json.dump(subzone_dict, subzone)
                    subprocess.call('/opt/nDeploy/scripts/cluster_gdnsd_ensure_user.py '+origcpaneluser, shell=True)
                else:
                    generate_zone(cpaneluser, main_domain, get_dns_ip(maindomain_ip), resourcemap[maindomain_ip], serverlist)
        # iterate over the addon-domain and add DNS RR for it
        for the_addon_domain in addon_domains_dict.keys():
            with open("/var/cpanel/userdata/"+cpaneluser+"/"+addon_domains_dict.get(the_addon_domain)+".cache") as addondomain_data_stream:
                addondomain_data_stream_parsed = json.load(addondomain_data_stream)
            addondomain_ip = addondomain_data_stream_parsed.get('ip')
            generate_zone(cpaneluser, the_addon_domain, get_dns_ip(addondomain_ip), resourcemap[addondomain_ip], serverlist)
        # We dont check sub-domains as they are handled in the other zones
        # iterate over parked domains and add DNS RR for it . IP being that of main domain
        for the_parked_domain in parked_domains:
            extpark = tldextract.extract(the_parked_domain)
            if not extpark.subdomain:
                generate_zone(cpaneluser, the_parked_domain, get_dns_ip(maindomain_ip), resourcemap[maindomain_ip], serverlist)
            else:
                reg_domain = extpark.registered_domain
                # Generate subzone map if this is a subzone
                with open("/etc/userdatadomains.json", "r") as userdatadomains:
                    json_parsed_userdata = json.load(userdatadomains)
                    if reg_domain in json_parsed_userdata.keys():
                        # prevent loop
                        if os.path.isfile('/etc/gdnsd/'+reg_domain+'_subzone'):
                            with open('/etc/gdnsd/'+reg_domain+'_subzone', "r") as mysubzone:
                                json_parsed_subzone = json.load(mysubzone)
                                mysubzonelist = json_parsed_subzone.get(reg_domain)
                                if the_parked_domain in mysubzonelist:
                                    pass
                                else:
                                    # Ok this is indeed a subzone
                                    # Iterate over all domains and record subzone map
                                    cpaneluserdata = json_parsed_userdata.get(reg_domain)
                                    origcpaneluser = cpaneluserdata[0]
                                    subzone_list = []
                                    for mydomain in json_parsed_userdata.keys():
                                        newext = tldextract.extract(mydomain)
                                        if not newext.subdomain:
                                            pass
                                        else:
                                            newreg_domain = newext.registered_domain
                                            if newreg_domain == reg_domain:
                                                subzone_list.append(mydomain)
                                    subzone_dict = {reg_domain: subzone_list}
                                    with open('/etc/gdnsd/'+reg_domain+'_subzone', 'w') as subzone:
                                        json.dump(subzone_dict, subzone)
                                    subprocess.call('/opt/nDeploy/scripts/cluster_gdnsd_ensure_user.py '+origcpaneluser, shell=True)
                        else:
                            # Ok this is indeed a subzone
                            # Iterate over all domains and record subzone map
                            cpaneluserdata = json_parsed_userdata.get(reg_domain)
                            origcpaneluser = cpaneluserdata[0]
                            subzone_list = []
                            for mydomain in json_parsed_userdata.keys():
                                newext = tldextract.extract(mydomain)
                                if not newext.subdomain:
                                    pass
                                else:
                                    newreg_domain = newext.registered_domain
                                    if newreg_domain == reg_domain:
                                        subzone_list.append(mydomain)
                            subzone_dict = {reg_domain: subzone_list}
                            with open('/etc/gdnsd/'+reg_domain+'_subzone', 'w') as subzone:
                                json.dump(subzone_dict, subzone)
                            subprocess.call('/opt/nDeploy/scripts/cluster_gdnsd_ensure_user.py '+origcpaneluser, shell=True)
                    else:
                        generate_zone(cpaneluser, the_parked_domain, get_dns_ip(maindomain_ip), resourcemap[maindomain_ip], serverlist)
