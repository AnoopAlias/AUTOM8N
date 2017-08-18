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

cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


def print_green(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_red(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>XtendWeb</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')
print('<div class="row">')
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li><a href="xtendweb.live.py">Select Domain</a></li><li class="active">Server Settings</li>')
print('</ol>')
print('<div class="panel panel-default">')
if form.getvalue('domain'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        # Server Settings
        autoindex = yaml_parsed_profileyaml.get('autoindex', 'disabled')
        pagespeed = yaml_parsed_profileyaml.get('pagespeed', 'disabled')
        brotli = yaml_parsed_profileyaml.get('brotli', 'disabled')
        gzip = yaml_parsed_profileyaml.get('gzip', 'disabled')
        http2 = yaml_parsed_profileyaml.get('http2', 'disabled')
        access_log = yaml_parsed_profileyaml.get('access_log', 'enabled')
        open_file_cache = yaml_parsed_profileyaml.get('open_file_cache', 'disabled')
        ssl_offload = yaml_parsed_profileyaml.get('ssl_offload', 'disabled')
        wwwredirect = yaml_parsed_profileyaml.get('wwwredirect', 'none')
        redirect_to_ssl = yaml_parsed_profileyaml.get('redirect_to_ssl', 'disabled')
        redirect_aliases = yaml_parsed_profileyaml.get('redirect_aliases', 'disabled')
        clickjacking_protect = yaml_parsed_profileyaml.get('clickjacking_protect', 'disabled')
        disable_contenttype_sniffing = yaml_parsed_profileyaml.get('disable_contenttype_sniffing', 'disabled')
        xss_filter = yaml_parsed_profileyaml.get('xss_filter', 'disabled')
        hsts = yaml_parsed_profileyaml.get('hsts', 'disabled')
        dos_mitigate = yaml_parsed_profileyaml.get('dos_mitigate', 'disabled')
        pagespeed_filter = yaml_parsed_profileyaml.get('pagespeed_filter', 'CoreFilters')
        redirecturl = yaml_parsed_profileyaml.get('redirecturl', 'none')
        redirectstatus = yaml_parsed_profileyaml.get('redirectstatus', 'none')
        append_requesturi = yaml_parsed_profileyaml.get('append_requesturi', 'disabled')
        test_cookie = yaml_parsed_profileyaml.get('test_cookie', 'disabled')
        symlink_protection = yaml_parsed_profileyaml.get('symlink_protection', 'disabled')
        user_config = yaml_parsed_profileyaml.get('user_config', 'disabled')
        # Ok we are done with getting the settings,now lets present it to the user
        print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div><div class="panel-body">'))
        print('<form id="config" class="form-inline" action="save_server_settings.live.py" method="post">')
        # user_config
        print('<ul class="list-group"><li class="list-group-item">')
        user_config_hint = "enable a custom nginx.conf placed in the document root"
        print('<div class="row">')
        if user_config == 'enabled':
            print_green("user_config", user_config_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="user_config" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="user_config" value="disabled"/> Disabled</label></div>')
            print('</div>')
        else:
            print_red("user_config", user_config_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="user_config" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="user_config" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # autoindex
        print('<ul class="list-group"><li class="list-group-item">')
        autoindex_hint = "enable for directory listing"
        print('<div class="row">')
        if autoindex == 'enabled':
            print_green("autoindex", autoindex_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="autoindex" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="autoindex" value="disabled"/> Disabled</label></div>')
            print('</div>')
        else:
            print_red("autoindex", autoindex_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="autoindex" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="autoindex" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # ssl_offload
        print('<li class="list-group-item">')
        ssl_offload_hint = "enable for performance, disable if redirect loop error"
        print('<div class="row">')
        if ssl_offload == 'enabled':
            print_green("ssl_offload", ssl_offload_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="ssl_offload" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="ssl_offload" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("ssl_offload", ssl_offload_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="ssl_offload" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="ssl_offload" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # pagespeed
        print('<li class="list-group-item">')
        print('<div class="row">')
        pagespeed_hint = "delivers pagespeed optimized webpage, resource intensive"
        if pagespeed == 'enabled':
            print_green("pagespeed", pagespeed_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="pagespeed" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="pagespeed" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("pagespeed", pagespeed_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="pagespeed" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="pagespeed" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # pagespeed filter level
        print('<li class="list-group-item">')
        print('<div class="row">')
        pagespeed_filter_hint = "PassThrough breaks some pages.CoreFilters is mostly safe"
        if pagespeed_filter == 'CoreFilters':
            print_red("pagespeed level", pagespeed_filter_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="pagespeed_filter" value="CoreFilters" checked/> CoreFilters</label></div>')
            print('<div class="radio"><label><input type="radio" name="pagespeed_filter" value="PassThrough" /> PassThrough</label></div>')
            print('</div>')
        else:
            print_green("pagespeed_filter", pagespeed_filter_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="pagespeed_filter" value="CoreFilters" /> CoreFilters</label></div>')
            print('<div class="radio"><label><input type="radio" name="pagespeed_filter" value="PassThrough" checked/> PassThrough</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # brotli
        print('<li class="list-group-item">')
        print('<div class="row">')
        brotli_hint = "bandwidth optimization, resource intensive, tls only"
        if brotli == 'enabled':
            print_green("brotli", brotli_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="brotli" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="brotli" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("brotli", brotli_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="brotli" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="brotli" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # gzip
        print('<li class="list-group-item">')
        print('<div class="row">')
        gzip_hint = "bandwidth optimization, resource intensive"
        if gzip == 'enabled':
            print_green("gzip", gzip_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="gzip" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="gzip" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("gzip", gzip_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="gzip" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="gzip" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # http2
        print('<li class="list-group-item">')
        print('<div class="row">')
        http2_hint = "works only with TLS"
        if http2 == 'enabled':
            print_green("http2", http2_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="http2" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="http2" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("http2", http2_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="http2" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="http2" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # access_log
        print('<li class="list-group-item">')
        print('<div class="row">')
        access_log_hint = "disabling access_log increase performance but stats wont work"
        if access_log == 'enabled':
            print_green("access_log", access_log_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="access_log" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="access_log" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("access_log", access_log_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="access_log" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="access_log" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # open_file_cache
        print('<li class="list-group-item">')
        print('<div class="row">')
        open_file_cache_hint = "increase performance, disable on dev environment for no caching"
        if open_file_cache == 'enabled':
            print_green("open_file_cache", open_file_cache_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="open_file_cache" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="open_file_cache" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("open_file_cache", open_file_cache_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="open_file_cache" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="open_file_cache" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # clickjacking_protect
        print('<li class="list-group-item">')
        print('<div class="row">')
        clickjacking_protect_hint = "add_header X-Frame-Options SAMEORIGIN;"
        if clickjacking_protect == 'enabled':
            print_green("clickjacking_protect", clickjacking_protect_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="clickjacking_protect" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="clickjacking_protect" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("clickjacking_protect", clickjacking_protect_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="clickjacking_protect" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="clickjacking_protect" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # disable_contenttype_sniffing
        print('<li class="list-group-item">')
        print('<div class="row">')
        disable_contenttype_sniffing_hint = "add_header X-Content-Type-Options nosniff;"
        if disable_contenttype_sniffing == 'enabled':
            print_green("disable_contenttype_sniffing", disable_contenttype_sniffing_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="disable_contenttype_sniffing" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="disable_contenttype_sniffing" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("disable_contenttype_sniffing", disable_contenttype_sniffing_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="disable_contenttype_sniffing" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="disable_contenttype_sniffing" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # xss_filter
        print('<li class="list-group-item">')
        print('<div class="row">')
        xss_filter_hint = 'add_header X-XSS-Protection "1; mode=block";'
        if xss_filter == 'enabled':
            print_green("xss_filter", xss_filter_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="xss_filter" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="xss_filter" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("xss_filter", xss_filter_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="xss_filter" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="xss_filter" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # hsts
        print('<li class="list-group-item">')
        print('<div class="row">')
        hsts_hint = 'add_header Strict-Transport-Security "max-age=31536000" always;'
        if hsts == 'enabled':
            print_green("hsts", hsts_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="hsts" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="hsts" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("hsts", hsts_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="hsts" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="hsts" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # dos_mitigate
        print('<li class="list-group-item">')
        print('<div class="row">')
        dos_mitigate_hint = "Enable only when under a dos attack"
        if dos_mitigate == 'enabled':
            print_green("dos_mitigate", dos_mitigate_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="dos_mitigate" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="dos_mitigate" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("dos_mitigate", dos_mitigate_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="dos_mitigate" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="dos_mitigate" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # test_cookie
        print('<li class="list-group-item">')
        print('<div class="row">')
        test_cookie_hint = "Disable most bots except good ones like google/yahoo etc with a cookie challenge"
        if test_cookie == 'enabled':
            print_green("test_cookie", test_cookie_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="test_cookie" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="test_cookie" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("test_cookie", test_cookie_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="test_cookie" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="test_cookie" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # symlink_protection
        print('<li class="list-group-item">')
        print('<div class="row">')
        symlink_protection_hint = "Access to a file is denied if any component of the pathname is a symbolic link, and the link and object that the link points to have different owners"
        if symlink_protection == 'enabled':
            print_green("symlink_protection", symlink_protection_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="symlink_protection" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="symlink_protection" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("symlink_protection", symlink_protection_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="symlink_protection" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="symlink_protection" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # redirect_to_ssl
        print('<li class="list-group-item">')
        print('<div class="row">')
        redirect_to_ssl_hint = "redirect http:// to https:// "
        if redirect_to_ssl == 'enabled':
            print_green("redirect_to_ssl", redirect_to_ssl_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="redirect_to_ssl" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="redirect_to_ssl" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("redirect_to_ssl", redirect_to_ssl_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="redirect_to_ssl" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="redirect_to_ssl" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # redirect_aliases
        print('<li class="list-group-item">')
        print('<div class="row">')
        redirect_aliases_hint = "redirect all alias domains to the main domain"
        if redirect_aliases == 'enabled':
            print_green("redirect_aliases", redirect_aliases_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="redirect_aliases" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="redirect_aliases" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("redirect_aliases", redirect_aliases_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="redirect_aliases" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="redirect_aliases" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # wwwredirect
        print('<li class="list-group-item">')
        www_redirect_hint = "select redirection mode"
        print('<div class="row">')
        if wwwredirect == 'none':
            print_red("www redirect", www_redirect_hint)
        else:
            print_green("www redirect", www_redirect_hint)
        print('<div class="col-sm-6 col-radio">')
        print('<select name="wwwredirect">')
        if wwwredirect == 'none':
            print(('<option selected value="none">no redirection</option>'))
            print(('<option value="tononwww">redirect www. to non-www</option>'))
            print(('<option value="towww">redirect non-www to www.</option>'))
        elif wwwredirect == 'towww':
            print(('<option value="none">no redirection</option>'))
            print(('<option value="tononwww">redirect www. to non-www</option>'))
            print(('<option selected value="towww">redirect non-www to www.</option>'))
        elif wwwredirect == 'tononwww':
            print(('<option value="none">no redirection</option>'))
            print(('<option selected value="tononwww">redirect www. to non-www</option>'))
            print(('<option value="towww">redirect non-www to www.</option>'))
        print('</select>')
        print('</div>')
        print('</div>')
        print('</li>')
        # URL Redirect
        print('<li class="list-group-item">')
        print('<div class="row">')
        url_redirect_hint = "select redirection status 301 or 307"
        if redirectstatus == 'none':
            print_red("URL Redirect", url_redirect_hint)
        else:
            print_green("URL Redirect", url_redirect_hint)
        print('<div class="col-sm-6 col-radio">')
        print('<select name="redirectstatus">')
        if redirectstatus == 'none':
            print(('<option selected value="none">no redirection</option>'))
            print(('<option value="301">Permanent Redirect</option>'))
            print(('<option value="307">Temporary Redirect</option>'))
        elif redirectstatus == '301':
            print(('<option value="none">no redirection</option>'))
            print(('<option value="307">Temporary Redirect</option>'))
            print(('<option selected value="301">Permanent Redirect</option>'))
        elif redirectstatus == '307':
            print(('<option value="none">no redirection</option>'))
            print(('<option selected value="307">Temporary Redirect</option>'))
            print(('<option value="301">Permanent Redirect</option>'))
        print('</select>')
        print('</div>')
        print('</div>')
        print('</li>')
        # Append request_uri to redirect
        print('<li class="list-group-item">')
        print('<div class="row">')
        append_requesturi_hint = 'append $$request_uri to the redirect URL'
        if append_requesturi == 'enabled':
            print_green("append $request_uri to redirecturl", append_requesturi_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="append_requesturi" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="append_requesturi" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("append $request_uri to redirecturl", append_requesturi_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="append_requesturi" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="append_requesturi" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        # Redirect URL
        print('<li class="list-group-item">')
        print('<div class="row">')
        redirecturl_hint = "A Valid URL, eg: http://mynewurl.tld"
        if redirecturl == "none":
            print_red("Redirect to URL", redirecturl_hint)
        else:
            print_green("Redirect to URL", redirecturl_hint)
        print('<div class="col-sm-6 col-radio">')
        print('<input class="form-control" placeholder='+redirecturl+' type="text" name="redirecturl">')
        print('</div>')
        print('</div>')
        print('</li>')
        # end
        print('</ul>')
        # Pass on the domain name to the next stage
        print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
        print('<input class="btn btn-primary" type="submit" value="Submit">')
        print('</form>')
    else:
        print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> domain-data file i/o error</div>')
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden</div>')
print('</div>')
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-hand-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
