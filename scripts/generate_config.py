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

# Function defentitions


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
        cpdomainyaml_ssl = "/var/cpanel/userdata/" + kwargs.get('configuser') + "/" + kwargs.get('maindomain') + "_SSL"
        with open(cpdomainyaml_ssl, 'r') as cpaneldomain_ssl_data_stream:
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
                    "HTTP2": http2,
                    "DOMAINLIST": domain_list,
                    "AUTOINDEX": autoindex,
                    "REDIRECT_TO_SSL": redirect_to_ssl
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
                                       "HTTP2": http2,
                                       "DOMAINLIST": domain_list,
                                       "AUTOINDEX": autoindex,
                                       "REDIRECT_TO_SSL": redirect_to_ssl
                                       }
                cluster_generated_config = template.render(clustertemplateVars)
                with open(cluster_config_out, "w") as confout:
                    confout.write(cluster_generated_config)


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
