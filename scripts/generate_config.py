#!/usr/bin/env python


import yaml
import argparse
import subprocess
import os
import sys
import pwd
import grp
import shutil
from lxml import etree
import jinja2
from hashlib import md5
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_bin = "/usr/sbin/nginx"


# Function definitions


# Railo is probably dead.Checkout http://lucee.org/ for a fork
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
    # enabling shell as Railo probably needs shell vars like CATALINA_HOME
    subprocess.Popen(['/opt/railo/railo_ctl', 'restart'], shell=True)
    return


# Railo is probably dead.Checkout http://lucee.org/ for a fork
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


def php_backend_add(user_name, domain_home):
    """Function to setup php-fpm pool for user and reload the master php-fpm"""
    phppool_file = installation_path + "/php-fpm.d/" + user_name + ".conf"
    if not os.path.isfile(phppool_file):
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "php-fpm.pool.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {"CPANELUSER": user_name,
                        "HOMEDIR": domain_home
                        }
        generated_config = template.render(templateVars)
        with open(phppool_file, "w") as confout:
            confout.write(generated_config)
        control_script = installation_path+"/scripts/init_backends.py"
        subprocess.Popen([control_script, 'reload'])
        return
    else:
        return


def nginx_confgen(is_suspended, clusterenabled, *cluster_serverlist, **kwargs):
    """Function that generates nginx config """
    # Initiate Jinja2 templateEnv
    templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    # Get all Data from cPanel userdata files
    cpdomainjson = "/var/cpanel/userdata/" + kwargs.get('configuser') + "/" + kwargs.get('maindomain') + ".cache"
    with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
        json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
    cpanel_ipv4 = json_parsed_cpaneldomain.get('ip')
    domain_home = json_parsed_cpaneldomain.get('homedir')
    document_root = json_parsed_cpaneldomain.get('documentroot')
    domain_server_name = json_parsed_cpaneldomain.get('servername')
    domain_alias_name = json_parsed_cpaneldomain.get('serveralias')
    if domain_alias_name:
        serveralias_list = domain_alias_name.split(' ')
    else:
        serveralias_list = []
    domain_list = domain_server_name + " " + domain_alias_name
    if json_parsed_cpaneldomain.get('ipv6'):
        try:
            ipv6_addr_list = json_parsed_cpaneldomain.get('ipv6').keys()
            ipv6_addr = str(ipv6_addr_list[0])
            hasipv6 = True
        except AttributeError:
            hasipv6 = False
            ipv6_addr = None
    else:
        hasipv6 = False
        ipv6_addr = None
    # if domain has TLS, get details about it too
    if os.path.isfile("/var/cpanel/userdata/" + kwargs.get('configuser') + "/" + kwargs.get('maindomain') + "_SSL"):
        hasssl = True
        cpdomainjson_ssl = "/var/cpanel/userdata/" + kwargs.get('configuser') + "/" + kwargs.get('maindomain') + "_SSL.cache"
        with open(cpdomainjson_ssl, 'r') as cpaneldomain_ssl_data_stream:
            json_parsed_cpaneldomain_ssl = json.load(cpaneldomain_ssl_data_stream)
        sslcertificatefile = json_parsed_cpaneldomain_ssl.get('sslcertificatefile')
        sslcertificatekeyfile = json_parsed_cpaneldomain_ssl.get('sslcertificatekeyfile')
        sslcacertificatefile = json_parsed_cpaneldomain_ssl.get('sslcacertificatefile')
        if sslcacertificatefile:
            sslcombinedcert = "/etc/nginx/ssl/" + kwargs.get('configdomain') + ".crt"
            ocsp = True
            filenames = [sslcertificatefile, sslcacertificatefile]
            with open(sslcombinedcert, 'w') as outfile:
                for fname in filenames:
                    with open(fname) as infile:
                        outfile.write(infile.read()+"\n")
        else:
            sslcombinedcert = sslcertificatefile
            ocsp = False
    else:
        hasssl = False
        ocsp = False
        sslcombinedcert = None
        sslcertificatefile = None
        sslcacertificatefile = None
        sslcertificatekeyfile = None
    # Get all data from nDeploy domain-data file
    if is_suspended:
        domain_data_file = installation_path + "/conf/domain_data.suspended"
    else:
        domain_data_file = installation_path + "/domain-data/" + kwargs.get('configdomain')
    if not os.path.isfile(domain_data_file):
        TEMPLATE_FILE = installation_path+"/conf/domain_data_default.yaml"
        shutil.copyfile(TEMPLATE_FILE, domain_data_file)
        cpuser_uid = pwd.getpwnam(kwargs.get('configuser')).pw_uid
        cpuser_gid = grp.getgrnam(kwargs.get('configuser')).gr_gid
        os.chown(domain_data_file, cpuser_uid, cpuser_gid)
        os.chmod(domain_data_file, 0o660)
    with open(domain_data_file, 'r') as domain_data_stream:
        yaml_parsed_domain_data = yaml.safe_load(domain_data_stream)
    # Following are the backend details that can be changed from the UI
    backend_category = yaml_parsed_domain_data.get('backend_category', None)
    apptemplate_code = str(yaml_parsed_domain_data.get('apptemplate_code', None))
    backend_path = yaml_parsed_domain_data.get('backend_path', None)
    backend_version = yaml_parsed_domain_data.get('backend_version', None)
    # Following are features that the UI can change . Can be expanded in future
    # as and when more features are incorporated
    naxsi = yaml_parsed_domain_data.get('naxsi', None)
    if naxsi:
        if not os.path.isfile("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+".wl"):
            os.mknod("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+".wl")
    pagespeed = yaml_parsed_domain_data.get('pagespeed', None)
    wwwredirect = yaml_parsed_domain_data.get('wwwredirect', None)
    autoindex = yaml_parsed_domain_data.get('autoindex', None)
    redirect_to_ssl = yaml_parsed_domain_data.get('redirect_to_ssl', None)
    clickjacking_protect = yaml_parsed_domain_data.get('clickjacking_protect', None)
    disable_contenttype_sniffing = yaml_parsed_domain_data.get('disable_contenttype_sniffing', None)
    xss_filter = yaml_parsed_domain_data.get('xss_filter', None)
    content_security_policy = yaml_parsed_domain_data.get('content_security_policy', None)
    hsts = yaml_parsed_domain_data.get('hsts', None)
    brotli = yaml_parsed_domain_data.get('brotli', None)
    gzip = yaml_parsed_domain_data.get('gzip', None)
    http2 = yaml_parsed_domain_data.get('http2', None)
    ssl_offload = yaml_parsed_domain_data.get('ssl_offload', None)
    disable_access_log = yaml_parsed_domain_data.get('disable_access_log', None)
    naxsi_mode = yaml_parsed_domain_data.get('naxsi_mode', None)
    disable_open_file_cache = yaml_parsed_domain_data.get('disable_open_file_cache', None)
    protected_dir = yaml_parsed_domain_data.get('protected_dir')
    if not protected_dir:
        protected_dir = []
    subdir_apps = yaml_parsed_domain_data.get('subdir_apps')
    if subdir_apps:
        subdir_apps_uniq = {}
        for key in subdir_apps.keys():
            uniq_path = document_root+key
            uniq_filename = md5(uniq_path.encode("utf-8")).hexdigest()
            subdir_apps_uniq[key] = uniq_filename
    else:
        subdir_apps = {}
        subdir_apps_uniq = {}
    # Since we have all data needed ,lets render the conf to a file
    TEMPLATE_FILE = "server.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)
    templateVars = {"OCSP": ocsp,
                    "SSL": hasssl,
                    "IPVSIX": hasipv6,
                    "WWWREDIRECT": wwwredirect,
                    "CPANELIP": cpanel_ipv4,
                    "CPIPVSIX": ipv6_addr,
                    "IPVSIX": hasipv6,
                    "HTTP2": http2,
                    "CPANELSSLCRT": sslcombinedcert,
                    "CPANELSSLKEY": sslcertificatekeyfile,
                    "CPANELCACERT": sslcacertificatefile,
                    "MAINDOMAINNAME": kwargs.get('maindomain'),
                    "CONFIGDOMAINNAME": kwargs.get('configdomain'),
                    "NAXSI": naxsi,
                    "NAXSIMODE": naxsi_mode,
                    "PAGESPEED": pagespeed,
                    "CLICKJACKING_PROTECT": clickjacking_protect,
                    "DISABLE_CONTENTTYPE_SNIFFING": disable_contenttype_sniffing,
                    "XSS_FILTER": xss_filter,
                    "GZIP_ENABLED": gzip,
                    "BROTLI_ENABLED": brotli,
                    "CONTENT_SECURITY_POLICY": content_security_policy,
                    "HSTS": hsts,
                    "DOMAINLIST": domain_list,
                    "AUTOINDEX": autoindex,
                    "REDIRECT_TO_SSL": redirect_to_ssl,
                    "DISABLELOG": disable_access_log,
                    "DISABLE_OPEN_FILE_CACHE": disable_open_file_cache,
                    "PROTECTED_DIR": protected_dir,
                    "HOMEDIR": domain_home
                    }
    generated_config = template.render(templateVars)
    with open("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+".conf", "w") as confout:
        confout.write(generated_config)
    # If a cluster is setup.Generate nginx config for other servers as well
    if clusterenabled:
        for server in cluster_serverlist:
            connect_server_dict = cluster_data_yaml_parsed.get(server)
            ipmap_dict = connect_server_dict.get("ipmap")
            remote_domain_ipv4 = ipmap_dict.get(cpanel_ipv4, "127.0.0.1")
            if ipv6_addr:
                remote_domain_ipv6 = ipmap_dict.get(ipv6_addr, "::1")
            cluster_config_out = "/etc/nginx/"+server+"/" + kwargs.get('configdomain') + ".conf"
            clustertemplateVars = {"OCSP": ocsp,
                                   "SSL": hasssl,
                                   "IPVSIX": hasipv6,
                                   "WWWREDIRECT": wwwredirect,
                                   "CPANELIP": remote_domain_ipv4,
                                   "CPIPVSIX": remote_domain_ipv6,
                                   "IPVSIX": hasipv6,
                                   "HTTP2": http2,
                                   "CPANELSSLCRT": sslcombinedcert,
                                   "CPANELSSLKEY": sslcertificatekeyfile,
                                   "CPANELCACERT": sslcacertificatefile,
                                   "MAINDOMAINNAME": kwargs.get('maindomain'),
                                   "CONFIGDOMAINNAME": kwargs.get('configdomain'),
                                   "NAXSI": naxsi,
                                   "NAXSIMODE": naxsi_mode,
                                   "PAGESPEED": pagespeed,
                                   "CLICKJACKING_PROTECT": clickjacking_protect,
                                   "DISABLE_CONTENTTYPE_SNIFFING": disable_contenttype_sniffing,
                                   "XSS_FILTER": xss_filter,
                                   "GZIP_ENABLED": gzip,
                                   "BROTLI_ENABLED": brotli,
                                   "CONTENT_SECURITY_POLICY": content_security_policy,
                                   "HSTS": hsts,
                                   "DOMAINLIST": domain_list,
                                   "AUTOINDEX": autoindex,
                                   "REDIRECT_TO_SSL": redirect_to_ssl,
                                   "DISABLELOG": disable_access_log,
                                   "DISABLE_OPEN_FILE_CACHE": disable_open_file_cache,
                                   "PROTECTED_DIR": protected_dir,
                                   "HOMEDIR": domain_home
                                   }
            cluster_generated_config = template.render(clustertemplateVars)
            with open(cluster_config_out, "w") as confout:
                confout.write(cluster_generated_config)
    # Generate the rest of the config(domain.include) based on the application template
    apptemplate = templateEnv.get_template(apptemplate_code)
    if backend_category == 'PROXY':
        if backend_version == 'httpd':
            apptemplateVars = {"SSL_OFFLOAD": ssl_offload,
                               "CPANELIP": cpanel_ipv4
                               }
        elif backend_version == 'railo_tomcat':
            apptemplateVars = {"UPSTREAM_PORT": backend_path,
                               "CPANELIP": cpanel_ipv4
                               }
            railo_vhost_add_tomcat(domain_server_name, document_root, *serveralias_list)
        elif backend_version == 'railo_resin':
            apptemplateVars = {"UPSTREAM_PORT": backend_path,
                               "CPANELIP": cpanel_ipv4
                               }
            railo_vhost_add_resin(kwargs.get('configuser'), domain_server_name, document_root, *serveralias_list)
    elif backend_category == 'PHP':
        path_to_socket = backend_path + "/var/run/" + kwargs.get('configuser') + ".sock"
        apptemplateVars = {"DOCUMENTROOT": document_root,
                           "SOCKETFILE": path_to_socket,
                           "SUBDIRAPPS": subdir_apps_uniq
                           }
        if not os.path.isfile(path_to_socket):
            php_backend_add(kwargs.get('configuser'), domain_home)
    elif backend_category == 'PYTHON':
        apptemplateVars = {"DOCUMENTROOT": document_root,
                           "PATHTOPYTHON": backend_path
                           }
    elif backend_category == 'RUBY':
        apptemplateVars = {"DOCUMENTROOT": document_root,
                           "PATHTORUBY": backend_path
                           }
    elif backend_category == 'NODEJS':
        apptemplateVars = {"DOCUMENTROOT": document_root,
                           "PATHTONODEJS": backend_path
                           }
    elif backend_category == 'HHVM_NOBODY':
        apptemplateVars = {"DOCUMENTROOT": document_root,
                           "SOCKETFILE": backend_path
                           }
    generated_app_config = apptemplate.render(apptemplateVars)
    with open("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+".include", "w") as confout:
        confout.write(generated_app_config)
    # Get the subdir config also rendered
    if subdir_apps:
        for key, value in subdir_apps.iteritems():
            subdirApptemplate = templateEnv.get_template(value)
            subdirApptemplateVars = {"DOCUMENTROOT": document_root,
                                     "SUBDIR": key
                                     }
            generated_subdir_app_config = subdirApptemplate.render(subdirApptemplateVars)
            with open("/etc/nginx/sites-enabled/"+subdir_apps_uniq.get(key)+".include", "w") as confout:
                confout.write(generated_subdir_app_config)


# End Function defs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate nginX and app server configs for cpanel user")
    parser.add_argument("CPANELUSER")
    args = parser.parse_args()
    cpaneluser = args.CPANELUSER
    # if user is not in /etc/passwd we dont proceed any further
    try:
        pwd.getpwnam(cpaneluser)
    except KeyError:
        sys.exit(0)
    else:
        # Try loading the main userdata cache file
        cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
        with open(cpuserdatajson) as cpaneluser_data_stream:
            json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
        main_domain = json_parsed_cpaneluser.get('main_domain')
        # parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   # This data is irrelevant as parked domain list is in ServerAlias
        addon_domains_dict = json_parsed_cpaneluser.get('addon_domains')     # So we know which addon is mapped to which sub-domain
        sub_domains = json_parsed_cpaneluser.get('sub_domains')
        # Check if a user is suspended and set a flag accordingly
        if os.path.exists("/var/cpanel/users/" + cpaneluser):
            with open("/var/cpanel/users/" + cpaneluser) as users_file:
                for line in users_file:
                    line = line.rstrip()
                    if line == "SUSPENDED=1":
                        is_suspended = True
                        break
                    else:
                        is_suspended = False
        else:
            # If cpanel users file is not present silently exit
            sys.exit(0)
        # If nDeploy cluster is enabled we set a global flag and generate a list of servers in the serverlist list
        if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):
            clusterenabled = True
            cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
            cluster_data_yaml = open(cluster_config_file, 'r')
            cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
            cluster_data_yaml.close()
            cluster_serverlist = cluster_data_yaml_parsed.keys()
        else:
            clusterenabled = False
            cluster_serverlist = []
        # Begin config generation .Do it first for the main domain
        nginx_confgen(is_suspended, clusterenabled, *cluster_serverlist, configuser=cpaneluser, configdomain=main_domain, maindomain=main_domain)  # Generate conf for main domain
        # iterate over the addon-domain ,passing the subdomain as the configdomain
        for the_addon_domain in addon_domains_dict.keys():
            nginx_confgen(is_suspended, clusterenabled, *cluster_serverlist, configuser=cpaneluser, configdomain=addon_domains_dict.get(the_addon_domain), maindomain=the_addon_domain)  # Generate conf for sub domains which takes care of addon as well
        # iterate over sub-domains and generate config if its not a linked sub-domain for addon-domain
        for the_sub_domain in sub_domains:
            if the_sub_domain not in addon_domains_dict.values():
                if the_sub_domain.startswith("*"):
                    subdom_config_dom = "_wildcard_."+the_sub_domain.replace('*.', '')
                    nginx_confgen(is_suspended, clusterenabled, *cluster_serverlist, configuser=cpaneluser, configdomain=subdom_config_dom, maindomain=the_sub_domain)
                else:
                    nginx_confgen(is_suspended, clusterenabled, *cluster_serverlist, configuser=cpaneluser, configdomain=the_sub_domain, maindomain=the_sub_domain)
        # Ok we are done generating .Lets reload nginx and some misc things ( Using async Popen whenever possible )
        subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'])
        if clusterenabled:
            for server in cluster_serverlist:
                target_dir = "/etc/nginx/"+server+"/"
                subprocess.Popen(['/usr/bin/rsync', '-a', '/etc/nginx/sites-enabled/*.{include,nxapi.wl}', target_dir])
