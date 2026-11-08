#!/usr/bin/env python3

import os
import re
import time
import yaml
import cgi
import cgitb
import sys
from ipaddress import ip_address
from celery import Celery
from autom8ntaskq import regen_nginx_conf
from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, print_success, print_error, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cpaneluser = os.environ["USER"]


def safe_profileyaml(path):
    """Return a canonical domain-data path, or None if it escapes that directory."""
    if not path:
        return None
    base = os.path.realpath(installation_path + "/domain-data")
    real = os.path.realpath(path)
    if os.path.dirname(real) != base:
        return None
    return real

cgitb.enable()

close_cpanel_liveapisock()
form = cgi.FieldStorage()

print_simple_header()


# nemesida_wl  RuleId and Zone
if form.getvalue('RuleId') and form.getvalue('Zone')and form.getvalue('profileyaml'):

    # Get the Rule ID from form data
    myRuleId = form.getvalue('RuleId')
    myZone = form.getvalue('Zone')
    if not re.match(r'^[0-9]+$', myRuleId) or not re.match(r'^[0-9]+$', myZone):
        print_error('Invalid rule id or zone')
        sys.exit(0)
    profileyaml = safe_profileyaml(form.getvalue('profileyaml'))
    if not profileyaml:
        print_error('Invalid profile path')
        sys.exit(0)

    # wlList = []
    # wl_list.append(+myRuleId+)
    # wl_list.append(+myZone+)
    # print_success(myZone)

    if os.path.isfile(profileyaml):
        wlist = []
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        if 'nemesida_wl' in list(yaml_parsed_profileyaml.keys()):
            nemesida_wl_list = yaml_parsed_profileyaml.get('nemesida_wl')
            wlist.append(myRuleId)
            wlist.append(myZone)
            nemesida_wl_list.append(wlist)
            yaml_parsed_profileyaml['nemesida_wl'] = nemesida_wl_list

        else:
            nemesida_wl_list = []
            wlist = []
            wlist.append(myRuleId)
            wlist.append(myZone)
            nemesida_wl_list.append(wlist)
            yaml_parsed_profileyaml['nemesida_wl'] = nemesida_wl_list


        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        regen_nginx_conf.delay(cpaneluser)

        # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Rule whitelisted successfully')
    else:
        print_error('Domain-data file I/O error!')
# delete Whitelisted Rule ID and Zone
elif form.getvalue('whiteList-to-delete') and form.getvalue('profileyaml'):

    deleting_list = form.getvalue('whiteList-to-delete')
    profileyaml = safe_profileyaml(form.getvalue('profileyaml'))
    if not profileyaml:
        print_error('Invalid profile path')
        sys.exit(0)
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
        regen_nginx_conf.delay(cpaneluser)
        # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        # time.sleep(2)
        print_success('Deleted whitelisted successfully.')
    else:
        print_error('Domain-data file I/O error!')
# whitelist ip address
elif form.getvalue('profileyaml') and form.getvalue('ip'):
    profileyaml = safe_profileyaml(form.getvalue('profileyaml'))
    if not profileyaml:
        print_error('Invalid profile path')
        sys.exit(0)
    ipaddress = form.getvalue('ip')
    try:
        ip_address(ipaddress)
    except ValueError:
        print_error('Invalid IP address')
        sys.exit(0)
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
        regen_nginx_conf.delay(cpaneluser)
    #
    #     # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Ipaddress updated successfully')
    else:
        print_error('Domain-data file I/O error!')
# delete Whitelisted ip addess
elif form.getvalue('ipaddress-to-delete') and form.getvalue('profileyaml'):

    deleting_list = form.getvalue('ipaddress-to-delete')
    profileyaml = safe_profileyaml(form.getvalue('profileyaml'))
    if not profileyaml:
        print_error('Invalid profile path')
        sys.exit(0)
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
        regen_nginx_conf.delay(cpaneluser)
    #     # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Deleted Ipadress successfully.')
    else:
        print_error('Domain-data file I/O error!')
# whitelist Ipv6
elif form.getvalue('profileyaml') and form.getvalue('ipv6'):
    profileyaml = safe_profileyaml(form.getvalue('profileyaml'))
    if not profileyaml:
        print_error('Invalid profile path')
        sys.exit(0)
    ipv6_address = form.getvalue('ipv6')
    try:
        if ip_address(ipv6_address).version != 6:
            raise ValueError
    except ValueError:
        print_error('Invalid IPv6 address')
        sys.exit(0)
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
        regen_nginx_conf.delay(cpaneluser)
    # #
    # #     # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Ipaddress updated successfully')
    else:
        print_error('Domain-data file I/O error!')
# delete Whitelisted ipv6 addess
elif form.getvalue('ipv6address_delete') and form.getvalue('profileyaml'):

    removing_list= form.getvalue('ipv6address_delete')
    profileyaml = safe_profileyaml(form.getvalue('profileyaml'))
    if not profileyaml:
        print_error('Invalid profile path')
        sys.exit(0)
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
        regen_nginx_conf.delay(cpaneluser)
    #     # Delay Ajax end so nginx reloads before we refresh otherwise we see invalid status
        time.sleep(2)
        print_success('Deleted Ipadress successfully.')
    else:
        print_error('Domain-data file I/O error!')

else:
    print_forbidden()
print_simple_footer()
