#!/usr/bin/env python


import yaml
import argparse
import subprocess
import os
from lxml import etree


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_bin = "/usr/sbin/nginx"
pagespeed_include_location = "include /etc/nginx/conf.d/pagespeed.conf"

# Function defs


def cpanel_nginx_awstats_fix(awstats_custom_conf, cpaneluser):
    """cPanel nginx awstats fix .Thanks to https://github.com/lucasRolff/cpanel-nginx-awstats"""
    file_content = """\
    LogFormat="%host %other %logname %time1 %methodurl %code %bytesd %refererquot %uaquot %extra1"
    ExtraSectionName1="Time to serve requests (seconds)"
    ExtraSectionCodeFilter1=""
    ExtraSectionFirstColumnTitle1="Number of seconds to serve the request"
    ExtraSectionFirstColumnValues1="extra1,(.*)"
    ExtraSectionStatTypes1="H"
    ExtraTrackedRowsLimit=100000
    """
    with open(awstats_custom_conf, 'w') as f:
		f.write(file_content)
    f.close()
    subprocess.call("chown "+cpaneluser+":"+cpaneluser+" "+awstats_custom_conf, shell=True)
    return



def railo_vhost_add(domain_name, document_root, *domain_aname_list):
    """Add a vhost to railo and restart railo app server"""
    tomcat_conf = "/opt/railo/tomcat/conf/server.xml"
    s1='<Host name="'+domain_name+'" appBase="webapps"><Context path="" docBase="'+document_root+'/" />'
    s2=''
    for domain in domain_aname_list:
        s2=s2+'<Alias>'+domain+'</Alias>'
	s3='</Host>'
	if s2:
	    xmlstring = s1+s2+s3
	else:
	    xmlstring = s1+s3
            
    new_xml_element=etree.fromstring(xmlstring)
    xml_data_stream = etree.parse(tomcat_conf)
    xml_root = xml_data_stream.getroot()
    for node1 in xml_root.iter('Service'):
	for node2 in node1.iter('Engine'):
            for node3 in node2.iter('Host'):
                if domain_name in node3.attrib.values():
                    node2.remove(node3)
	    node2.append(new_xml_element)
    xml_data_stream.write(tomcat_conf, xml_declaration=True, encoding='utf-8', pretty_print=True)
    subprocess.call('/opt/railo/railo_ctl restart', shell=True)
    return


def update_custom_profile(profile_yaml, value):
    """Function to set custom profile status in domain data yaml"""
    yaml_data_stream_toupdate = open(profile_yaml, 'r')
    yaml_profile_datadict = yaml.safe_load(yaml_data_stream_toupdate)
    yaml_data_stream_toupdate.close()
    yaml_profile_datadict["customconf"] = str(value)
    with open(profile_yaml, 'w') as yaml_file:
        yaml_file.write(yaml.dump(yaml_profile_datadict, default_flow_style=False))
    yaml_file.close()
    return


def nginx_server_reload():
    """Function to reload nginX config"""
    subprocess.call(nginx_bin + " -s reload", shell=True)
    return


def php_profile_set(user_name, phpversion, php_path):
    """Function to setup php-fpm pool for user and restart the master php-fpm"""
    phppool_file = php_path + "/etc/fpm.d/" + user_name + ".conf"
    if os.path.isfile(phppool_file):
        subprocess.call("kill -USR2 `cat " + php_path + "/var/run/php-fpm.pid`", shell=True)
    else:
        sed_string='sed "s/CPANELUSER/' + user_name + '/g" ' + installation_path + '/conf/php-fpm.pool.tmpl > ' + phppool_file
        subprocess.call(sed_string, shell=True)
        subprocess.call("kill -USR2 `cat " + php_path + "/var/run/php-fpm.pid`", shell=True)
    return


def nginx_confgen_profilegen(user_name, domain_name, cpanelip, document_root, sslenabled, domain_home, *domain_aname_list):
    """Function generating config include based on profile"""
    with open("/var/cpanel/users/" + user_name) as users_file:
        if "SUSPENDED=1" in users_file.read():
            profileyaml = installation_path + "/conf/domain_data.suspended"
            if sslenabled == 1:
                include_file = "/etc/nginx/sites-enabled/" + domain_name + "_ssl.include"
            else:
                include_file = "/etc/nginx/sites-enabled/" + domain_name + ".include"
        else:
            if sslenabled == 1:
                include_file = "/etc/nginx/sites-enabled/" + domain_name + "_ssl.include"
                profileyaml = installation_path + "/domain-data/" + domain_name + "_ssl"
            else:
                include_file = "/etc/nginx/sites-enabled/" + domain_name + ".include"
                profileyaml = installation_path + "/domain-data/" + domain_name
    if os.path.isfile(profileyaml):
        profileyaml_data_stream = open(profileyaml, 'r')
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        profile_custom_status = yaml_parsed_profileyaml.get('customconf')
        if profile_custom_status == "0":
            profile_category = yaml_parsed_profileyaml.get('backend_category')
            profile_code = str(yaml_parsed_profileyaml.get('profile'))
            if profile_category == "PHP":
                phpversion = yaml_parsed_profileyaml.get('backend_version')
                php_path = yaml_parsed_profileyaml.get('backend_path')
                pagespeed_status = str(yaml_parsed_profileyaml.get('pagespeed'))
                if pagespeed_status == "0":
                    pagespeed_include = "#PAGESPEED_NOT_ENABLED"
                else:
                    pagespeed_include = pagespeed_include_location
                path_to_socket = php_path + "/var/run/" + user_name + ".sock"
                php_profile_set(user_name, phpversion, php_path)
                profile_template_file = open(installation_path + "/conf/" + profile_code + ".tmpl", 'r')
                profile_config_out = open(include_file, 'w')
                for line in profile_template_file:
                    line = line.replace('CPANELIP', cpanelip)
                    line = line.replace('DOMAINNAME', domain_name)
                    line = line.replace('DOCUMENTROOT', document_root)
                    line = line.replace('SOCKETFILE', path_to_socket)
                    line = line.replace('#PAGESPEED_NOT_ENABLED', pagespeed_include)
                    profile_config_out.write(line)
                profile_template_file.close()
                profile_config_out.close()
            elif profile_category == "RUBY":
                ruby_path = yaml_parsed_profileyaml.get('backend_path')
                pagespeed_status = str(yaml_parsed_profileyaml.get('pagespeed'))
                if pagespeed_status == "0":
                    pagespeed_include = "#PAGESPEED_NOT_ENABLED"
                else:
                    pagespeed_include = pagespeed_include_location
                profile_template_file = open(installation_path + "/conf/" + profile_code + ".tmpl", 'r')
                profile_config_out = open(include_file, 'w')
                for line in profile_template_file:
                    line = line.replace('CPANELIP', cpanelip)
                    line = line.replace('DOMAINNAME', domain_name)
                    line = line.replace('DOCUMENTROOT', document_root)
                    line = line.replace('#PAGESPEED_NOT_ENABLED', pagespeed_include)
                    line = line.replace('PATHTORUBY', ruby_path)
                    profile_config_out.write(line)
                profile_template_file.close()
                profile_config_out.close()
            elif profile_category == "PYTHON":
                python_path = yaml_parsed_profileyaml.get('backend_path')
                pagespeed_status = str(yaml_parsed_profileyaml.get('pagespeed'))
                if pagespeed_status == "0":
                    pagespeed_include = "#PAGESPEED_NOT_ENABLED"
                else:
                    pagespeed_include = pagespeed_include_location
                profile_template_file = open(installation_path + "/conf/" + profile_code + ".tmpl", 'r')
                profile_config_out = open(include_file, 'w')
                for line in profile_template_file:
                    line = line.replace('CPANELIP', cpanelip)
                    line = line.replace('DOMAINNAME', domain_name)
                    line = line.replace('DOCUMENTROOT', document_root)
                    line = line.replace('#PAGESPEED_NOT_ENABLED', pagespeed_include)
                    line = line.replace('PATHTOPYTHON', python_path)
                    profile_config_out.write(line)
                profile_template_file.close()
                profile_config_out.close()
            elif profile_category == "NODEJS":
                nodejs_path = yaml_parsed_profileyaml.get('backend_path')
                pagespeed_status = str(yaml_parsed_profileyaml.get('pagespeed'))
                if pagespeed_status == "0":
                    pagespeed_include = "#PAGESPEED_NOT_ENABLED"
                else:
                    pagespeed_include = pagespeed_include_location
                profile_template_file = open(installation_path + "/conf/" + profile_code + ".tmpl", 'r')
                profile_config_out = open(include_file, 'w')
                for line in profile_template_file:
                    line = line.replace('CPANELIP', cpanelip)
                    line = line.replace('DOMAINNAME', domain_name)
                    line = line.replace('DOCUMENTROOT', document_root)
                    line = line.replace('#PAGESPEED_NOT_ENABLED', pagespeed_include)
                    line = line.replace('PATHTONODEJS', nodejs_path)
                    profile_config_out.write(line)
                profile_template_file.close()
                profile_config_out.close()
            else:
		proxytype = yaml_parsed_profileyaml.get('backend_version')
                proxy_port = str(yaml_parsed_profileyaml.get('backend_path'))
                proxy_path = cpanelip + ":" + proxy_port
                profile_template_file = open(installation_path + "/conf/" + profile_code + ".tmpl", 'r')
                profile_config_out = open(include_file, 'w')
                for line in profile_template_file:
                    line = line.replace('CPANELIP', cpanelip)
		    line = line.replace('DOMAINNAME', domain_name)
                    line = line.replace('PROXYLOCATION', proxy_path)
                    profile_config_out.write(line)
                profile_template_file.close()
                profile_config_out.close()
		if proxytype == "railo":
			railo_vhost_add(domain_name,document_root,*domain_aname_list)
        elif profile_custom_status == "1":
            custom_config_file = domain_home + '/.' + domain_name + '_nginx.include.custom.conf'
            if os.path.isfile(custom_config_file):
                test_config_file = open(installation_path + "/conf/nginx.conf.test", 'r')
                test_config_out = open(installation_path + "/conf/nginx.conf." + domain_name + ".test", 'w')
                config = installation_path + "/conf/nginx.conf." + domain_name + ".test"
                for line in test_config_file:
                    line = line.replace('NGINX_INCLUDE', custom_config_file)
                    test_config_out.write(line)
                test_config_file.close()
                test_config_file.close()
                test_config_out.close()
                nginx_conf_test = subprocess.call("/usr/sbin/nginx -c " + config + " -t", shell=True)
                if nginx_conf_test == 0:
                    profile_config_out = open(include_file, 'w')
                    profile_config_in = open(custom_config_file, 'r')
                    for line in profile_config_in:
                        profile_config_out.write(line)
                    profile_config_out.close()
                    profile_config_in.close()
                    update_custom_profile(profileyaml, 2)
                else:
                    update_custom_profile(profileyaml, 0)

            else:
                update_custom_profile(profileyaml, 0)
        else:
            return
    else:
        template_file = open(installation_path + "/conf/domain_data.yaml.tmpl", 'r')
        config_out = open(profileyaml, 'w')
        for line in template_file:
            line = line.replace('CPANELUSER', user_name)
            config_out.write(line)
        template_file.close()
        config_out.close()
        subprocess.call("chown " + user_name + ":" + user_name + " " + profileyaml, shell=True)
        nginx_confgen_profilegen(user_name, domain_name, cpanelip, document_root, sslenabled, domain_home, *domain_aname_list)


def nginx_confgen(user_name, domain_name):
    """Function that generates nginx config given a domain name"""
    cpdomainyaml = "/var/cpanel/userdata/" + user_name + "/" + domain_name
    cpaneldomain_data_stream = open(cpdomainyaml, 'r')
    yaml_parsed_cpaneldomain = yaml.safe_load(cpaneldomain_data_stream)
    cpanel_ipv4 = yaml_parsed_cpaneldomain.get('ip')
    domain_home = yaml_parsed_cpaneldomain.get('homedir')
    awstats_dir=domain_home+"/tmp/awstats"
    awstats_custom_conf=domain_home+"/tmp/awstats/awstats.conf.include"
    if os.path.exists(awstats_dir):
    	if not os.path.isfile(awstats_custom_conf):
		cpanel_nginx_awstats_fix(awstats_custom_conf, user_name)
    document_root = yaml_parsed_cpaneldomain.get('documentroot')
    domain_sname = yaml_parsed_cpaneldomain.get('servername')
    domain_aname = yaml_parsed_cpaneldomain.get('serveralias')
    domain_aname_list = domain_aname.split(' ')
    domain_list = domain_sname + " " + domain_aname
    if 'ipv6' in yaml_parsed_cpaneldomain.keys():
	if yaml_parsed_cpaneldomain.get('ipv6'):
        	for ipv6_addr in yaml_parsed_cpaneldomain.get('ipv6').keys():
            		cpanel_ipv6 = "listen [" + ipv6_addr + "]"
	else:
		cpanel_ipv6 = "#CPIPVSIX"
    else:
        cpanel_ipv6 = "#CPIPVSIX"
    if os.path.isfile("/var/cpanel/userdata/" + user_name + "/" + domain_name + "_SSL"):
        cpdomainyaml_ssl = "/var/cpanel/userdata/" + user_name + "/" + domain_name + "_SSL"
        cpaneldomain_ssl_data_stream = open(cpdomainyaml_ssl, 'r')
        yaml_parsed_cpaneldomain_ssl = yaml.safe_load(cpaneldomain_ssl_data_stream)
        sslcertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatefile')
        sslcertificatekeyfile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatekeyfile')
        sslcacertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcacertificatefile')
        sslcombinedcert = "/etc/nginx/ssl/" + domain_name + ".crt"
        subprocess.call("cat /dev/null > " + sslcombinedcert, shell=True)
        if sslcacertificatefile:
            subprocess.call("cat " + sslcertificatefile + " " + sslcacertificatefile + " >> " + sslcombinedcert,
                            shell=True)
        else:
            subprocess.call("cat " + sslcertificatefile + " >> " + sslcombinedcert, shell=True)
        nginx_confgen_profilegen(user_name, domain_sname, cpanel_ipv4, document_root, 1, domain_home, *domain_aname_list)
        template_file = open(installation_path + "/conf/server_ssl.tmpl", 'r')
        config_out = open("/etc/nginx/sites-enabled/" + domain_name + "_SSL.conf", 'w')
        for line in template_file:
            line = line.replace('CPANELIP', cpanel_ipv4)
            line = line.replace('DOMAINLIST', domain_list)
            line = line.replace('DOMAINNAME', domain_sname)
            line = line.replace('#CPIPVSIX', cpanel_ipv6)
            line = line.replace('CPANELSSLKEY', sslcertificatekeyfile)
            line = line.replace('CPANELSSLCRT', sslcombinedcert)
            config_out.write(line)
        template_file.close()
        config_out.close()
    nginx_confgen_profilegen(user_name, domain_sname, cpanel_ipv4, document_root, 0, domain_home, *domain_aname_list)
    template_file = open(installation_path + "/conf/server.tmpl", 'r')
    config_out = open("/etc/nginx/sites-enabled/" + domain_name + ".conf", 'w')
    for line in template_file:
        line = line.replace('CPANELIP', cpanel_ipv4)
        line = line.replace('DOMAINLIST', domain_list)
        line = line.replace('DOMAINNAME', domain_sname)
        line = line.replace('#CPIPVSIX', cpanel_ipv6)
        config_out.write(line)
    template_file.close()
    config_out.close()
    nginx_server_reload()


# End Function defs


parser = argparse.ArgumentParser(description="Regenerate nginX and app server configs for cpanel user")
parser.add_argument("CPANELUSER")
args = parser.parse_args()
cpaneluser = args.CPANELUSER

cpuserdatayaml = "/var/cpanel/userdata/" + cpaneluser + "/main"
cpaneluser_data_stream = open(cpuserdatayaml, 'r')
yaml_parsed_cpaneluser = yaml.safe_load(cpaneluser_data_stream)

main_domain = yaml_parsed_cpaneluser.get('main_domain')
#parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   #This data is irrelevant as parked domain list is in ServerAlias
#addon_domains = yaml_parsed_cpaneluser.get('addon_domains')     #This data is irrelevant as addon is mapped to a subdomain
sub_domains = yaml_parsed_cpaneluser.get('sub_domains')

nginx_confgen(cpaneluser, main_domain)  #Generate conf for main domain

for domain_in_subdomains in sub_domains:
    nginx_confgen(cpaneluser, domain_in_subdomains)  #Generate conf for sub domains which takes care of addon as well
