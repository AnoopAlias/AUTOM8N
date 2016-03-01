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
app_signatures = installation_path+"/conf/appsignatures.yaml"
# Function defs


def set_preferred_php():
    backend_config_file = installation_path+"/conf/backends.yaml"
    backend_data_yaml = open(backend_config_file, 'r')
    backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    backend_data_yaml.close()
    if "PHP" in backend_data_yaml_parsed:
        print("Please choose one preferred PHP version from the list below")
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        for versions_defined in list(php_backends_dict.keys()):
            print(versions_defined)
        required_version = str(raw_input("Provide the exact desired version string here and press ENTER: "))
        required_version_path = php_backends_dict.get(required_version)
        userdata_dict = {'PHP': {required_version: required_version_path}}
        with open(installation_path+"/conf/preferred_php.yaml", 'w') as yaml_file:
            yaml_file.write(yaml.dump(userdata_dict, default_flow_style=False))
        yaml_file.close()
        return
    else:
        print("ERROR : You need atleast one PHP backends defined for setting default PHP -FPM for Apache httpd")
        sys.exit(1)


def nginx_conf_switch(user_name, domain_name):
    cpdomainyaml = "/var/cpanel/userdata/" + user_name + "/" + domain_name
    cpaneldomain_data_stream = open(cpdomainyaml, 'r')
    yaml_parsed_cpaneldomain = yaml.safe_load(cpaneldomain_data_stream)
    cpaneldomain_data_stream.close()
    document_root = yaml_parsed_cpaneldomain.get('documentroot')
    if not os.path.isfile(installation_path+"/conf/preferred_php.yaml"):
        set_preferred_php()
    prefphpyaml = installation_path+"/conf/preferred_php.yaml"
    prefphpyaml_data_stream = open(prefphpyaml, 'r')
    yaml_parsed_prefphpyaml = yaml.safe_load(prefphpyaml_data_stream)
    prefphpyaml_data_stream.close()
    phpversion = yaml_parsed_prefphpyaml.get('PHP')
    my_phpversion = str(phpversion.keys())
    my_phppath = str(phpversion.get(my_phpversion))
    sigsyaml = installation_path+"/conf/appsignatures.yaml"
    sigs_data_stream = open(sigsyaml, 'r')
    yaml_parsed_sigs = yaml.safe_load(sigs_data_stream)
    sigs_data_stream.close()
    for domain_data_file in installation_path+"/domain-data/"+domain_name, installation_path+"/domain-data/"+domain_name+"_SSL":
        if os.path.isfile(domain_data_file):
            domaindata_data_stream = open(domain_data_file, 'r')
            yaml_parsed_domaindata = yaml.safe_load(domaindata_data_stream)
            domaindata_data_stream.close()
            backend_category = yaml_parsed_domaindata.get('backend_category')
            if backend_category == "PROXY":
                phpsigs = yaml_parsed_sigs.get("PHP")
                for app_path in list(phpsigs.keys()):
                    if os.path.isfile(document_root+app_path):
                        yaml_parsed_domaindata["backend_category"] = "PHP"
                        yaml_parsed_domaindata["backend_version"] = my_phpversion
                        yaml_parsed_domaindata["backend_path"] = my_phppath
                        yaml_parsed_domaindata["profile"] = phpsigs.get(app_path)
                        with open(domain_data_file, 'w') as yaml_file:
                            yaml_file.write(yaml.dump(yaml_parsed_domaindata, default_flow_style=False))
                        yaml_file.close()
# End Function defs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto switch nginx config for domains of a cpanel user")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    if os.path.isfile(installation_path+"/conf/auto_config.exclude"):
        with open(installation_path+"/conf/auto_config.exclude") as excludes:
            for line in excludes:
                if str(line) == cpaneluser:
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
        nginx_conf_switch(cpaneluser, main_domain)  # Generate conf for main domain

        for domain_in_subdomains in sub_domains:
            nginx_conf_switch(cpaneluser, domain_in_subdomains)  # Generate conf for sub domains which takes care of addon as well
