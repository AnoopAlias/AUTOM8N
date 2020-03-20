#!/usr/bin/python

import cgitb
import cgi
import os
import yaml
from commoninclude import silentremove, sighupnginx, print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cgitb.enable()

form = cgi.FieldStorage()


print_simple_header()

if form.getvalue('ddos'):
    if form.getvalue('ddos') == 'enable':
        os.rename("/etc/nginx/conf.d/dos_mitigate_systemwide.disabled", "/etc/nginx/conf.d/dos_mitigate_systemwide.enabled")
        sighupnginx()
        # Do this clusterwide if we are on a cluster
        if os.path.isfile(cluster_config_file):
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"mv /etc/nginx/conf.d/dos_mitigate_systemwide.disabled /etc/nginx/conf.d/dos_mitigate_systemwide.enabled && nginx -s reload\"', 'Enabling Nginx DDOS mitigation cluster-wide...', 'Nginx DDOS mitigation enabled cluster-wide!')
            print_success('Nginx DDOS mitigation is now enabled cluster-wide!')
        else:
            print_success('Nginx DDOS mitigation is now enabled!')
    elif form.getvalue('ddos') == 'disable':
        os.rename("/etc/nginx/conf.d/dos_mitigate_systemwide.enabled", "/etc/nginx/conf.d/dos_mitigate_systemwide.disabled")
        sighupnginx()
        # Do this clusterwide if we are on a cluster
        if os.path.isfile(cluster_config_file):
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"mv /etc/nginx/conf.d/dos_mitigate_systemwide.enabled /etc/nginx/conf.d/dos_mitigate_systemwide.disabled && nginx -s reload\"', 'Disabling Nginx DDOS mitigation cluster-wide...', 'Nginx DDOS mitigation disabled cluster-wide!')
            print_success('Nginx DDOS mitigation is now disabled cluster-wide!')
        else:
            print_success('Nginx DDOS mitigation is now disabled!')
elif form.getvalue('ipaccess'):
    if form.getvalue('ipaccess') == 'enable':
        with open('/etc/nginx/conf.d/default_server_include.conf_ddos', 'w+') as conf:
            conf.write('return 444;\n')
        sighupnginx()
        # Do this clusterwide if we are on a cluster
        if os.path.isfile(cluster_config_file):
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m copy -a \"src=/etc/nginx/conf.d/default_server_include.conf_ddos dest=/etc/nginx/conf.d/default_server_include.conf_ddos\"', 'Restricting Direct IP access...', 'Restricting direct IP access cluster-wide!')
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"nginx -s reload\"')
            print_success('Blackhole Direct IP access is now enabled cluster-wide!')
        else:
            print_success('Blackhole Direct IP access is now enabled!')
    elif form.getvalue('ipaccess') == 'disable':
        silentremove('/etc/nginx/conf.d/default_server_include.conf_ddos')
        sighupnginx()
        # Do this clusterwide if we are on a cluster
        if os.path.isfile(cluster_config_file):
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m file -a \"path=/etc/nginx/conf.d/default_server_include.conf_ddos state=absent\"', 'Removing restrictions on direct IP access...', 'Removing restrictions on direct IP access cluster-wide!')
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"nginx -s reload\"')
            print_success('Blackhole Direct IP access is now disabled cluster-wide!')
        else:
            print_success('Blackhole Direct IP access is now disabled!')
elif form.getvalue('blackholesuspended'):
    if form.getvalue('blackholesuspended') == 'enable':
        if os.path.isfile(installation_path + "/conf/domain_data_suspended_local.yaml"):
            domain_data_file = installation_path + "/conf/domain_data_suspended_local.yaml"
        else:
            domain_data_file = installation_path + "/conf/domain_data_suspended.yaml"
        with open(domain_data_file, 'r') as domain_data_stream:
            yaml_parsed_domain_data = yaml.safe_load(domain_data_stream)
        yaml_parsed_domain_data['apptemplate_code'] = 'blackhole.j2'
        with open(domain_data_file, 'w') as domain_data_stream:
            yaml.dump(yaml_parsed_domain_data, domain_data_stream, default_flow_style=False)
    elif form.getvalue('blackholesuspended') == 'disable':
        if os.path.isfile(installation_path + "/conf/domain_data_suspended_local.yaml"):
            domain_data_file = installation_path + "/conf/domain_data_suspended_local.yaml"
        else:
            domain_data_file = installation_path + "/conf/domain_data_suspended.yaml"
        with open(domain_data_file, 'r') as domain_data_stream:
            yaml_parsed_domain_data = yaml.safe_load(domain_data_stream)
        yaml_parsed_domain_data['apptemplate_code'] = 'suspended.j2'
        with open(domain_data_file, 'w') as domain_data_stream:
            yaml.dump(yaml_parsed_domain_data, domain_data_stream, default_flow_style=False)
else:
    print_forbidden()

print_simple_footer()
