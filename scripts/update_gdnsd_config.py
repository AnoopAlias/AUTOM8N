#!/usr/bin/env python


import yaml
import os
import jinja2
import codecs


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
geoip_res_file = "/etc/gdnsd/geoip_resources"
metafo_res_file = "/etc/gdnsd/metafo_resources"


def shorthostname(myhostname):
    return myhostname.split('.')[0]


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



if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
    cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
    cluster_data_yaml = open(cluster_config_file, 'r')
    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    cluster_data_yaml.close()
    cluster_serverlist = cluster_data_yaml_parsed.keys()
    if os.path.isfile(installation_path+"/conf/ndeploy_master.yaml"):
        master_config_file = installation_path+"/conf/ndeploy_master.yaml"
        master_data_yaml = open(master_config_file, 'r')
        master_data_yaml_parsed = yaml.safe_load(master_data_yaml)
        master_data_yaml.close()
        master_server = master_data_yaml_parsed.keys()[0]
        master_dnsmap = master_data_yaml_parsed.get(master_server).get('dnsmap')
        master_natmap = {}
        for ip in master_dnsmap.keys():
            master_natmap[ip] = get_dns_ip(ip)
        # Lets generate the metafo_resources file
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "metafo_resources.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {"dnsmap": master_dnsmap}
        generated_config = template.render(templateVars)
        with codecs.open(metafo_res_file, 'w', 'utf-8') as confout:
            confout.write(generated_config)
        # Lets generate the geoip_resources
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        templateEnv.filters['genshorthostname'] = shorthostname
        TEMPLATE_FILE = "geoip_resources.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {"dnsmap": master_dnsmap,
                        "clustermap": cluster_data_yaml_parsed,
                        "master_server": master_server,
                        "cluster_serverlist": cluster_serverlist,
                        "natpmap": master_natmap
                        }
        generated_config = template.render(templateVars)
        with codecs.open(geoip_res_file, 'w', 'utf-8') as confout:
            confout.write(generated_config)
