#!/usr/bin/env python

import yaml
import argparse

installation_path = "/opt/xstack" #Absolute Installation Path

#Function defs
def nginx_confgen(user_name,domain_name,config_template_code):
	"Function that generates nginx config given a domain name"
	cpdomainyaml = "/var/cpanel/userdata/"+user_name+"/"+domain_name
	cpaneldomain_data_stream = open(cpdomainyaml,'r')
	yaml_parsed_cpaneldomain = yaml.safe_load(cpaneldomain_data_stream)
	cpanel_ipv4 = yaml_parsed_cpaneldomain.get('ip')
	if 'ipv6' in yaml_parsed_cpaneldomain.keys():
		for ipv6_addr in yaml_parsed_cpaneldomain.get('ipv6').keys():
			print ipv6_addr
			cpanel_ipv6 = "listen ["+ipv6_addr+"]"
	else:
		cpanel_ipv6 = "#CPIPVSIX"
	if 'ssl' in yaml_parsed_cpaneldomain.keys():
		cpdomainyaml_ssl = "/var/cpanel/userdata/"+user_name+"/"+domain_name+"_SSL"
		cpaneldomain_ssl_data_stream = open(cpdomainyaml_ssl,'r')
		yaml_parsed_cpaneldomain_ssl = yaml.safe_load(cpaneldomain_ssl_data_stream)
		sslcertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatefile')
		sslcertificatekeyfile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatekeyfile')
		print sslcertificatefile
		print sslcertificatekeyfile
	domain_sname = yaml_parsed_cpaneldomain.get('servername')
	domain_aname = yaml_parsed_cpaneldomain.get('serveralias')
	domain_list = domain_sname+" "+domain_aname
	template_file = open(installation_path+"/conf/"+config_template_code+".tmpl",'r')
	config_out = open(installation_path+"/sites-enabled/"+domain_name+".conf",'w')
	for line in template_file:
		line = line.replace('CPANELIP',cpanel_ipv4)
		line = line.replace('DOMAINNAME',domain_list)
		line = line.replace('#CPIPVSIX',cpanel_ipv6)
		config_out.write(line)
	template_file.close()
	config_out.close()


#End Function defs

parser = argparse.ArgumentParser(description = "Regenerate nginX and app server configs for cpanel user")
parser.add_argument("CPANELUSER")
args = parser.parse_args()
cpaneluser = args.CPANELUSER

cpuserdatayaml = "/var/cpanel/userdata/"+cpaneluser+"/main"
plugin_user_datayaml = installation_path+"/userdata/"+cpaneluser

cpaneluser_data_stream = open(cpuserdatayaml,'r')
yaml_parsed_cpaneluser = yaml.safe_load(cpaneluser_data_stream)

main_domain = yaml_parsed_cpaneluser.get('main_domain')   
#parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   #This data is irrelevant as parked domain list is in ServerAlias
#addon_domains = yaml_parsed_cpaneluser.get('addon_domains')     #This data is irrelevant as addon is mapped to a subdomain
sub_domains = yaml_parsed_cpaneluser.get('sub_domains')

nginx_confgen(cpaneluser,main_domain,str(1001)) #Generate conf for main domain

for domain_in_subdomains in sub_domains:
	nginx_confgen(cpaneluser,domain_in_subdomains,str(1001)) #Generate conf for sub domains which takes care of addon as well
