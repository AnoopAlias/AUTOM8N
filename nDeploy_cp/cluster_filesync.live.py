#!/usr/bin/env python

import os
import cgitb
try:
    import simplejson as json
except ImportError:
    import json
from commoninclude import print_simple_header, print_simple_footer, terminal_call, close_cpanel_liveapisock

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cpaneluser = os.environ["USER"]

cgitb.enable()
close_cpanel_liveapisock()

print_simple_header()

# Setup SSH keys
terminal_call(installation_path+'/scripts/cluster_user_ssh_keyadd.sh')
# Try loading the main userdata cache file
cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
if os.path.isfile(cpuserdatajson):
    with open(cpuserdatajson) as cpaneluser_data_stream:
        json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
    main_domain = json_parsed_cpaneluser.get('main_domain')
    sub_domains = json_parsed_cpaneluser.get('sub_domains')
    cpdomainjson = "/var/cpanel/userdata/" + cpaneluser + "/" + main_domain + ".cache"
    with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
        json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
    maindom_docroot = json_parsed_cpaneldomain.get('documentroot')
    the_raw_cmd = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts --key-file "~/.ssh/clusterkey" ndeployslaves -m synchronize -a "src='+maindom_docroot+'/ dest='+maindom_docroot+'/"'
    terminal_call(the_raw_cmd)
    for mydomain in sub_domains:
        cpdomainjson = "/var/cpanel/userdata/" + cpaneluser + "/" + mydomain + ".cache"
        with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
            json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
        subdom_docroot = json_parsed_cpaneldomain.get('documentroot')
        the_raw_cmd = 'ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts --key-file "~/.ssh/clusterkey" ndeployslaves -m synchronize -a "src='+subdom_docroot+'/ dest='+subdom_docroot+'/"'
        terminal_call(the_raw_cmd)

print_simple_footer()
