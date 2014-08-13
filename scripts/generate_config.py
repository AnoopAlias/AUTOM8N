import yaml
import argparse

parser = argparse.ArgumentParser(description = "Regenerate nginX and app server configs for cpanel user")
parser.add_argument("CPANELUSER")
args = parser.parse_args()
cpaneluser = args.CPANELUSER

cpuserdatayaml = "/var/cpanel/userdata/"+cpaneluser+"/main"
xsuserdatayaml = "../userdata/"+cpaneluser

data_stream = open(cpuserdatayaml,'r')
yaml_parsed = yaml.safe_load(data_stream)


main_domain = yaml_parsed.get('main_domain')   
parked_domains = yaml_parsed.get('parked_domains')   #This data is irrelevant as parked domain list can be obtained from the domains userdata
addon_domains = yaml_parsed.get('addon_domains')     #This data is irrelevant as addon is mapped to a subdomain
sub_domains = yaml_parsed.get('sub_domains')

def nginx_confgen(user_name,domain_name,config_template_code):
	"Function that generates nginx config given a domain name"
	cpdomainyaml = "/var/cpanel/userdata/"+user_name+"/"+domain_name
	data_dstream = open(cpdomainyaml,'r')
	yaml_dparsed = yaml.safe_load(data_dstream)
	template_file = open("../conf/"+config_template_code+".tmpl",'r')
	config_out = open("../sites-enabled/"+domain_name+".conf",'w')
	for line in template_file:
		config_out.write(line.replace('CPANELIP',cpanel_ipv4))
		config_out.write(line.replace('DOMAINNAME',domain_name))
	template_file.close()
	config_out.close()







print main_domain
##nginx_confgen("domain_name")

print parked_domains
for domain in parked_domains:
        print domain
        ##nginx_park_domain("domain_name")

print sub_domains
print(type(sub_domains))
for domain in sub_domains:
        print domain
        ##nginx_confgen("domain_name")

