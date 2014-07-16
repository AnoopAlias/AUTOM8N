import yaml
import argparse

parser = argparse.ArgumentParser(description = "Regenerate nginX and app server configs for cpanel user")
parser.add_argument("CPANELUSER")
args = parser.parse_args()
cpaneluser = args.CPANELUSER

cpuserdatayaml = "/var/cpanel/userdata/"+cpaneluser+"/main"
xsuserdatayaml = "/opt/xstack/userdata/"+cpaneluser

data_stream = open(cpuserdatayaml,'r')
yaml_parsed = yaml.safe_load(data_stream)


main_domain = yaml_parsed.get('main_domain')
parked_domains = yaml_parsed.get('parked_domains')
addon_domains = yaml_parsed.get('addon_domains')
sub_domains = yaml_parsed.get('sub_domains')

#pass1 for the main domain and its Alias(parked)
print main_domain
##nginx_confgen("domain_name")


print parked_domains
for domain in parked_domains:
        print domain
        ##nginx_park_domain("domain_name")

print addon_domains
print(type(addon_domains))
for domain in addon_domains.keys():
        print domain
        ##nginx_confgen("domain_name")
        parked_of_addon = addon_domains.get(domain)
        print parked_of_addon
        ##nginx_park_domain("domain_name")

print sub_domains
print(type(sub_domains))
for domain in sub_domains:
        print domain
        ##nginx_confgen("domain_name")

