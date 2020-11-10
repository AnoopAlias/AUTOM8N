#!/usr/bin/env python3

import os
import time
import yaml
import cgi
import cgitb
import sys
from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, print_success, print_error, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

close_cpanel_liveapisock()
form = cgi.FieldStorage()

print_simple_header()


#nemesida_wl  RuleId and Zone
if form.getvalue('RuleId') and form.getvalue('Zone')and form.getvalue('profileyaml'):

    # Get the Rule ID from form data
    myRuleId = form.getvalue('RuleId')
    myZone = form.getvalue('Zone')
    profileyaml = form.getvalue('profileyaml')

    if os.path.isfile(profileyaml):

        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        if 'nemesida_wl' in list(yaml_parsed_profileyaml.keys()):
            nemesida_wl_list = yaml_parsed_profileyaml.get('nemesida_wl')
            if 'WL ID:'+myRuleId+' "Z:'+myZone+'"' not in nemesida_wl_list:
                nemesida_wl_list.append('WL ID:'+myRuleId+' "Z:'+myZone+'"')
                yaml_parsed_profileyaml['nemesida_wl'] = nemesida_wl_list
        else:
            nemesida_wl_list = []
            nemesida_wl_list.append('WL ID:'+myRuleId+' "Z:'+myZone+'"')
            yaml_parsed_profileyaml['nemesida_wl'] = nemesida_wl_list


        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)

        # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Rule whitelisted successfully')
    else:
        print_error('Domain-data file I/O error!')
#delete Whitelisted Rule ID and Zone
elif form.getvalue('whiteList-to-delete') and form.getvalue('profileyaml'):

    deleting_list = form.getvalue('whiteList-to-delete')
    profileyaml = form.getvalue('profileyaml')
    # print_success(str(deleting_list))
    if os.path.isfile(profileyaml):
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        if 'nemesida_wl' in list(yaml_parsed_profileyaml.keys()):
            nemesida_wl_list = yaml_parsed_profileyaml.get('nemesida_wl')
            # print_success(nemesida_wl_list['+deleting_list+'])
            nemesida_wl_list.pop(int(deleting_list))
            yaml_parsed_profileyaml['nemesida_wl'] = nemesida_wl_list
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        # time.sleep(2)
        print_success('Deleted whitelisted successfully.')
    else:
        print_error('Domain-data file I/O error!')
#whitelist ip address
elif form.getvalue('profileyaml') and form.getvalue('ip'):
    profileyaml = form.getvalue('profileyaml')
    ipaddress = form.getvalue('ip')
    # print_success(str(ipaddress))
    if os.path.isfile(profileyaml):
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        if 'nemesida_ip_wl' in list(yaml_parsed_profileyaml.keys()):
            nemesida_ip_wl_list = yaml_parsed_profileyaml.get('nemesida_ip_wl')
            if str(ipaddress) not in nemesida_ip_wl_list:
                nemesida_ip_wl_list.append(str(ipaddress))
                yaml_parsed_profileyaml['nemesida_ip_wl'] = nemesida_ip_wl_list
        else:
            nemesida_ip_wl_list = []
            nemesida_ip_wl_list.append(str(ipaddress))
            yaml_parsed_profileyaml['nemesida_ip_wl'] = nemesida_ip_wl_list
    #
    #
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
    #
    #     # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Ipaddress updated successfully')
    else:
        print_error('Domain-data file I/O error!')
#delete Whitelisted ip addess
elif form.getvalue('ipaddress-to-delete') and form.getvalue('profileyaml'):

    deleting_list = form.getvalue('ipaddress-to-delete')
    profileyaml = form.getvalue('profileyaml')
    # print_success(str(deleting_list))
    if os.path.isfile(profileyaml):
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        if 'nemesida_ip_wl' in list(yaml_parsed_profileyaml.keys()):
            nemesida_ip_wl_list = yaml_parsed_profileyaml.get('nemesida_ip_wl')
            # print_success(nemesida_wl_list['+deleting_list+'])
            nemesida_ip_wl_list.pop(int(deleting_list))
            yaml_parsed_profileyaml['nemesida_ip_wl'] = nemesida_ip_wl_list
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
    #     # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Deleted Ipadress successfully.')
    else:
        print_error('Domain-data file I/O error!')
#whitelist Ipv6
elif form.getvalue('profileyaml') and form.getvalue('ipv6'):
    profileyaml = form.getvalue('profileyaml')
    ipv6_address = form.getvalue('ipv6')
    # print_success(str(ipv6_address))
    if os.path.isfile(profileyaml):
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        if 'nemesidaipv6_wl' in list(yaml_parsed_profileyaml.keys()):
            nemesidaipv6_wl_list = yaml_parsed_profileyaml.get('nemesidaipv6_wl')
            if ipv6_address not in nemesidaipv6_wl_list:
                nemesidaipv6_wl_list.append(ipv6_address)
                yaml_parsed_profileyaml['nemesidaipv6_wl'] = nemesidaipv6_wl_list
        else:
            nemesidaipv6_wl_list = []
            nemesidaipv6_wl_list.append(ipv6_address)
            yaml_parsed_profileyaml['nemesidaipv6_wl'] = nemesidaipv6_wl_list
    # #
    # #
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
    # #
    # #     # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Ipaddress updated successfully')
    else:
        print_error('Domain-data file I/O error!')
#delete Whitelisted ipv6 addess
elif form.getvalue('ipv6address_delete') and form.getvalue('profileyaml'):

    removing_list= form.getvalue('ipv6address_delete')
    profileyaml = form.getvalue('profileyaml')
    # print_success(str(deleting_list))
    if os.path.isfile(profileyaml):
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        if 'nemesidaipv6_wl' in list(yaml_parsed_profileyaml.keys()):
            nemesidaipv6_wl_list = yaml_parsed_profileyaml.get('nemesidaipv6_wl')
            # print_success(nemesida_wl_list['+deleting_list+'])
            nemesidaipv6_wl_list.pop(int(removing_list))
            yaml_parsed_profileyaml['nemesidaipv6_wl'] = nemesidaipv6_wl_list
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
    #     # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Deleted Ipadress successfully.')
    else:
        print_error('Domain-data file I/O error!')




else:
    print_forbidden()
print_simple_footer()
