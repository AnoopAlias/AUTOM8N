#!/usr/bin/env python


import yaml
import argparse
import os
import sys
import pwd


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_bin = "/usr/sbin/nginx"
backend_config_file = installation_path+"/conf/backends.yaml"
# Function defs


def get_target_version(backend_version):
    if backend_version == "PHP54" or backend_version == "PHP54_LVE":
        target = "CPANELPHP54"
    elif backend_version == "PHP55" or backend_version == "PHP55_LVE":
        target = "CPANELPHP55"
    elif backend_version == "PHP56" or backend_version == "PHP56_LVE":
        target = "CPANELPHP56"
    elif backend_version == "PHP70" or backend_version == "PHP70_LVE":
        target = "CPANELPHP70"
    else:
        target = "UNKNOWN"
    return target


def cpanelphp_switch(user_name, domain_name):
    domain_data = installation_path+"/domain-data/"+domain_name
    domaindata_data_stream = open(domain_data, 'r')
    yaml_parsed_domaindata = yaml.safe_load(domaindata_data_stream)
    domaindata_data_stream.close()
    backend_version = yaml_parsed_domaindata.get('backend_version')
    target = get_target_version(backend_version)
    if target == "UNKNOWN":
        print(domain_name+": remi php or php_lve not found . Not switching")
    else:
        if target in php_backends_dict.keys():
            php_path = php_backends_dict.get(target)
            yaml_parsed_domaindata['backend_version'] = target
            yaml_parsed_domaindata['backend_path'] = php_path
            with open(domain_data, 'w') as yaml_file:
                yaml_file.write(yaml.dump(yaml_parsed_domaindata, default_flow_style=False))
            yaml_file.close()
            print(domain_name+": PHP version updated to "+target)
        else:
            print(target+" version not installed.")
    if os.path.isfile(installation_path+"/domain-data/"+domain_name+"_SSL"):
        domain_data_ssl = installation_path+"/domain-data/"+domain_name+"_SSL"
        domaindata_data_stream = open(domain_data_ssl, 'r')
        yaml_parsed_domaindata = yaml.safe_load(domaindata_data_stream)
        domaindata_data_stream.close()
        backend_version = yaml_parsed_domaindata.get('backend_version')
        target = get_target_version(backend_version)
        if target == "UNKNOWN":
            print(domain_name+"_SSL: remi php or php_lve not found . Not switching")
        else:
            if target in php_backends_dict.keys():
                php_path = php_backends_dict.get(target)
                yaml_parsed_domaindata['backend_version'] = target
                yaml_parsed_domaindata['backend_path'] = php_path
                with open(domain_data_ssl, 'w') as yaml_file:
                    yaml_file.write(yaml.dump(yaml_parsed_domaindata, default_flow_style=False))
                yaml_file.close()
                print(domain_name+"_SSL: PHP version updated to "+target)
            else:
                print(target+" version not installed.")


# End Function defs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto switch PHP to CPANELPHP for domains of a cpanel user")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
    else:
        print("No PHP backends detected .Aborting..")
        sys.exit(0)
    if os.path.isfile(installation_path+"/conf/auto_php.exclude"):
        with open(installation_path+"/conf/auto_php.exclude") as excludes:
            for line in excludes:
                if str(line).rstrip() == cpaneluser:
                    sys.exit(0)
    try:
        pwd.getpwnam(cpaneluser)
    except KeyError:
        sys.exit(0)
    else:
        cpuserdatayaml = "/var/cpanel/userdata/" + cpaneluser + "/main"
        try:
            cpaneluser_data_stream = open(cpuserdatayaml, 'r')
        except IOError:
            sys.exit(0)
        yaml_parsed_cpaneluser = yaml.safe_load(cpaneluser_data_stream)

        main_domain = yaml_parsed_cpaneluser.get('main_domain')
        # parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   #This data is irrelevant as parked domain list is in ServerAlias
        # addon_domains = yaml_parsed_cpaneluser.get('addon_domains')     #This data is irrelevant as addon is mapped to a subdomain
        sub_domains = yaml_parsed_cpaneluser.get('sub_domains')
        cpanelphp_switch(cpaneluser, main_domain)  # Generate conf for main domain

        for domain_in_subdomains in sub_domains:
            cpanelphp_switch(cpaneluser, domain_in_subdomains)  # Generate conf for sub domains which takes care of addon as well
