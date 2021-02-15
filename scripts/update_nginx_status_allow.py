#!/usr/bin/env python3


import yaml
import os
import jinja2
import codecs


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_status_allow_file = "/etc/nginx/conf.d/nginx_status_allow.conf"


if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
    cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
    cluster_data_yaml = open(cluster_config_file, 'r')
    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    cluster_data_yaml.close()
    cluster_serverlist = list(cluster_data_yaml_parsed.keys())
    mergedlist = []
    ipmap_nat = []
    for server in cluster_serverlist:
        connect_server_dict = cluster_data_yaml_parsed.get(server)
        ipmap_dict = connect_server_dict.get("ipmap")
        dnsmap_dict = connect_server_dict.get("dnsmap")
        for the_upstream_ip in ipmap_dict.keys():
            if os.path.isfile('/var/cpanel/cpnat'):
                with open('/var/cpanel/cpnat') as f:
                    content = f.readlines()
                content = [x.strip() for x in content]
                if content:
                    upstream_master_ip = the_upstream_ip
                    for line in content:
                        internalip, externalip = line.split()
                        if internalip == the_upstream_ip:
                            upstream_master_ip = externalip
                            break
                else:
                    upstream_master_ip = the_upstream_ip
            else:
                upstream_master_ip = the_upstream_ip
            ipmap_nat.append(upstream_master_ip)
        mergedlist = mergedlist + ipmap_nat + list(ipmap_dict.keys()) + list(ipmap_dict.values()) + list(dnsmap_dict.keys()) + list(dnsmap_dict.values())
    the_iplist = list(set(mergedlist))
    templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "nginx_status_allow.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)
    templateVars = {"iplist": the_iplist}
    generated_config = template.render(templateVars)
    with codecs.open(nginx_status_allow_file, 'w', 'utf-8') as confout:
        confout.write(generated_config)
