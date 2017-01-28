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
    print(('<div class="col-sm-6"><div class="label label-success" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


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
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-home"></span></a></li>')
print('<li><a href="xtendweb.live.py">Set Domain</a></li><li class="active">Server Settings</li>')
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
        # Ok we are done with getting the settings,now lets present it to the user
        print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div><div class="panel-body">'))
        print('<form id="config" class="form-inline" action="save_server_settings.live.py" method="post">')
        print('<ul class="list-group"><li class="list-group-item">')
        # autoindex
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
            print('<div class="radio"><label><input type="radio" name="autoindex" value="enabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        print('<li class="list-group-item">')
        # ssl_offload
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
        print('<li class="list-group-item">')
        # pagespeed
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
        print('<li class="list-group-item">')
        # brotli
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
        print('<li class="list-group-item">')
        # gzip
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
        print('<li class="list-group-item">')
        # http2
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
        print('<li class="list-group-item">')
        # access_log
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
        print('<li class="list-group-item">')
        # open_file_cache
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
        print('<li class="list-group-item">')
        # clickjacking_protect
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
        print('<li class="list-group-item">')
        # disable_contenttype_sniffing
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
        print('<li class="list-group-item">')
        # xss_filter
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
        print('<li class="list-group-item">')
        # content_security_policy
        print('<div class="row">')
        content_security_policy_hint = 'add_header Content-Security-Policy "script-src self www.google-analytics.com ajax.googleapis.com;";'
        if content_security_policy == 'enabled':
            print_green("content_security_policy", content_security_policy_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="content_security_policy" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="content_security_policy" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("content_security_policy", content_security_policy_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="content_security_policy" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="content_security_policy" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        print('<li class="list-group-item">')
        # hsts
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
        print('<li class="list-group-item">')
        # dos_mitigate
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
        print('<li class="list-group-item">')
        # naxsi
        print('<div class="row">')
        naxsi_hint = "NAXSI is a web application firewall"
        if naxsi == 'enabled':
            print_green("naxsi", naxsi_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="naxsi" value="enabled" checked/> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="naxsi" value="disabled" /> Disabled</label></div>')
            print('</div>')
        else:
            print_red("naxsi", naxsi_hint)
            print('<div class="col-sm-6 col-radio">')
            print('<div class="radio"><label><input type="radio" name="naxsi" value="enabled" /> Enabled</label></div>')
            print('<div class="radio"><label><input type="radio" name="naxsi" value="disabled" checked/> Disabled</label></div>')
            print('</div>')
            print('</div>')
        print('</li>')
        print('<li class="list-group-item">')
        # naxsi_mode
        print('<div class="row">')
        print('<div class="col-sm-6">')
        print(('<div class="label label-default" data-toggle="tooltip" title="active mode blocks requests on trigger">naxsi_mode</div>'))
        print('</div>')
        print('<div class="col-sm-6 col-radio">')
        print('<select name="naxsi_mode">')
        if naxsi_mode == 'learn':
            print(('<option selected value="learn">learn</option>'))
            print(('<option value="active">active</option>'))
        else:
            print(('<option value="learn">learn</option>'))
            print(('<option selected value="active">active</option>'))
        print('</select>')
        print('</div>')
        print('</div>')
        print('</li>')
        print('<li class="list-group-item">')
        # redirect_to_ssl
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
        print('<li class="list-group-item">')
        # redirect_aliases
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
        print('<li class="list-group-item">')
        # wwwredirect
        print('<div class="row">')
        print('<div class="col-sm-6">')
        print(('<div class="label label-default" data-toggle="tooltip" title="select redirection mode">www redirect</div>'))
        print('</div>')
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
print('<div class="panel-footer"><small>Powered by <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb</a> <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> Themed by <a target="_blank" href="http://www.stirstudiosdesign.com/">StirStudios</a></small></div>')
print('</div>')
print('<div class="help pull-right"><a target="_blank" href="http://xtendweb.gnusys.net/"><span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span> <em>Need Help?</em></a></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
