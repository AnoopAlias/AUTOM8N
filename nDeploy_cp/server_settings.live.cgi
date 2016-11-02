#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()

def print_green(theoption, hint):
    print(('<p style="background-color:LightGrey"><font color="green">'+theoption+'</font> - '+hint+'</p>'))

def print_red(theoption, hint):
    print(('<p style="background-color:LightGrey"><font color="red">'+theoption+'</font> - '+hint+'</p>'))


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>nDeploy</title>')
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<a href="ndeploy.live.cgi"><img border="0" src="nDeploy.png" alt="nDeploy"></a>')
print('<HR>')
if form.getvalue('domain'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        # App settings
        backend_category = yaml_parsed_profileyaml.get('backend_category')
        backend_version = yaml_parsed_profileyaml.get('backend_version')
        backend_path = yaml_parsed_profileyaml.get('backend_path')
        apptemplate_code = yaml_parsed_profileyaml.get('apptemplate_code')
        # Server Settings
        naxsi = yaml_parsed_profileyaml.get('naxsi')
        naxsi_mode = yaml_parsed_profileyaml.get('naxsi_mode')
        autoindex = yaml_parsed_profileyaml.get('autoindex')
        pagespeed = yaml_parsed_profileyaml.get('pagespeed')
        brotli = yaml_parsed_profileyaml.get('brotli')
        gzip = yaml_parsed_profileyaml.get('gzip')
        http2 = yaml_parsed_profileyaml.get('http2')
        access_log = yaml_parsed_profileyaml.get('access_log')
        open_file_cache = yaml_parsed_profileyaml.get('open_file_cache')
        ssl_offload = yaml_parsed_profileyaml.get('ssl_offload')
        wwwredirect = yaml_parsed_profileyaml.get('wwwredirect')
        redirect_to_ssl = yaml_parsed_profileyaml.get('redirect_to_ssl')
        redirect_aliases = yaml_parsed_profileyaml.get('redirect_aliases')
        clickjacking_protect = yaml_parsed_profileyaml.get('clickjacking_protect')
        disable_contenttype_sniffing = yaml_parsed_profileyaml.get('disable_contenttype_sniffing')
        xss_filter = yaml_parsed_profileyaml.get('xss_filter')
        content_security_policy = yaml_parsed_profileyaml.get('content_security_policy')
        hsts = yaml_parsed_profileyaml.get('hsts')
        dos_mitigate = yaml_parsed_profileyaml.get('dos_mitigate')
        # get the human friendly name of the app template
        if os.path.isfile(app_template_file):
            with open(app_template_file,'r') as apptemplate_data_yaml:
                apptemplate_data_yaml_parsed = yaml.safe_load(apptemplate_data_yaml)
            apptemplate_dict = apptemplate_data_yaml_parsed.get(backend_category)
            apptemplate_description = apptemplate_dict.get(apptemplate_code)
        else:
            print('ERROR : app template data file error')
        # Ok we are done with getting the settings,now lets present it to the user
        print(('<p style="background-color:LightGrey">SERVER SETTINGS:  '+mydomain+'</p>'))
        print('<HR>')
        print('<form action="save_server_settings.live.cgi" method="post">')
        print('<div class="boxedyellow">')
        # autoindex
        autoindex_hint = "enable for directory listing"
        if autoindex is True:
            print_green("autoindex", autoindex_hint)
            print('<input type="radio" name="autoindex" value="True" checked/> Enabled')
            print('<input type="radio" name="autoindex" value="False" /> Disabled')
        else:
            print_red("autoindex", autoindex_hint)
            print('<input type="radio" name="autoindex" value="True" /> Enabled')
            print('<input type="radio" name="autoindex" value="False" checked/> Disabled')
        # ssl_offload
        ssl_offload_hint = "enable for performance, disable if redirect loop error"
        if ssl_offload is True:
            print_green("ssl_offload", ssl_offload_hint)
            print('<input type="radio" name="ssl_offload" value="True" checked/> Enabled')
            print('<input type="radio" name="ssl_offload" value="False" /> Disabled')
        else:
            print_red("ssl_offload", ssl_offload_hint)
            print('<input type="radio" name="ssl_offload" value="True" /> Enabled')
            print('<input type="radio" name="ssl_offload" value="False" checked/> Disabled')
        # pagespeed
        pagespeed_hint = "delivers pagespeed optimized webpage, resource intensive"
        if pagespeed is True:
            print_green("pagespeed", pagespeed_hint)
            print('<input type="radio" name="pagespeed" value="True" checked/> Enabled')
            print('<input type="radio" name="pagespeed" value="False" /> Disabled')
        else:
            print_red("pagespeed", pagespeed_hint)
            print('<input type="radio" name="pagespeed" value="True" /> Enabled')
            print('<input type="radio" name="pagespeed" value="False" checked/> Disabled')
        # brotli
        brotli_hint = "bandwidth optimization, resource intensive, tls only"
        if brotli is True:
            print_green("brotli", brotli_hint)
            print('<input type="radio" name="brotli" value="True" checked/> Enabled')
            print('<input type="radio" name="brotli" value="False" /> Disabled')
        else:
            print_red("brotli", brotli_hint)
            print('<input type="radio" name="brotli" value="True" /> Enabled')
            print('<input type="radio" name="brotli" value="False" checked/> Disabled')
        # gzip
        gzip_hint = "bandwidth optimization, reource intensive"
        if gzip is True:
            print_green("gzip", gzip_hint)
            print('<input type="radio" name="gzip" value="True" checked/> Enabled')
            print('<input type="radio" name="gzip" value="False" /> Disabled')
        else:
            print_red("gzip", gzip_hint)
            print('<input type="radio" name="gzip" value="True" /> Enabled')
            print('<input type="radio" name="gzip" value="False" checked/> Disabled')
        # http2
        http2_hint = "works only with TLS"
        if http2 is True:
            print_green("http2", http2_hint)
            print('<input type="radio" name="http2" value="True" checked/> Enabled')
            print('<input type="radio" name="http2" value="False" /> Disabled')
        else:
            print_red("http2", http2_hint)
            print('<input type="radio" name="http2" value="True" /> Enabled')
            print('<input type="radio" name="http2" value="False" checked/> Disabled')
        # access_log
        access_log_hint = "disabling access_log increase performance but stats wont work"
        if access_log is True:
            print_green("access_log", access_log_hint)
            print('<input type="radio" name="access_log" value="True" checked/> Enabled')
            print('<input type="radio" name="access_log" value="False" /> Disabled')
        else:
            print_red("access_log", access_log_hint)
            print('<input type="radio" name="access_log" value="True" /> Enabled')
            print('<input type="radio" name="access_log" value="False" checked/> Disabled')
        # open_file_cache
        open_file_cache_hint = "increase performance, disable on dev environment for no caching"
        if open_file_cache is True:
            print_green("open_file_cache", open_file_cache_hint)
            print('<input type="radio" name="open_file_cache" value="True" checked/> Enabled')
            print('<input type="radio" name="open_file_cache" value="False" /> Disabled')
        else:
            print_red("open_file_cache", open_file_cache_hint)
            print('<input type="radio" name="open_file_cache" value="True" /> Enabled')
            print('<input type="radio" name="open_file_cache" value="False" checked/> Disabled')
        # clickjacking_protect
        clickjacking_protect_hint = "add_header X-Frame-Options SAMEORIGIN;"
        if clickjacking_protect is True:
            print_green("clickjacking_protect", clickjacking_protect_hint)
            print('<input type="radio" name="clickjacking_protect" value="True" checked/> Enabled')
            print('<input type="radio" name="clickjacking_protect" value="False" /> Disabled')
        else:
            print_red("clickjacking_protect", clickjacking_protect_hint)
            print('<input type="radio" name="clickjacking_protect" value="True" /> Enabled')
            print('<input type="radio" name="clickjacking_protect" value="False" checked/> Disabled')
        # disable_contenttype_sniffing
        disable_contenttype_sniffing_hint = "add_header X-Content-Type-Options nosniff;"
        if disable_contenttype_sniffing is True:
            print_green("disable_contenttype_sniffing", disable_contenttype_sniffing_hint)
            print('<input type="radio" name="disable_contenttype_sniffing" value="True" checked/> Enabled')
            print('<input type="radio" name="disable_contenttype_sniffing" value="False" /> Disabled')
        else:
            print_red("disable_contenttype_sniffing", disable_contenttype_sniffing_hint)
            print('<input type="radio" name="disable_contenttype_sniffing" value="True" /> Enabled')
            print('<input type="radio" name="disable_contenttype_sniffing" value="False" checked/> Disabled')
        # xss_filter
        xss_filter_hint = 'add_header X-XSS-Protection "1; mode=block";'
        if xss_filter is True:
            print_green("xss_filter", xss_filter_hint)
            print('<input type="radio" name="xss_filter" value="True" checked/> Enabled')
            print('<input type="radio" name="xss_filter" value="False" /> Disabled')
        else:
            print_red("xss_filter", xss_filter_hint)
            print('<input type="radio" name="xss_filter" value="True" /> Enabled')
            print('<input type="radio" name="xss_filter" value="False" checked/> Disabled')
        # content_security_policy
        content_security_policy_hint = 'add_header Content-Security-Policy "script-src \'self\' www.google-analytics.com ajax.googleapis.com;";'
        if content_security_policy is True:
            print_green("content_security_policy", content_security_policy_hint)
            print('<input type="radio" name="content_security_policy" value="True" checked/> Enabled')
            print('<input type="radio" name="content_security_policy" value="False" /> Disabled')
        else:
            print_red("content_security_policy", content_security_policy_hint)
            print('<input type="radio" name="content_security_policy" value="True" /> Enabled')
            print('<input type="radio" name="content_security_policy" value="False" checked/> Disabled')
        # hsts
        hsts_hint = 'add_header Strict-Transport-Security "max-age=86400" always;'
        if hsts is True:
            print_green("hsts", hsts_hint)
            print('<input type="radio" name="hsts" value="True" checked/> Enabled')
            print('<input type="radio" name="hsts" value="False" /> Disabled')
        else:
            print_red("hsts", hsts_hint)
            print('<input type="radio" name="hsts" value="True" /> Enabled')
            print('<input type="radio" name="hsts" value="False" checked/> Disabled')
        # dos_mitigate
        dos_mitigate_hint = "Enable only when under a dos attack"
        if dos_mitigate is True:
            print_green("dos_mitigate", dos_mitigate_hint)
            print('<input type="radio" name="dos_mitigate" value="True" checked/> Enabled')
            print('<input type="radio" name="dos_mitigate" value="False" /> Disabled')
        else:
            print_red("dos_mitigate", dos_mitigate_hint)
            print('<input type="radio" name="dos_mitigate" value="True" /> Enabled')
            print('<input type="radio" name="dos_mitigate" value="False" checked/> Disabled')
        # naxsi
        naxsi_hint = "NAXSI is a web application firewall"
        if naxsi is True:
            print_green("naxsi", naxsi_hint)
            print('<input type="radio" name="naxsi" value="True" checked/> Enabled')
            print('<input type="radio" name="naxsi" value="False" /> Disabled')
        else:
            print_red("naxsi", naxsi_hint)
            print('<input type="radio" name="naxsi" value="True" /> Enabled')
            print('<input type="radio" name="naxsi" value="False" checked/> Disabled')
        # naxsi_mode
        print(('<p style="background-color:LightGrey">naxsi_mode : active mode blocks requests on trigger</p>'))
        print('<select name="naxsi_mode">')
        print(('<option value="learn">learn</option>'))
        print(('<option value="active">active</option>'))
        print('</select>')
        # redirect_to_ssl
        redirect_to_ssl_hint = "redirect http:// to https:// "
        if redirect_to_ssl is True:
            print_green("redirect_to_ssl", redirect_to_ssl_hint)
            print('<input type="radio" name="redirect_to_ssl" value="True" checked/> Enabled')
            print('<input type="radio" name="redirect_to_ssl" value="False" /> Disabled')
        else:
            print_red("redirect_to_ssl", redirect_to_ssl_hint)
            print('<input type="radio" name="redirect_to_ssl" value="True" /> Enabled')
            print('<input type="radio" name="redirect_to_ssl" value="False" checked/> Disabled')
        # redirect_aliases
        redirect_aliases_hint = "redirect all alias domains to the main domain"
        if redirect_aliases is True:
            print_green("redirect_aliases", redirect_aliases_hint)
            print('<input type="radio" name="redirect_aliases" value="True" checked/> Enabled')
            print('<input type="radio" name="redirect_aliases" value="False" /> Disabled')
        else:
            print_red("redirect_aliases", redirect_aliases_hint)
            print('<input type="radio" name="redirect_aliases" value="True" /> Enabled')
            print('<input type="radio" name="redirect_aliases" value="False" checked/> Disabled')
        # wwwredirect
        print(('<p style="background-color:LightGrey">wwwredirect : select redirection mode</p>'))
        print('<select name="wwwredirect">')
        print(('<option value="none">no redirection</option>'))
        print(('<option value="tononwww">redirect www. to non-www</option>'))
        print(('<option value="towww">redirect non-www to www.</option>'))
        print('</select>')
        # Pass on the domain name to the next stage
        print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
        print('<HR>')
        print('<center><input type="submit" value="Submit"></center>')
        print('</div>')
        print('</form>')
    else:
        print('ERROR : domain-data file i/o error')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
