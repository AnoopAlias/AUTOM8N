#!/usr/bin/env python

import codecs
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
import json
import time


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
nginx_bin = "/usr/sbin/nginx"


# Function definitions

# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


# Railo is probably dead.Checkout http://lucee.org/ for a fork
def railo_vhost_add_tomcat(domain_name, document_root, *domain_aname_list):
    """Add a vhost to tomcat and restart railo-tomcat app server"""
    tomcat_conf = "/opt/lucee/tomcat/conf/server.xml"
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
    if not os.path.isfile(installation_path+'/conf/skip_tomcat_reload'):
        subprocess.Popen(['/opt/lucee/lucee_ctl', 'restart'], shell=True)
    return


def java_vhost_add_tomcat(domain_name, document_root, *domain_aname_list):
    """Add a vhost to tomcat and restart tomcat app server"""
    tomcat_conf = "/etc/tomcat/server.xml"
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
    if not os.path.isfile(installation_path+'/conf/skip_tomcat_reload'):
        subprocess.Popen('service tomcat restart', shell=True)
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
        # cPanel ea-php includes chroot patch
        # One just need to create the file /var/cpanel/feature_toggles/apachefpmjail for chroot
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "php-fpm.pool.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {"CPANELUSER": user_name,
                        "HOMEDIR": domain_home,
                        }
        generated_config = template.render(templateVars)
        with codecs.open(phppool_file, 'w', 'utf-8') as confout:
            confout.write(generated_config)
        if not os.path.isfile(installation_path+'/conf/skip_php-fpm_reload'):
            control_script = installation_path+"/scripts/init_backends.py"
            subprocess.Popen([control_script, 'reload'])
            # Workaround for incomplete virtfs jail initialization
            user_shell = pwd.getpwnam(user_name).pw_shell
            if user_shell == '/usr/local/cpanel/bin/jailshell':
                subprocess.call('su - '+user_name+' -c "touch '+domain_home+'/public_html"', shell=True)
        return
    else:
        return


def hhvm_backend_add(user_name, owner_name, domain_home, clusterenabled, *cluster_serverlist):
    """Function to setup hhvm for user """
    hhvm_server_file = installation_path + "/hhvm.d/" + user_name + ".ini"
    HHVM_MASTER_TEMPLATE = 'hhvm_secure.ini.j2'
    # Generate hhvm ini files
    if not os.path.isfile(hhvm_server_file):
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(HHVM_MASTER_TEMPLATE)
        templateVars = {"CPANELUSER": user_name,
                        "HOMEDIR": domain_home
                        }
        generated_config = template.render(templateVars)
        with codecs.open(hhvm_server_file, 'w', 'utf-8') as confout:
            confout.write(generated_config)
        # generate HHVM resource limit settings
        silentremove('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d/limits.conf')
        if not os.path.isdir('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d'):
            os.mkdir('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d', 0o755)
        TEMPLATE_FILE = "limits.conf.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {"OWNER": owner_name
                        }
        generated_config = template.render(templateVars)
        with codecs.open('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d/limits.conf', 'w', 'utf-8') as confout:
            confout.write(generated_config)
        os.chmod('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d/limits.conf', 0o644)
        subprocess.call(['systemctl', 'start', 'ndeploy_hhvm@'+user_name+'.service'])
        subprocess.call(['systemctl', 'enable', 'ndeploy_hhvm@'+user_name+'.service'])
        # Sync cluster config and call systemd remotely
        if clusterenabled:
            subprocess.call('/usr/sbin/csync2 -x', shell=True)
            subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m systemd -a "name=ndeploy_hhvm@'+user_name+'.service state=started enabled=yes"', shell=True)
    else:
        # generate HHVM resource limit settings
        silentremove('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d/limits.conf')
        if not os.path.isdir('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d'):
            os.mkdir('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d', 0o755)
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "limits.conf.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {"OWNER": owner_name
                        }
        generated_config = template.render(templateVars)
        with codecs.open('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d/limits.conf', 'w', 'utf-8') as confout:
            confout.write(generated_config)
        os.chmod('/etc/systemd/system/ndeploy_hhvm@'+user_name+'.service.d/limits.conf', 0o644)
        subprocess.call(['systemctl', 'restart', 'ndeploy_hhvm@'+user_name+'.service'])
        subprocess.call(['systemctl', 'enable', 'ndeploy_hhvm@'+user_name+'.service'])
        if clusterenabled:
            subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m systemd -a "name=ndeploy_hhvm@'+user_name+'.service state=restarted enabled=yes"', shell=True)
    return


def php_secure_backend_add(user_name, owner_name, domain_home, clusterenabled, *cluster_serverlist):
    """Function to setup php-fpm for user using systemd socket activation"""
    phpfpm_conf_file = installation_path + "/secure-php-fpm.d/" + user_name + ".conf"
    if not os.path.isfile(phpfpm_conf_file):
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "secure-php-fpm.conf.j2"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {"CPANELUSER": user_name,
                        "HOMEDIR": domain_home
                        }
        generated_config = template.render(templateVars)
        with codecs.open(phpfpm_conf_file, 'w', 'utf-8') as confout:
            confout.write(generated_config)
        if clusterenabled:
            subprocess.call('/usr/sbin/csync2 -x', shell=True)
    backend_config_file = installation_path+"/conf/backends.yaml"
    with open(backend_config_file, 'r') as backend_data_yaml:
        backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        for backend_name in php_backends_dict.keys():
            silentremove('/etc/systemd/system/'+backend_name+'@'+user_name+'.service.d/limits.conf')
            if not os.path.isdir('/etc/systemd/system/'+backend_name+'@'+user_name+'.service.d'):
                os.mkdir('/etc/systemd/system/'+backend_name+'@'+user_name+'.service.d', 0o755)
            templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
            templateEnv = jinja2.Environment(loader=templateLoader)
            TEMPLATE_FILE = "limits.conf.j2"
            template = templateEnv.get_template(TEMPLATE_FILE)
            templateVars = {"OWNER": owner_name
                            }
            generated_config = template.render(templateVars)
            with codecs.open('/etc/systemd/system/'+backend_name+'@'+user_name+'.service.d/limits.conf', 'w', 'utf-8') as confout:
                confout.write(generated_config)
            os.chmod('/etc/systemd/system/'+backend_name+'@'+user_name+'.service.d/limits.conf', 0o644)
            subprocess.call(['systemctl', 'start', backend_name+'@'+user_name+'.socket'])
            subprocess.call(['systemctl', 'enable', backend_name+'@'+user_name+'.socket'])
            # Stopping the service as a new request to socket will activate it again
            if not os.path.isfile(installation_path+'/conf/skip_php-fpm_reload'):
                subprocess.call(['systemctl', 'stop', backend_name+'@'+user_name+'.service'])
            if clusterenabled:
                subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m systemd -a "name='+backend_name+'@'+user_name+'.socket state=started enabled=yes"', shell=True)
                if not os.path.isfile(installation_path+'/conf/skip_php-fpm_reload'):
                    subprocess.call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m systemd -a "name='+backend_name+'@'+user_name+'.service state=stopped"', shell=True)
    return


def nginx_confgen(is_suspended, owner, clusterenabled, *cluster_serverlist, **kwargs):
    """Function that generates nginx config """
    # Initiate Jinja2 templateEnv
    templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    # Get all Data from cPanel userdata files
    if kwargs.get('maindomain').startswith("*"):
        cpdomainjson = "/var/cpanel/userdata/" + kwargs.get('configuser') + "/" + kwargs.get('maindomain') + ".cache"
    else:
        cpdomainjson = "/var/cpanel/userdata/" + kwargs.get('configuser') + "/" + kwargs.get('configdomain') + ".cache"
    with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
        json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
    cpanel_ipv4 = json_parsed_cpaneldomain.get('ip')
    if clusterenabled:
        if os.path.isfile('/var/cpanel/cpnat'):
            with open('/var/cpanel/cpnat') as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            if content:
                appserver_ipv4 = cpanel_ipv4
                for line in content:
                    internalip, externalip = line.split()
                    if internalip == cpanel_ipv4:
                        appserver_ipv4 = externalip
                        break
            else:
                appserver_ipv4 = cpanel_ipv4
        else:
            appserver_ipv4 = cpanel_ipv4
    else:
        appserver_ipv4 = cpanel_ipv4
    domain_home = json_parsed_cpaneldomain.get('homedir')
    document_root = json_parsed_cpaneldomain.get('documentroot')
    diff_dir = document_root.replace(domain_home, "")
    domain_server_name = json_parsed_cpaneldomain.get('servername')
    domain_alias_name = json_parsed_cpaneldomain.get('serveralias')
    if domain_alias_name:
        serveralias_list = domain_alias_name.split(' ')
        serveralias_list_new = list(serveralias_list)
        try:
            serveralias_list_new.remove('www.'+kwargs.get('maindomain'))
        except ValueError:
            pass
        try:
            serveralias_list_new.remove(kwargs.get('maindomain'))
        except ValueError:
            pass
    else:
        serveralias_list = []
        serveralias_list_new = []
    if domain_alias_name:
        domain_list = domain_server_name + " " + domain_alias_name
    else:
        domain_list = domain_server_name
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
    if kwargs.get('maindomain').startswith("*"):
        cpdomainyaml_ssl = "/var/cpanel/userdata/" + kwargs.get('configuser') + "/" + kwargs.get('maindomain') + "_SSL"
        # We setup TLS based on /var/cpanel/ssl/apache_tls/ path in cPanel v68+ first
        sslcertificatekeyfile = '/var/cpanel/ssl/apache_tls/'+kwargs.get('maindomain')+'/combined'
        sslcertificatefile = '/var/cpanel/ssl/apache_tls/'+kwargs.get('maindomain')+'/combined'
        sslcombinedcert = '/var/cpanel/ssl/apache_tls/'+kwargs.get('maindomain')+'/combined'
    else:
        cpdomainyaml_ssl = "/var/cpanel/userdata/" + kwargs.get('configuser') + "/" + kwargs.get('configdomain') + "_SSL"
        # We setup TLS based on /var/cpanel/ssl/apache_tls/ path in cPanel v68+ first
        sslcertificatekeyfile = '/var/cpanel/ssl/apache_tls/'+kwargs.get('configdomain')+'/combined'
        sslcertificatefile = '/var/cpanel/ssl/apache_tls/'+kwargs.get('configdomain')+'/combined'
        sslcombinedcert = '/var/cpanel/ssl/apache_tls/'+kwargs.get('configdomain')+'/combined'
    if os.path.isfile(cpdomainyaml_ssl):
        hasssl = True
        # If new TLS path dont exist lets get legacy TLS path from the cPanel domaindata
        if not os.path.isfile(sslcertificatekeyfile):
            with open(cpdomainyaml_ssl, 'r') as cpdomainyaml_ssl_data_stream:
                yaml_parsed_cpaneldomain_ssl = yaml.safe_load(cpdomainyaml_ssl_data_stream)
            sslcertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatefile')
            sslcertificatekeyfile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatekeyfile')
            sslcacertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcacertificatefile')
            if sslcacertificatefile:
                sslcombinedcert = "/etc/nginx/ssl/" + kwargs.get('configdomain') + ".crt"
                filenames = [sslcertificatefile, sslcacertificatefile]
                # Intialize a count to prevent an infinite loop
                wait_count = 0
                with codecs.open(sslcombinedcert, 'w', 'utf-8') as outfile:
                    for fname in filenames:
                        # we wait for the file to be created if it does not exist.
                        # this will eventually be removed  when SSL events have hook as there is a risk for infinite loop
                        # Lets wait 10 minutes in the hope that cPanel creates the SSL file
                        while not os.path.exists(fname):
                            time.sleep(1)
                            wait_count = wait_count + 1
                            if wait_count > 600:
                                break
                        # if we reached the timeout exit by raising an error
                        if not wait_count < 600:
                            print("Invalid TLS data in userdata file")
                            sys.exit(1)
                        with codecs.open(fname, 'r', 'utf-8') as infile:
                            outfile.write(infile.read()+"\n")
                os.chmod(sslcombinedcert, 0o644)
                if os.stat(sslcombinedcert).st_size == 0:
                    hasssl = False
                    sslcombinedcert = None
                    sslcertificatefile = None
                    sslcacertificatefile = None
                    sslcertificatekeyfile = None
                    print("Error:: TLS cert is invalid")
            else:
                sslcombinedcert = sslcertificatefile
    else:
        hasssl = False
        sslcombinedcert = None
        sslcertificatefile = None
        sslcacertificatefile = None
        sslcertificatekeyfile = None
    # Get all data from nDeploy domain-data file
    if is_suspended:
        if os.path.isfile(installation_path + "/conf/domain_data_suspended_local.yaml"):
            domain_data_file = installation_path + "/conf/domain_data_suspended_local.yaml"
        else:
            domain_data_file = installation_path + "/conf/domain_data_suspended.yaml"
    else:
        domain_data_file = installation_path + "/domain-data/" + kwargs.get('configdomain')
    if not os.path.isfile(domain_data_file):
        if os.path.isfile(installation_path+"/conf/domain_data_default_local.yaml"):
            TEMPLATE_FILE = installation_path+"/conf/domain_data_default_local.yaml"
        else:
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
    apptemplate_code = yaml_parsed_domain_data.get('apptemplate_code', None)
    backend_path = yaml_parsed_domain_data.get('backend_path', None)
    backend_version = yaml_parsed_domain_data.get('backend_version', None)
    user_config = yaml_parsed_domain_data.get('user_config', 'disabled')
    phpfpm_selector = yaml_parsed_domain_data.get('phpfpm_selector', None)
    phpfpm_path = yaml_parsed_domain_data.get('phpfpm_path', None)
    # initialize the fastcgi_socket variable
    fastcgi_socket = None
    # Lets get the PHPFPM selector stuff done
    if os.path.isfile(installation_path+'/conf/PHPFPM_SELECTOR_ENABLED') and phpfpm_selector is not None:
        if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
            php_secure_backend_add(kwargs.get('configuser'), owner, domain_home, clusterenabled, *cluster_serverlist)
            phpfpm_secure_socket = domain_home+"/tmp/"+kwargs.get('configdomain')+".sock"
            if not os.path.islink(phpfpm_secure_socket):
                os.symlink(phpfpm_path + "/var/run/" + kwargs.get('configuser') + ".sock", phpfpm_secure_socket)
            else:
                if not os.path.realpath(phpfpm_secure_socket) == phpfpm_path + "/var/run/" + kwargs.get('configuser') + ".sock":
                    silentremove(phpfpm_secure_socket)
                    os.symlink(phpfpm_path + "/var/run/" + kwargs.get('configuser') + ".sock", phpfpm_secure_socket)
        else:
            php_backend_add(kwargs.get('configuser'), domain_home)
            phpfpm_socket = domain_home+"/tmp/"+kwargs.get('configdomain')+".sock"
            if not os.path.islink(phpfpm_socket):
                os.symlink(phpfpm_path + "/var/run/" + kwargs.get('configuser') + ".sock", phpfpm_socket)
            else:
                if not os.path.realpath(phpfpm_socket) == phpfpm_path + "/var/run/" + kwargs.get('configuser') + ".sock":
                    silentremove(phpfpm_socket)
                    os.symlink(phpfpm_path + "/var/run/" + kwargs.get('configuser') + ".sock", phpfpm_socket)
    # Following are features that the UI can change . Can be expanded in future
    # as and when more features are incorporated
    if os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
        mod_security = yaml_parsed_domain_data.get('mod_security', 'disabled')
    else:
        mod_security = 'disabled'
    if os.path.isfile('/etc/nginx/modules.d/naxsi.load') and mod_security == 'disabled':
        naxsi = yaml_parsed_domain_data.get('naxsi', 'disabled')
        naxsi_whitelist = yaml_parsed_domain_data.get('naxsi_whitelist', None)
    else:
        naxsi = 'disabled'
        naxsi_whitelist = 'none'
    if os.path.isfile('/etc/nginx/conf.auto/luarestywaf.conf'):
        lua_waf = yaml_parsed_domain_data.get('lua_waf', 'disabled')
    else:
        lua_waf = 'disabled'
    if os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
        pagespeed = yaml_parsed_domain_data.get('pagespeed', 'disabled')
        pagespeed_filter = yaml_parsed_domain_data.get('pagespeed_filter', 'CoreFilters')
    else:
        pagespeed = 'disabled'
        pagespeed_filter = 'CoreFilters'
    if os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):
        test_cookie = yaml_parsed_domain_data.get('test_cookie', 'disabled')
    else:
        test_cookie = 'disabled'
    if domain_server_name.startswith("*"):
        wwwredirect = None
    else:
        wwwredirect = yaml_parsed_domain_data.get('wwwredirect', None)
    autoindex = yaml_parsed_domain_data.get('autoindex', None)
    redirect_to_ssl = yaml_parsed_domain_data.get('redirect_to_ssl', None)
    clickjacking_protect = yaml_parsed_domain_data.get('clickjacking_protect', None)
    disable_contenttype_sniffing = yaml_parsed_domain_data.get('disable_contenttype_sniffing', None)
    xss_filter = yaml_parsed_domain_data.get('xss_filter', None)
    hsts = yaml_parsed_domain_data.get('hsts', None)
    if os.path.isfile('/etc/nginx/modules.d/brotli.load'):
        brotli = yaml_parsed_domain_data.get('brotli', None)
    else:
        brotli = 'disabled'
    gzip = yaml_parsed_domain_data.get('gzip', None)
    http2 = yaml_parsed_domain_data.get('http2', None)
    ssl_offload = yaml_parsed_domain_data.get('ssl_offload', None)
    access_log = yaml_parsed_domain_data.get('access_log', None)
    naxsi_mode = yaml_parsed_domain_data.get('naxsi_mode', 'learn')
    redirect_url = yaml_parsed_domain_data.get('redirecturl', 'none')
    redirectstatus = yaml_parsed_domain_data.get('redirectstatus', 'none')
    append_requesturi = yaml_parsed_domain_data.get('append_requesturi', 'disabled')
    set_expire_static = yaml_parsed_domain_data.get('set_expire_static', 'disabled')
    dos_mitigate = yaml_parsed_domain_data.get('dos_mitigate', None)
    open_file_cache = yaml_parsed_domain_data.get('open_file_cache', None)
    symlink_protection = yaml_parsed_domain_data.get('symlink_protection', 'disabled')
    if not serveralias_list_new:
        redirect_aliases = 'disabled'
    else:
        redirect_aliases = yaml_parsed_domain_data.get('redirect_aliases', None)
    auth_basic = yaml_parsed_domain_data.get('auth_basic', 'disabled')
    subdir_apps = yaml_parsed_domain_data.get('subdir_apps', None)
    if subdir_apps:
        subdir_apps_uniq = {}
        subdir_apps_passenger = {}
        for key in subdir_apps.keys():
            uniq_path = document_root+key
            uniq_filename = md5(uniq_path.encode("utf-8")).hexdigest()
            subdir_apps_uniq[key] = uniq_filename
            my_subdir_dict = subdir_apps.get(key)
            my_subdir_backend = my_subdir_dict.get('backend_category')
            if my_subdir_backend == 'PYTHON' or my_subdir_backend == 'RUBY' or my_subdir_backend == 'NODEJS':
                is_passenger_app = 'enabled'
            else:
                is_passenger_app = 'disabled'
            subdir_apps_passenger[key] = is_passenger_app
    else:
        subdir_apps = {}
        subdir_apps_uniq = {}
        subdir_apps_passenger = {}
    # Lets remove the user config files .We will regenerate it at a later stage
    silentremove("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+".manualconfig_user")
    # For cluster We remove the manualconfigs here as it is regenerated
    if clusterenabled:
        for server in cluster_serverlist:
            silentremove("/etc/nginx/"+server+"/" + kwargs.get('configdomain') + ".manualconfig_user")
    if subdir_apps:
        for subdir in subdir_apps.keys():
            silentremove("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+"_"+subdir_apps_uniq.get(subdir)+".manualconfig_user")
            if clusterenabled:
                for server in cluster_serverlist:
                    silentremove("/etc/nginx/"+server+"/" + kwargs.get('configdomain') + "_" + subdir_apps_uniq.get(subdir) + ".manualconfig_user")
    # Since we have all data needed ,lets render the conf to a file
    if os.path.isfile(installation_path+'/conf/server_local.j2'):
        TEMPLATE_FILE = "server_local.j2"
    else:
        TEMPLATE_FILE = "server.j2"
    server_template = templateEnv.get_template(TEMPLATE_FILE)
    templateVars = {"SSL": hasssl,
                    "IPVSIX": hasipv6,
                    "WWWREDIRECT": wwwredirect,
                    "REDIRECTALIASES": redirect_aliases,
                    "REDIRECTALIASES_LIST": serveralias_list_new,
                    "CPANELIP": cpanel_ipv4,
                    "APPSERVERIP": appserver_ipv4,
                    "CPIPVSIX": ipv6_addr,
                    "IPVSIX": hasipv6,
                    "HTTP2": http2,
                    "CPANELSSLCRT": sslcombinedcert,
                    "CPANELSSLKEY": sslcertificatekeyfile,
                    "CPANELCACERT": sslcacertificatefile,
                    "MAINDOMAINNAME": kwargs.get('maindomain'),
                    "CONFIGDOMAINNAME": kwargs.get('configdomain'),
                    "PAGESPEED": pagespeed,
                    "TEST_COOKIE": test_cookie,
                    "SYMLINK_PROTECTION": symlink_protection,
                    "CLICKJACKING_PROTECT": clickjacking_protect,
                    "DISABLE_CONTENTTYPE_SNIFFING": disable_contenttype_sniffing,
                    "XSS_FILTER": xss_filter,
                    "GZIP": gzip,
                    "BROTLI": brotli,
                    "HSTS": hsts,
                    "MODSECURITY": mod_security,
                    "NAXSI": naxsi,
                    "NAXSIMODE": naxsi_mode,
                    "DOMAINLIST": domain_list,
                    "AUTOINDEX": autoindex,
                    "REDIRECT_TO_SSL": redirect_to_ssl,
                    "ENABLEACCESSLOG": access_log,
                    "OPEN_FILE_CACHE": open_file_cache,
                    "HOMEDIR": domain_home,
                    "SUBDIRAPPS": subdir_apps_uniq,
                    "PASSENGERAPPS": subdir_apps_passenger,
                    "DIFFDIR": diff_dir,
                    "NAXSI_WHITELIST": naxsi_whitelist,
                    "PAGESPEED_FILTER": pagespeed_filter,
                    "SET_EXPIRE_STATIC": set_expire_static,
                    "AUTH_BASIC": auth_basic,
                    "REDIRECTSTATUS": redirectstatus,
                    "REDIRECT_URL": redirect_url,
                    "APPEND_REQUESTURI": append_requesturi,
                    "DOSMITIGATE": dos_mitigate,
                    "LUAWAF": lua_waf,
                    "BACKEND_CATEGORY": backend_category
                    }
    generated_config = server_template.render(templateVars)
    with codecs.open("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+".conf", "w", 'utf-8') as confout:
        confout.write(generated_config)
    if user_config == 'enabled':
        # generate a temp server config
        if os.path.isfile(installation_path+'/conf/server_test_local.j2'):
            TEST_TEMPLATE_FILE = "server_test_local.j2"
        else:
            TEST_TEMPLATE_FILE = "server_test.j2"
        test_server_template = templateEnv.get_template(TEST_TEMPLATE_FILE)
        generated_config = test_server_template.render(templateVars)
        with codecs.open(installation_path+"/lock/"+kwargs.get('configdomain')+".conf", "w", 'utf-8') as confout:
            confout.write(generated_config)
    # If a cluster is setup.Generate nginx config for other servers as well
    if clusterenabled:
        for server in cluster_serverlist:
            connect_server_dict = cluster_data_yaml_parsed.get(server)
            ipmap_dict = connect_server_dict.get("ipmap")
            remote_domain_ipv4 = ipmap_dict.get(cpanel_ipv4, "127.0.0.1")
            if ipv6_addr:
                remote_domain_ipv6 = ipmap_dict.get(ipv6_addr, "::1")
            else:
                remote_domain_ipv6 = None
            cluster_config_out = "/etc/nginx/"+server+"/" + kwargs.get('configdomain') + ".conf"
            templateVars["CPANELIP"] = remote_domain_ipv4
            templateVars["CPIPVSIX"] = remote_domain_ipv6
            cluster_generated_config = server_template.render(templateVars)
            with codecs.open(cluster_config_out, "w", 'utf-8') as confout:
                confout.write(cluster_generated_config)
    # Generate the rest of the config(domain.include) based on the application template
    app_template = templateEnv.get_template(apptemplate_code)
    # We configure the backends first if necessary
    if backend_category == 'PROXY':
        if backend_version == 'railo_tomcat':
            railo_vhost_add_tomcat(domain_server_name, document_root, *serveralias_list)
        elif backend_version == 'java_tomcat':
            java_vhost_add_tomcat(domain_server_name, document_root, *serveralias_list)
        elif backend_version == 'railo_resin':
            railo_vhost_add_resin(kwargs.get('configuser'), domain_server_name, document_root, *serveralias_list)
    elif backend_category == 'PHP':
        fastcgi_socket = backend_path + "/var/run/" + kwargs.get('configuser') + ".sock"
        if not os.path.isfile(fastcgi_socket):
            if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
                php_secure_backend_add(kwargs.get('configuser'), owner, domain_home, clusterenabled, *cluster_serverlist)
            else:
                php_backend_add(kwargs.get('configuser'), domain_home)
    elif backend_category == 'HHVM':
        fastcgi_socket = domain_home+"/hhvm.sock"
        if not os.path.isfile(fastcgi_socket):
            hhvm_backend_add(kwargs.get('configuser'), owner, domain_home, clusterenabled, *cluster_serverlist)
    # We generate the app config from template next
    apptemplateVars = {"SSL_OFFLOAD": ssl_offload,
                       "CPANELIP": cpanel_ipv4,
                       "APPSERVERIP": appserver_ipv4,
                       "DOCUMENTROOT": document_root,
                       "CONFIGDOMAINNAME": kwargs.get('configdomain'),
                       "HOMEDIR": domain_home,
                       "MODSECURITY": mod_security,
                       "NAXSI": naxsi,
                       "NAXSIMODE": naxsi_mode,
                       "UPSTREAM_PORT": backend_path,
                       "PATHTOPYTHON": backend_path,
                       "PATHTORUBY": backend_path,
                       "PATHTONODEJS": backend_path,
                       "SOCKETFILE": fastcgi_socket,
                       "SUBDIRAPPS": subdir_apps_uniq,
                       "DIFFDIR": diff_dir,
                       "NAXSI_WHITELIST": naxsi_whitelist,
                       "SET_EXPIRE_STATIC": set_expire_static,
                       "AUTH_BASIC": auth_basic,
                       "REDIRECTSTATUS": redirectstatus,
                       "REDIRECT_URL": redirect_url,
                       "APPEND_REQUESTURI": append_requesturi,
                       "PATHTOPYTHON": backend_path,
                       "LUAWAF": lua_waf
                       }
    generated_app_config = app_template.render(apptemplateVars)
    with codecs.open("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+".include", "w", 'utf-8') as confout:
        confout.write(generated_app_config)
    # Copy the user config for testing if present
    if user_config == 'enabled' and os.path.isfile(document_root+"/nginx.conf"):
        shutil.copyfile(document_root+"/nginx.conf", installation_path+"/lock/"+kwargs.get('configdomain')+".manualconfig_test")
    # Get the subdir config also rendered
    if subdir_apps:
        for subdir in subdir_apps.keys():
            the_subdir_app_dict = subdir_apps.get(subdir)
            subdir_backend_category = the_subdir_app_dict.get('backend_category')
            subdir_backend_path = the_subdir_app_dict.get('backend_path')
            subdir_backend_version = the_subdir_app_dict.get('backend_version')
            subdir_apptemplate_code = the_subdir_app_dict.get('apptemplate_code')
            subdir_auth_basic = the_subdir_app_dict.get('auth_basic', 'disabled')
            subdir_naxsi_mode = the_subdir_app_dict.get('naxsi_mode', 'learn')
            if os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
                subdir_mod_security = the_subdir_app_dict.get('mod_security', 'disabled')
            else:
                subdir_mod_security = 'disabled'
            if os.path.isfile('/etc/nginx/modules.d/naxsi.load') and subdir_mod_security == 'disabled':
                subdir_naxsi = the_subdir_app_dict.get('naxsi', 'disabled')
                subdir_naxsi_whitelist = the_subdir_app_dict.get('naxsi_whitelist', None)
            else:
                subdir_naxsi = 'disabled'
                subdir_naxsi_whitelist = 'none'
            subdir_redirect_url = the_subdir_app_dict.get('redirecturl', 'none')
            subdir_redirectstatus = the_subdir_app_dict.get('redirectstatus', 'none')
            subdir_set_expire_static = the_subdir_app_dict.get('set_expire_static', 'disabled')
            subdir_append_requesturi = the_subdir_app_dict.get('append_requesturi', 'disabled')
            subdirApptemplate = templateEnv.get_template(subdir_apptemplate_code)
            # We configure the backends first if necessary
            if subdir_backend_category == 'PROXY':
                if subdir_backend_version == 'railo_tomcat':
                    railo_vhost_add_tomcat(domain_server_name, document_root, *serveralias_list)
                elif backend_version == 'java_tomcat':
                    java_vhost_add_tomcat(domain_server_name, document_root, *serveralias_list)
                elif subdir_backend_version == 'railo_resin':
                    railo_vhost_add_resin(kwargs.get('configuser'), domain_server_name, document_root, *serveralias_list)
            elif subdir_backend_category == 'PHP':
                fastcgi_socket = subdir_backend_path + "/var/run/" + kwargs.get('configuser') + ".sock"
                if not os.path.isfile(fastcgi_socket):
                    if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
                        php_secure_backend_add(kwargs.get('configuser'), owner, domain_home, clusterenabled, *cluster_serverlist)
                    else:
                        php_backend_add(kwargs.get('configuser'), domain_home)
            elif subdir_backend_category == 'HHVM':
                fastcgi_socket = domain_home+"/hhvm.sock"
                if not os.path.isfile(fastcgi_socket):
                    hhvm_backend_add(kwargs.get('configuser'), owner, domain_home, clusterenabled, *cluster_serverlist)
            subdirApptemplateVars = {"NEWDOCUMENTROOT": document_root+'/'+subdir,
                                     "SUBDIR": subdir,
                                     "SUBDIRAPPS": subdir_apps_uniq,
                                     "CPANELIP": cpanel_ipv4,
                                     "APPSERVERIP": appserver_ipv4,
                                     "SSL_OFFLOAD": ssl_offload,
                                     "CPANELIP": cpanel_ipv4,
                                     "DOCUMENTROOT": document_root,
                                     "CONFIGDOMAINNAME": kwargs.get('configdomain'),
                                     "HOMEDIR": domain_home,
                                     "DIFFDIR": diff_dir,
                                     "MODSECURITY": subdir_mod_security,
                                     "NAXSI": subdir_naxsi,
                                     "NAXSIMODE": subdir_naxsi_mode,
                                     "UPSTREAM_PORT": subdir_backend_path,
                                     "PATHTOPYTHON": subdir_backend_path,
                                     "PATHTORUBY": subdir_backend_path,
                                     "PATHTONODEJS": subdir_backend_path,
                                     "SOCKETFILE": fastcgi_socket,
                                     "NAXSI_WHITELIST": subdir_naxsi_whitelist,
                                     "SET_EXPIRE_STATIC": subdir_set_expire_static,
                                     "AUTH_BASIC": subdir_auth_basic,
                                     "REDIRECT_URL": subdir_redirect_url,
                                     "REDIRECTSTATUS": subdir_redirectstatus,
                                     "APPEND_REQUESTURI": subdir_append_requesturi,
                                     "PATHTOPYTHON": backend_path,
                                     "LUAWAF": lua_waf
                                     }
            generated_subdir_app_config = subdirApptemplate.render(subdirApptemplateVars)
            with codecs.open("/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+"_"+subdir_apps_uniq.get(subdir)+".subinclude", "w", 'utf-8') as confout:
                confout.write(generated_subdir_app_config)
            # Copy the user config for testing if present
            if user_config == 'enabled' and os.path.isfile(document_root+'/'+subdir+"/nginx.conf"):
                shutil.copyfile(document_root+'/'+subdir+"/nginx.conf", installation_path+"/lock/"+kwargs.get('configdomain')+"_"+subdir_apps_uniq.get(subdir)+".manualconfig_test")
    # If we have a user_config.Lets generate the test confg
    if user_config == 'enabled':
        # generate a temp nginx config
        NGINX_CONF_TEMPLATE = 'nginx_test.j2'
        nginx_test_template = templateEnv.get_template(NGINX_CONF_TEMPLATE)
        nginxConftemplateVars = {"CONFIGDOMAINNAME": kwargs.get('configdomain')}
        generated_nginx_config = nginx_test_template.render(nginxConftemplateVars)
        domain_nginx_test = installation_path+"/lock/"+kwargs.get('configdomain')+".nginx_test"
        with codecs.open(domain_nginx_test, "w", 'utf-8') as confout:
            confout.write(generated_nginx_config)
        # test the temp confg and if all ok activate the user_configs
        nginx_conf_test = subprocess.call("/usr/sbin/nginx -c " + domain_nginx_test + " -t", shell=True)
        if nginx_conf_test == 0:
            # ok all seems good we copy the user_configs to /etc/nginx/sites-enabled
            if os.path.isfile(installation_path+"/lock/"+kwargs.get('configdomain')+".manualconfig_test"):
                shutil.copyfile(installation_path+"/lock/"+kwargs.get('configdomain')+".manualconfig_test", "/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+".manualconfig_user")
            if subdir_apps:
                for subdir in subdir_apps.keys():
                    if os.path.isfile(installation_path+"/lock/"+kwargs.get('configdomain')+"_"+subdir_apps_uniq.get(subdir)+".manualconfig_test"):
                        shutil.copyfile(installation_path+"/lock/"+kwargs.get('configdomain')+"_"+subdir_apps_uniq.get(subdir)+".manualconfig_test", "/etc/nginx/sites-enabled/"+kwargs.get('configdomain')+"_"+subdir_apps_uniq.get(subdir)+".manualconfig_user")
        # Remove all the temporary files we created for the test
        silentremove(domain_nginx_test)
        silentremove(installation_path+"/lock/"+kwargs.get('configdomain')+".conf")
        silentremove(installation_path+"/lock/"+kwargs.get('configdomain')+".manualconfig_test")
        if subdir_apps:
            for subdir in subdir_apps.keys():
                silentremove(installation_path+"/lock/"+kwargs.get('configdomain')+"_"+subdir_apps_uniq.get(subdir)+".manualconfig_test")

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
        # Update the userdata cache
        subprocess.Popen(['/scripts/updateuserdatacache', '--force', cpaneluser], shell=True)
        # Try loading the main userdata cache file
        cpuserdatajson = "/var/cpanel/userdata/" + cpaneluser + "/main.cache"
        if os.path.isfile(cpuserdatajson):
            with open(cpuserdatajson) as cpaneluser_data_stream:
                json_parsed_cpaneluser = json.load(cpaneluser_data_stream)
            main_domain = json_parsed_cpaneluser.get('main_domain')
            # parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   # This data is irrelevant as parked domain list is in ServerAlias
            addon_domains_dict = json_parsed_cpaneluser.get('addon_domains')     # So we know which addon is mapped to which sub-domain
            sub_domains = json_parsed_cpaneluser.get('sub_domains')
            # Check if a user is suspended and set a flag accordingly
            if os.path.exists("/var/cpanel/users.cache/" + cpaneluser):
                with open("/var/cpanel/users.cache/" + cpaneluser) as users_file:
                    json_parsed_cpusersfile = json.load(users_file)
                if json_parsed_cpusersfile.get('SUSPENDED') == "1":
                    is_suspended = True
                else:
                    is_suspended = False
                myowner = json_parsed_cpusersfile.get('OWNER')
                if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
                    ownerslice = "/etc/systemd/system/"+myowner+".slice"
                    if not os.path.isfile(ownerslice):
                        # create the slice from a template
                        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
                        templateEnv = jinja2.Environment(loader=templateLoader)
                        if os.path.isfile(installation_path+"/conf/simpler_resources_local.j2"):
                            TEMPLATE_FILE = "simpler_resources_local.j2"
                        else:
                            TEMPLATE_FILE = "simpler_resources.j2"
                        template = templateEnv.get_template(TEMPLATE_FILE)
                        templateVars = {"OWNER": myowner
                                        }
                        generated_config = template.render(templateVars)
                        with codecs.open(ownerslice, 'w', 'utf-8') as confout:
                            confout.write(generated_config)
            else:
                # If cpanel users file is not present silently exit
                sys.exit(0)
        else:
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
        nginx_confgen(is_suspended, myowner, clusterenabled, *cluster_serverlist, configuser=cpaneluser, configdomain=main_domain, maindomain=main_domain)  # Generate conf for main domain
        # iterate over the addon-domain ,passing the subdomain as the configdomain
        for the_addon_domain in addon_domains_dict.keys():
            nginx_confgen(is_suspended, myowner, clusterenabled, *cluster_serverlist, configuser=cpaneluser, configdomain=addon_domains_dict.get(the_addon_domain), maindomain=the_addon_domain)  # Generate conf for sub domains which takes care of addon as well
        # iterate over sub-domains and generate config if its not a linked sub-domain for addon-domain
        for the_sub_domain in sub_domains:
            if the_sub_domain not in addon_domains_dict.values():
                if the_sub_domain.startswith("*"):
                    subdom_config_dom = "_wildcard_."+the_sub_domain.replace('*.', '')
                    nginx_confgen(is_suspended, myowner, clusterenabled, *cluster_serverlist, configuser=cpaneluser, configdomain=subdom_config_dom, maindomain=the_sub_domain)
                else:
                    nginx_confgen(is_suspended, myowner, clusterenabled, *cluster_serverlist, configuser=cpaneluser, configdomain=the_sub_domain, maindomain=the_sub_domain)
        # Ok we are done generating .Lets reload nginx and some misc things ( Using async Popen whenever possible )
        # Unless someone has set a skip reload flag
        if not os.path.isfile(installation_path+'/conf/skip_nginx_reload'):
            subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'])
        if clusterenabled:
            for server in cluster_serverlist:
                target_dir = "/etc/nginx/"+server+"/"
                subprocess.Popen(['/usr/bin/rsync', '-a', '--exclude=*.conf', '/etc/nginx/sites-enabled/', target_dir])
