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
    dnsip = ipaddress
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
    return dnsip


def generate_zone(domainname, slavelist):
    """Function that generate the gdnsd zone file"""
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
    zonedump = subprocess.Popen("/usr/local/cpanel/bin/whmapi1 --output=json dumpzone domain="+domainname, shell=True, stdout=subprocess.PIPE)
    zone_datafeed = zonedump.stdout.read()
    zonedump_parsed = json.loads(zone_datafeed)
    thezone = zonedump_parsed['data']['zone'][0]
    resource_record = thezone['record']
    gdnsdzone = []
    mx_skip_flag = False
    mx_loop_skip = False
    with open("/etc/userdatadomains.json", "r") as myuserdatadomains:
        myjson_parsed_userdata = json.load(myuserdatadomains)
    myipaddress = myjson_parsed_userdata.get(domainname)[5].split(':')[0]
    ipaddress = get_dns_ip(myipaddress)
    resourcename = resourcemap[ipaddress]
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
                    gdnsdzone.append(rr['name']+' 60 DYNA metafo!'+resourcename+'\n')
            elif rr['type'] == 'AAAA':
                # we add ipv6 only if there is a mapping
                if rr['address'] in resourcemap.keys():
                    if rr["name"].startswith(("ftp.", "webdisk.", "whm.", "cpcalendars.", "cpcontacts.", "webmail.", "cpanel.")):
                        gdnsdzone.append(rr['name']+' AAAA '+rr['address']+'\n')
                    else:
                        gdnsdzone.append(rr['name']+' 60 DYNA metafo!'+resourcemap.get(rr['address'])+'\n')
                else:
                    gdnsdzone.append(rr['name']+' AAAA '+rr['address']+'\n')
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
                if os.path.isfile(installation_path+"/conf/dnscluster.exclude"):
                    with open(installation_path+"/conf/dnscluster.exclude") as excludes:
                        for line in excludes:
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
            elif rr['type'] == 'TYPE257':
                gdnsdzone.append(rr['name']+' TYPE257 '+rr['value_legacy']+'\n')
            else:
                pass
    # Append subzone RR's
    if os.path.isfile('/etc/gdnsd/'+domainname+'_subzone'):
        with open('/etc/gdnsd/'+domainname+'_subzone', "r") as mysubzone:
            json_parsed_subzone = json.load(mysubzone)
            mysubzonelist = json_parsed_subzone.get(domainname)
        for subzonedom in mysubzonelist:
            myipaddresssub = myjson_parsed_userdata.get(subzonedom)[5].split(':')[0]
            ipaddresssub = get_dns_ip(myipaddresssub)
            resourcenamesub = resourcemap[ipaddresssub]
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
                        if rr["name"].startswith(("ftp.", "webdisk.", "whm.", "cpcalendars.", "cpcontacts.", "webmail.", "cpanel.")) or rr["address"] != ipaddresssub:
                            gdnsdzone.append(rr['name']+' A '+rr['address']+'\n')
                        else:
                            gdnsdzone.append(rr['name']+' 60 DYNA metafo!'+resourcenamesub+'\n')
                    elif rr['type'] == 'AAAA':
                        # we add ipv6 only if there is a mapping
                        if rr['address'] in resourcemap.keys():
                            if rr["name"].startswith(("ftp.", "webdisk.", "whm.", "cpcalendars.", "cpcontacts.", "webmail.", "cpanel.")):
                                gdnsdzone.append(rr['name']+' AAAA '+rr['address']+'\n')
                            else:
                                gdnsdzone.append(rr['name']+' 60 DYNA metafo!'+resourcemap.get(rr['address'])+'\n')
                        else:
                            gdnsdzone.append(rr['name']+' AAAA '+rr['address']+'\n')
                    elif rr['type'] == 'CNAME':
                        if rr['name'] == 'mail.'+subzonedom+"." and rr['cname'] == subzonedom:
                            gdnsdzone.append(rr['name']+' A '+ipaddresssub+'\n')
                        else:
                            gdnsdzone.append(rr['name']+' CNAME '+rr['cname']+'.\n')
                    elif rr['type'] == "MX" and not mx_loop_skip:
                        with open('/etc/remotedomains') as mx_excludes:
                            for line in mx_excludes:
                                if str(line).rstrip() == subzonedom:
                                    mx_skip_flag = True
                                    break
                        if os.path.isfile(installation_path+"/conf/dnscluster.exclude"):
                            with open(installation_path+"/conf/dnscluster.exclude") as excludes:
                                for line in excludes:
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
                    elif rr['type'] == 'TYPE257':
                        gdnsdzone.append(rr['name']+' TYPE257 '+rr['value_legacy']+'\n')
                    else:
                        pass
    with codecs.open('/etc/gdnsd/zones/'+domainname, "w", 'utf-8') as confout:
        confout.writelines(gdnsdzone)
    gdnsd_uid = pwd.getpwnam('nobody').pw_uid
    gdnsd_gid = grp.getgrnam('nobody').gr_gid
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
        # We use /etc/userdatadomains.json to generate the domain list and populate zonefile
        with open("/etc/userdatadomains.json", "r") as userdatadomains:
            json_parsed_userdata = json.load(userdatadomains)
            for mydomain in json_parsed_userdata.keys():
                mydata = json_parsed_userdata.get(mydomain)
                mycpaneluser = mydata[0]
                if mycpaneluser == cpaneluser:
                    myip = mydata[5].split(':')[0]
                    # Ok we need to generate the zone for this domain
                    # check if this is a subzone
                    ext = tldextract.extract(mydomain)
                    if not ext.subdomain:
                        # Its not a subzone
                        # Lets check if the zone file actually exists
                        if os.path.isfile("/var/named/"+mydomain+".db"):
                            generate_zone(mydomain, serverlist)
                    else:
                        # This is a subzone we check and generate the main zone if it exists
                        reg_domain = ext.registered_domain
                        if os.path.isfile("/var/named/"+reg_domain+".db"):
                            # Ok the zone for main domain exist do we need to generate this zone
                            # and append the subzone data in there
                            subzone_list = []
                            for mynewdomain in json_parsed_userdata.keys():
                                newext = tldextract.extract(mynewdomain)
                                if not newext.subdomain:
                                    pass
                                else:
                                    newreg_domain = newext.registered_domain
                                    if newreg_domain == reg_domain:
                                        if os.path.isfile("/var/named/"+mynewdomain+".db"):
                                            subzone_list.append(mynewdomain)
                            subzone_dict = {reg_domain: subzone_list}
                            with open('/etc/gdnsd/'+reg_domain+'_subzone', 'w') as subzone:
                                json.dump(subzone_dict, subzone)
                            generate_zone(reg_domain, serverlist)
                        else:
                            # The main domain zone does not exist, we are good to generate
                            # a seperate zone for this subzone
                            if os.path.isfile("/var/named/"+mydomain+".db"):
                                generate_zone(mydomain, serverlist)
