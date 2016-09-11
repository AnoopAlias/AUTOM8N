#!/usr/bin/env python


import yaml
import argparse
import subprocess
import os
import sys
import pwd
import grp
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')



__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_bin = "/usr/sbin/nginx"
pagespeed_include_location = "include /etc/nginx/conf.d/pagespeed.conf"

# Function defs


def railo_vhost_add_tomcat(domain_name, document_root, *domain_aname_list):
    """Add a vhost to tomcat and restart railo-tomcat app server"""
    tomcat_conf = "/opt/railo/tomcat/conf/server.xml"
    s1 = '<Host name="'+domain_name+'" appBase="webapps"><Context path="" docBase="'+document_root+'/" />'
    s2 = ''
    for domain in domain_aname_list:
        s2 = s2+'<Alias>'+domain+'</Alias>'
        s3 = '</Host>'
        if s2:
            xmlstring = s1+s2+s3
        else:
            xmlstring = s1+s3

    new_xml_element = etree.fromstring(xmlstring)
    xml_data_stream = etree.parse(tomcat_conf)
    xml_root = xml_data_stream.getroot()
    for node1 in xml_root.iter('Service'):
        for node2 in node1.iter('Engine'):
            for node3 in node2.iter('Host'):
                if domain_name in list(node3.attrib.values()):
                    node2.remove(node3)
            node2.append(new_xml_element)
    xml_data_stream.write(tomcat_conf, xml_declaration=True, encoding='utf-8', pretty_print=True)
    subprocess.call('/opt/railo/railo_ctl restart', shell=True)
    return


def railo_vhost_add_resin(user_name, domain_name, document_root, *domain_aname_list):
    """Add a vhost to resin and restart railo-resin app server"""
    resin_conf_dir = "/var/resin/hosts/"
    if not os.path.exists(document_root+"/WEB-INF"):
        os.mkdir(document_root+"/WEB-INF", 0o770)
    if not os.path.exists(document_root+"/log"):
        os.mkdir(document_root+"/log", 0o770)
    uid_user = pwd.getpwnam(user_name).pw_uid
    uid_nobody = pwd.getpwnam("nobody").pw_uid
    gid_nobody = grp.getgrnam("nobody").gr_gid
    os.chown(document_root+"/WEB-INF", uid_user, gid_nobody)
    os.chown(document_root+"/log", uid_user, gid_nobody)
    os.chmod(document_root+"/WEB-INF", 0o770)
    os.chmod(document_root+"/log", 0o770)
    nsm = {None: "http://caucho.com/ns/resin"}
    mydict = {'id': "/", 'root-directory': document_root}
    page = etree.Element('host', nsmap=nsm)
    doc = etree.ElementTree(page)
    host_name = etree.SubElement(page, 'host-name')
    host_name.text = domain_name
    for domain in domain_aname_list:
        host_alias = etree.SubElement(page, 'host-alias')
        host_alias.text = domain
    web_app = etree.SubElement(page, 'web-app', mydict)
    if not os.path.exists(resin_conf_dir+domain_name):
        os.mkdir(resin_conf_dir+domain_name, 0o755)
    os.chown(resin_conf_dir+domain_name, uid_nobody, gid_nobody)
    host_xml_file = resin_conf_dir+domain_name+"/host.xml"
    outFile = open(host_xml_file, 'w')
    doc.write(host_xml_file, method='xml', pretty_print=True)
    outFile.close()
    os.chown(host_xml_file, uid_nobody, gid_nobody)
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


def update_config_test_status(profile_yaml, value):
    """Function to set custom profile status in domain data yaml"""
    yaml_data_stream_toupdate = open(profile_yaml, 'r')
    yaml_profile_datadict = yaml.safe_load(yaml_data_stream_toupdate)
    yaml_data_stream_toupdate.close()
    yaml_profile_datadict["testconf"] = str(value)
    with open(profile_yaml, 'w') as yaml_file:
        yaml_file.write(yaml.dump(yaml_profile_datadict, default_flow_style=False))
    yaml_file.close()
    return


def update_naxsi_test_status(profile_yaml, value):
    """Function to update naxsi wl test status"""
    yaml_data_stream_toupdate = open(profile_yaml, 'r')
    yaml_profile_datadict = yaml.safe_load(yaml_data_stream_toupdate)
    yaml_data_stream_toupdate.close()
    yaml_profile_datadict["testnaxsi"] = str(value)
    with open(profile_yaml, 'w') as yaml_file:
        yaml_file.write(yaml.dump(yaml_profile_datadict, default_flow_style=False))
    yaml_file.close()
    return


def naxsi_wl_update(domain_home, naxsi_wl_domain):
    """Function to test and accept a naxsi whitelist config file"""
    naxsi_whitelist = "/etc/nginx/sites-enabled/" + naxsi_wl_domain + ".nxapi.wl"
    wl_test_file = domain_home + '/' + naxsi_wl_domain + '.naxsi.wl.test.conf'
    if os.path.isfile(wl_test_file):
        test_config_file = open(installation_path + "/conf/nginx.conf.test.naxsi", 'r')
        test_config_out = open(installation_path + "/conf/nginx.conf." + naxsi_wl_domain + ".naxsi.test", 'w')
        config = installation_path + "/conf/nginx.conf." + naxsi_wl_domain + ".naxsi.test"
        for line in test_config_file:
            line = line.replace('NAXSI_WL_INCLUDE', wl_test_file)
            test_config_out.write(line)
        test_config_file.close()
        test_config_out.close()
        nginx_conf_test = subprocess.call("/usr/sbin/nginx -c " + config + " -t", shell=True)
        if nginx_conf_test == 0:
            wl_config_out = open(naxsi_whitelist, 'w')
            wl_config_in = open(wl_test_file, 'r')
            for line in wl_config_in:
                wl_config_out.write(line)
            wl_config_out.close()
            wl_config_in.close()


def nginx_server_reload():
    """Function to reload nginX config"""
    subprocess.call(nginx_bin + " -s reload", shell=True)
    return


def php_profile_set(user_name, domain_home):
    """Function to setup php-fpm pool for user and reload the master php-fpm"""
    phppool_file = installation_path + "/php-fpm.d/" + user_name + ".conf"
    if not os.path.isfile(phppool_file):
        fpmpool_template_file = open(installation_path+'/conf/php-fpm.pool.tmpl', 'r')
        phpfpm_config_out = open(phppool_file, 'w')
        for line in fpmpool_template_file:
            line = line.replace('CPANELUSER', user_name)
            line = line.replace('DOCUMENTROOT', domain_home+"/")
            line = line.replace('ERRORLOGFILE', domain_home+"/logs/php_error_log")
            line = line.replace('OPCACHEBLACKLIST', domain_home+"/opcache-blacklist.txt")
            phpfpm_config_out.write(line)
        fpmpool_template_file.close()
        phpfpm_config_out.close()
        subprocess.call(installation_path+"/scripts/init_backends.py reload", shell=True)
        return
    else:
        return


def nginx_confgen_profilegen(user_name, domain_name, cpanelip, document_root, sslenabled, domain_home, *domain_aname_list):
    """Function generating config include based on profile"""
    if os.path.exists("/var/cpanel/users/" + user_name):
        with open("/var/cpanel/users/" + user_name) as users_file:
            for line in users_file:
                line = line.rstrip()
                if line == "SUSPENDED=1":
                    is_suspended = 1
                    break
                else:
                    is_suspended = 0
        if is_suspended == 1:
            profileyaml = installation_path + "/conf/domain_data.suspended"
            if sslenabled == 1:
                    include_file = "/etc/nginx/sites-enabled/" + domain_name + "_SSL.include"
                    custom_config_file = domain_home + '/' + domain_name + '_SSL_nginx.include.custom.conf'
            else:
                    include_file = "/etc/nginx/sites-enabled/" + domain_name + ".include"
                    custom_config_file = domain_home + '/' + domain_name + '_nginx.include.custom.conf'
        else:
            if sslenabled == 1:
                include_file = "/etc/nginx/sites-enabled/" + domain_name + "_SSL.include"
                profileyaml = installation_path + "/domain-data/" + domain_name + "_SSL"
                custom_config_file = domain_home + '/' + domain_name + '_SSL_nginx.include.custom.conf'
            else:
                include_file = "/etc/nginx/sites-enabled/" + domain_name + ".include"
                profileyaml = installation_path + "/domain-data/" + domain_name
                custom_config_file = domain_home + '/' + domain_name + '_nginx.include.custom.conf'
        if os.path.isfile(profileyaml):
            profileyaml_data_stream = open(profileyaml, 'r')
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
            profileyaml_data_stream.close()
            profile_category = yaml_parsed_profileyaml.get('backend_category')
            profile_code = str(yaml_parsed_profileyaml.get('profile'))
            naxsi_whitelist = "/etc/nginx/sites-enabled/" + domain_name + ".nxapi.wl"
            if not os.path.isfile(naxsi_whitelist):
                subprocess.call("touch "+naxsi_whitelist, shell=True)
            naxsi_whitelist_file = "include "+naxsi_whitelist
            naxsi_status = yaml_parsed_profileyaml.get('naxsi', None)
            naxsi_test = yaml_parsed_profileyaml.get('testnaxsi', None)
            if naxsi_status == "1":
                naxsi_rules_file = "include /etc/nginx/conf.d/naxsi_active.rules"
            else:
                naxsi_rules_file = "include /etc/nginx/conf.d/naxsi_learn.rules"
            if naxsi_test == "1":
                naxsi_test_result = naxsi_wl_update(domain_home, domain_name)
                update_naxsi_test_status(profileyaml, 0)
            profile_custom_status = yaml_parsed_profileyaml.get('customconf')
            config_test_status = yaml_parsed_profileyaml.get('testconf')
            if profile_custom_status == "0" and config_test_status == "0":
                if profile_category == "PHP":
                    phpversion = yaml_parsed_profileyaml.get('backend_version')
                    php_path = yaml_parsed_profileyaml.get('backend_path')
                    pagespeed_status = str(yaml_parsed_profileyaml.get('pagespeed'))
                    if pagespeed_status == "0":
                        pagespeed_include = "#PAGESPEED_NOT_ENABLED"
                    else:
                        pagespeed_include = pagespeed_include_location
                    path_to_socket = php_path + "/var/run/" + user_name + ".sock"
                    php_profile_set(user_name, domain_home)
                    profile_template_file = open(installation_path + "/conf/" + profile_code + ".tmpl", 'r')
                    profile_config_out = open(include_file, 'w')
                    for line in profile_template_file:
                        if 'naxsi_status' in locals():
                            line = line.replace('#NAXSI_INCLUDE_FILE', naxsi_rules_file)
                            line = line.replace('#NAXSI_DOMAIN_WHITELISTS', naxsi_whitelist_file)
                        line = line.replace('CPANELIP', cpanelip)
                        line = line.replace('CPANELUSER', user_name)
                        line = line.replace('DOMAINNAME', domain_name)
                        line = line.replace('DOCUMENTROOT', document_root)
                        line = line.replace('SOCKETFILE', path_to_socket)
                        line = line.replace('#PAGESPEED_NOT_ENABLED', pagespeed_include)
                        profile_config_out.write(line)
                    profile_template_file.close()
                    profile_config_out.close()
                elif profile_category == "HHVM_NOBODY":
                    hhvm_nobody_socket = yaml_parsed_profileyaml.get('backend_path')
                    pagespeed_status = str(yaml_parsed_profileyaml.get('pagespeed'))
                    if pagespeed_status == "0":
                        pagespeed_include = "#PAGESPEED_NOT_ENABLED"
                    else:
                        pagespeed_include = pagespeed_include_location
                    profile_template_file = open(installation_path + "/conf/" + profile_code + ".tmpl", 'r')
                    profile_config_out = open(include_file, 'w')
                    for line in profile_template_file:
                        if 'naxsi_status' in locals():
                            line = line.replace('#NAXSI_INCLUDE_FILE', naxsi_rules_file)
                            line = line.replace('#NAXSI_DOMAIN_WHITELISTS', naxsi_whitelist_file)
                        line = line.replace('CPANELIP', cpanelip)
                        line = line.replace('CPANELUSER', user_name)
                        line = line.replace('DOMAINNAME', domain_name)
                        line = line.replace('DOCUMENTROOT', document_root)
                        line = line.replace('#PAGESPEED_NOT_ENABLED', pagespeed_include)
                        line = line.replace('SOCKETFILE', hhvm_nobody_socket)
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
                        if 'naxsi_status' in locals():
                            line = line.replace('#NAXSI_INCLUDE_FILE', naxsi_rules_file)
                            line = line.replace('#NAXSI_DOMAIN_WHITELISTS', naxsi_whitelist_file)
                        line = line.replace('CPANELIP', cpanelip)
                        line = line.replace('CPANELUSER', user_name)
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
                        if 'naxsi_status' in locals():
                            line = line.replace('#NAXSI_INCLUDE_FILE', naxsi_rules_file)
                            line = line.replace('#NAXSI_DOMAIN_WHITELISTS', naxsi_whitelist_file)
                        line = line.replace('CPANELIP', cpanelip)
                        line = line.replace('CPANELUSER', user_name)
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
                        if 'naxsi_status' in locals():
                            line = line.replace('#NAXSI_INCLUDE_FILE', naxsi_rules_file)
                            line = line.replace('#NAXSI_DOMAIN_WHITELISTS', naxsi_whitelist_file)
                        line = line.replace('CPANELIP', cpanelip)
                        line = line.replace('CPANELUSER', user_name)
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
                    pagespeed_status = str(yaml_parsed_profileyaml.get('pagespeed'))
                    if pagespeed_status == "0":
                        pagespeed_include = "#PAGESPEED_NOT_ENABLED"
                    else:
                        pagespeed_include = pagespeed_include_location
                    proxy_path = cpanelip + ":" + proxy_port
                    profile_template_file = open(installation_path + "/conf/" + profile_code + ".tmpl", 'r')
                    profile_config_out = open(include_file, 'w')
                    for line in profile_template_file:
                        if 'naxsi_status' in locals():
                            line = line.replace('#NAXSI_INCLUDE_FILE', naxsi_rules_file)
                            line = line.replace('#NAXSI_DOMAIN_WHITELISTS', naxsi_whitelist_file)
                        line = line.replace('CPANELIP', cpanelip)
                        line = line.replace('CPANELUSER', user_name)
                        line = line.replace('DOMAINNAME', domain_name)
                        line = line.replace('PROXYLOCATION', proxy_path)
                        line = line.replace('DOCUMENTROOT', document_root)
                        line = line.replace('#PAGESPEED_NOT_ENABLED', pagespeed_include)
                        profile_config_out.write(line)
                    profile_template_file.close()
                    profile_config_out.close()
                    if proxytype == "railo_tomcat":
                        railo_vhost_add_tomcat(domain_name, document_root, *domain_aname_list)
                    elif proxytype == "railo_resin":
                        railo_vhost_add_resin(user_name, domain_name, document_root, *domain_aname_list)
            elif config_test_status == "1":
                if os.path.isfile(custom_config_file) and 'server_name' not in open(custom_config_file).read():
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
                        update_custom_profile(profileyaml, 1)
                        update_config_test_status(profileyaml, 0)
                    else:
                        if profile_custom_status == '0':
                            update_custom_profile(profileyaml, 0)
                            update_config_test_status(profileyaml, 0)
                        else:
                            update_custom_profile(profileyaml, 1)
                            update_config_test_status(profileyaml, 0)
                else:
                    update_custom_profile(profileyaml, 0)
                    update_config_test_status(profileyaml, 0)
            else:
                if profile_category == "PHP":
                    php_profile_set(user_name, domain_home)
                    return
                else:
                    return
        else:
            if sslenabled == 1:
                try:
                    template_file = open(installation_path + "/conf/domain_data_SSL.yaml.tmpl.local", 'r')
                except IOError:
                    template_file = open(installation_path + "/conf/domain_data_SSL.yaml.tmpl", 'r')
            else:
                try:
                    template_file = open(installation_path + "/conf/domain_data.yaml.tmpl.local", 'r')
                except IOError:
                    template_file = open(installation_path + "/conf/domain_data.yaml.tmpl", 'r')
            config_out = open(profileyaml, 'w')
            for line in template_file:
                line = line.replace('CPANELUSER', user_name)
                config_out.write(line)
            template_file.close()
            config_out.close()
            cpuser_uid = pwd.getpwnam(user_name).pw_uid
            cpuser_gid = grp.getgrnam(user_name).gr_gid
            os.chown(profileyaml, cpuser_uid, cpuser_gid)
            os.chmod(profileyaml, 0o660)
            nginx_confgen_profilegen(user_name, domain_name, cpanelip, document_root, sslenabled, domain_home, *domain_aname_list)


def nginx_confgen(user_name, domain_name):
    """Function that generates nginx config given a domain name"""
    cpdomainyaml = "/var/cpanel/userdata/" + user_name + "/" + domain_name
    cpaneldomain_data_stream = open(cpdomainyaml, 'r')
    yaml_parsed_cpaneldomain = yaml.safe_load(cpaneldomain_data_stream)
    cpanel_ipv4 = yaml_parsed_cpaneldomain.get('ip')
    domain_home = yaml_parsed_cpaneldomain.get('homedir')
    document_root = yaml_parsed_cpaneldomain.get('documentroot')
    domain_sname = yaml_parsed_cpaneldomain.get('servername')
    if domain_sname.startswith("*"):
        domain_aname = domain_sname
        domain_sname = "_wildcard_."+domain_sname.replace('*.', '')
    else:
        domain_aname = yaml_parsed_cpaneldomain.get('serveralias')
    if domain_aname:
        domain_aname_list = domain_aname.split(' ')
    else:
        domain_aname_list = []
    domain_list = domain_sname + " " + domain_aname
    if 'ipv6' in list(yaml_parsed_cpaneldomain.keys()):
        if yaml_parsed_cpaneldomain.get('ipv6'):
            try:
                ipv6_addr_list = yaml_parsed_cpaneldomain.get('ipv6').keys()
                ipv6_addr = str(ipv6_addr_list[0])
            except AttributeError:
                ipv6_addr = None
        else:
            ipv6_addr = None
    else:
        ipv6_addr = None
    if os.path.isfile("/var/cpanel/userdata/" + user_name + "/" + domain_name + "_SSL"):
        cpdomainyaml_ssl = "/var/cpanel/userdata/" + user_name + "/" + domain_name + "_SSL"
        cpaneldomain_ssl_data_stream = open(cpdomainyaml_ssl, 'r')
        yaml_parsed_cpaneldomain_ssl = yaml.safe_load(cpaneldomain_ssl_data_stream)
        cpaneldomain_ssl_data_stream.close()
        sslcertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatefile')
        sslcertificatekeyfile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatekeyfile')
        sslcacertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcacertificatefile')
        if sslcacertificatefile:
            sslcombinedcert = "/etc/nginx/ssl/" + domain_name + ".crt"
            subprocess.call("cat /dev/null > " + sslcombinedcert, shell=True)
            subprocess.call("cat " + sslcertificatefile + " >> " + sslcombinedcert, shell=True)
            subprocess.call('echo "" >> ' + sslcombinedcert, shell=True)
            subprocess.call("cat " + sslcacertificatefile + " >> " + sslcombinedcert, shell=True)
            subprocess.call('echo "" >> ' + sslcombinedcert, shell=True)
            template_file = installation_path + "/conf/server_ssl_ocsp.tmpl"
        else:
            sslcombinedcert = sslcertificatefile
            template_file = installation_path + "/conf/server_ssl.tmpl"
        nginx_confgen_profilegen(user_name, domain_sname, cpanel_ipv4, document_root, 1, domain_home, *domain_aname_list)
        config_out = open("/etc/nginx/sites-enabled/" + domain_sname + "_SSL.conf", 'w')
        with open(template_file) as my_template_file:
            for line in my_template_file:
                line = line.replace('CPANELIP', cpanel_ipv4)
                line = line.replace('DOMAINLIST', domain_list)
                line = line.replace('DOMAINNAME', domain_sname)
                if ipv6_addr:
                    line = line.replace('#CPIPVSIX', "listen [" + ipv6_addr + "]")
                line = line.replace('CPANELSSLKEY', sslcertificatekeyfile)
                line = line.replace('CPANELSSLCRT', sslcombinedcert)
                if sslcacertificatefile:
                    line = line.replace('CPANELCACERT', sslcacertificatefile)
                config_out.write(line)
        config_out.close()
        my_template_file.close()
        if clusterenabled:
            for server in serverlist:
                connect_server_dict = cluster_data_yaml_parsed.get(server)
                ipmap_dict = connect_server_dict.get("ipmap")
                remote_domain_ipv4 = ipmap_dict.get(cpanel_ipv4, "127.0.0.1")
                if ipv6_addr:
                    remote_domain_ipv6 = ipmap_dict.get(ipv6_addr, "::1")
                config_out = open("/etc/nginx/"+server+"/" + domain_sname + "_SSL.conf", 'w')
                with open(template_file) as my_template_file:
                    for line in my_template_file:
                        line = line.replace('CPANELIP', remote_domain_ipv4)
                        line = line.replace('DOMAINLIST', domain_list)
                        line = line.replace('DOMAINNAME', domain_sname)
                        if ipv6_addr:
                            line = line.replace('#CPIPVSIX', "listen [" + remote_domain_ipv6 + "]")
                        line = line.replace('CPANELSSLKEY', sslcertificatekeyfile)
                        line = line.replace('CPANELSSLCRT', sslcombinedcert)
                        if sslcacertificatefile:
                            line = line.replace('CPANELCACERT', sslcacertificatefile)
                        config_out.write(line)
                    config_out.close()
                my_template_file.close()
    nginx_confgen_profilegen(user_name, domain_sname, cpanel_ipv4, document_root, 0, domain_home, *domain_aname_list)
    config_out = open("/etc/nginx/sites-enabled/" + domain_sname + ".conf", 'w')
    with open(installation_path + "/conf/server.tmpl", 'r') as my_template_file:
        for line in my_template_file:
            line = line.replace('CPANELIP', cpanel_ipv4)
            line = line.replace('DOMAINLIST', domain_list)
            line = line.replace('DOMAINNAME', domain_sname)
            if ipv6_addr:
                line = line.replace('#CPIPVSIX', "listen [" + ipv6_addr + "]")
            config_out.write(line)
        config_out.close()
    my_template_file.close()
    if clusterenabled:
        for server in serverlist:
            connect_server_dict = cluster_data_yaml_parsed.get(server)
            ipmap_dict = connect_server_dict.get("ipmap")
            remote_domain_ipv4 = ipmap_dict.get(cpanel_ipv4, "127.0.0.1")
            if ipv6_addr:
                remote_domain_ipv6 = ipmap_dict.get(ipv6_addr, "::1")
            config_out = open("/etc/nginx/"+server+"/" + domain_sname + ".conf", 'w')
            with open(installation_path + "/conf/server.tmpl", 'r') as my_template_file:
                for line in my_template_file:
                    line = line.replace('CPANELIP', remote_domain_ipv4)
                    line = line.replace('DOMAINLIST', domain_list)
                    line = line.replace('DOMAINNAME', domain_sname)
                    if ipv6_addr:
                        line = line.replace('#CPIPVSIX', "listen [" + remote_domain_ipv6 + "]")
                    config_out.write(line)
                config_out.close()
            my_template_file.close()
    if clusterenabled:
        for server in serverlist:
            subprocess.call("rsync -a /etc/nginx/sites-enabled/*.{include,nxapi.wl} /etc/nginx/"+server+"/", shell=True)
    nginx_server_reload()


# End Function defs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenerate nginX and app server configs for cpanel user")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER

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
        if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
            clusterenabled = True
            cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            serverlist = cluster_data_yaml_parsed.keys()
        else:
            clusterenabled = None

        nginx_confgen(cpaneluser, main_domain)  # Generate conf for main domain

        for domain_in_subdomains in sub_domains:
            nginx_confgen(cpaneluser, domain_in_subdomains)  # Generate conf for sub domains which takes care of addon as well
