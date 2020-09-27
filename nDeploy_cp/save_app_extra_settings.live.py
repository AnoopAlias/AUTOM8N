#!/usr/bin/python

import commoninclude
import os
import yaml
import cgi
import cgitb
import sys
import re
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"


cgitb.enable()

commoninclude.close_cpanel_liveapisock()
form = cgi.FieldStorage()


print_simple_header()


# Get the domain name
if 'domain' in form.keys():
    mydomain = form.getvalue('domain')
else:
    commoninclude.print_error('Error: Forbidden::domain')
    sys.exit(0)
# Getting the current domain data
profileyaml = installation_path + "/domain-data/" + mydomain
if os.path.isfile(profileyaml):
    # Get all config settings from the domains domain-data config file
    with open(profileyaml, 'r') as profileyaml_data_stream:
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
    try:
        current_dev_mode = yaml_parsed_profileyaml.get('dev_mode')
    except KeyError:
        current_dev_mode = 'disabled'
else:
    commoninclude.print_error('Error: Domain data file i/o error')
    sys.exit(0)
if form.getvalue('thesubdir'):
    thesubdir = form.getvalue('thesubdir')
    subdir_apps_dict = yaml_parsed_profileyaml.get('subdir_apps')
    if subdir_apps_dict:
        if subdir_apps_dict.get(thesubdir):
            the_subdir_dict = subdir_apps_dict.get(thesubdir)
            current_redirecturl = the_subdir_dict.get('redirecturl', "none")
            # auth_basic
            if 'auth_basic' in form.keys():
                auth_basic = form.getvalue('auth_basic')
                the_subdir_dict['auth_basic'] = auth_basic
            else:
                commoninclude.print_error('Error: Forbidden::auth_basic')
                sys.exit(0)
            # proxy_to_master
            if 'proxy_to_master' in form.keys():
                proxy_to_master = form.getvalue('proxy_to_master')
                the_subdir_dict['proxy_to_master'] = proxy_to_master
            else:
                commoninclude.print_error('Error: Forbidden::proxy_to_master')
                sys.exit(0)
            # mod_security
            if 'mod_security' in form.keys():
                mod_security = form.getvalue('mod_security')
                the_subdir_dict['mod_security'] = mod_security
            else:
                commoninclude.print_error('Error: Forbidden::mod_security')
                sys.exit(0)
            # set_expire_static
            if 'set_expire_static' in form.keys():
                set_expire_static = form.getvalue('set_expire_static')
                the_subdir_dict['set_expire_static'] = set_expire_static
            else:
                commoninclude.print_error('Error: Forbidden::set_expire_static')
                sys.exit(0)
            # redirectstatus
            if 'redirectstatus' in form.keys():
                redirectstatus = form.getvalue('redirectstatus')
                the_subdir_dict['redirectstatus'] = redirectstatus
            else:
                commoninclude.print_error('Error: Forbidden::redirectstatus')
                sys.exit(0)
            # redirecturl
            if redirectstatus != "none":
                if 'redirecturl' in form.keys():
                    redirecturl = form.getvalue('redirecturl')
                    if not redirecturl == "none":
                        regex = re.compile(
                            r'^(?:http|ftp)s?://'
                            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                            r'localhost|'
                            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                            r'(?::\d+)?'
                            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                        it_matches = regex.match(redirecturl)
                        if not it_matches:
                            commoninclude.print_error('Error: Invalid Redirect URL. The URL must be something like https://google.com')
                            sys.exit(0)
                        else:
                            the_subdir_dict['redirecturl'] = redirecturl
                    else:
                        the_subdir_dict['redirecturl'] = current_redirecturl
            # append_requesturi
            if 'append_requesturi' in form.keys():
                append_requesturi = form.getvalue('append_requesturi')
                the_subdir_dict['append_requesturi'] = append_requesturi
            else:
                commoninclude.print_error('Error: Forbidden::append_requesturi')
                sys.exit(0)
            subdir_apps_dict[thesubdir] = the_subdir_dict
            yaml_parsed_profileyaml['subdir_apps'] = subdir_apps_dict
        else:
            commoninclude.print_error('Missing subdir::'+thesubdir+' in domain data')
    else:
        commoninclude.print_error('Missing subdir_apps section in domain data')
else:
    current_redirecturl = yaml_parsed_profileyaml.get('redirecturl', "none")
    # auth_basic
    if 'auth_basic' in form.keys():
        auth_basic = form.getvalue('auth_basic')
        yaml_parsed_profileyaml['auth_basic'] = auth_basic
    else:
        commoninclude.print_error('Error: Forbidden::auth_basic')
        sys.exit(0)
    # set_expire_static
    if 'set_expire_static' in form.keys():
        set_expire_static = form.getvalue('set_expire_static')
        dev_check = yaml_parsed_profileyaml.get('dev_mode', 'disabled')
        if dev_check == 'enabled':
            set_expire_static = 'disabled'
        else:
            yaml_parsed_profileyaml['set_expire_static'] = set_expire_static
    else:
        commoninclude.print_error('Error: Forbidden::set_expire_static')
        sys.exit(0)
    # mod_security
    if 'mod_security' in form.keys():
        mod_security = form.getvalue('mod_security')
        yaml_parsed_profileyaml['mod_security'] = mod_security
    else:
        commoninclude.print_error('Error: Forbidden::mod_security')
        sys.exit(0)
    # autoindex
    if 'autoindex' in form.keys():
        autoindex = form.getvalue('autoindex')
        yaml_parsed_profileyaml['autoindex'] = autoindex
    else:
        commoninclude.print_error('Error: Forbidden::autoindex')
        sys.exit(0)
    # ssl_offload
    if 'ssl_offload' in form.keys():
        ssl_offload = form.getvalue('ssl_offload')
        yaml_parsed_profileyaml['ssl_offload'] = ssl_offload
    else:
        commoninclude.print_error('Error: Forbidden::ssl_offload')
        sys.exit(0)
    # pagespeed
    if 'pagespeed' in form.keys():
        pagespeed = form.getvalue('pagespeed')
        yaml_parsed_profileyaml['pagespeed'] = pagespeed
    else:
        commoninclude.print_error('Error: Forbidden::pagespeed')
        sys.exit(0)
    # pagespeed_filter
    if 'pagespeed_filter' in form.keys():
        pagespeed_filter = form.getvalue('pagespeed_filter')
        yaml_parsed_profileyaml['pagespeed_filter'] = pagespeed_filter
    else:
        commoninclude.print_error('Error: Forbidden::pagespeed_filter')
        sys.exit(0)
    # brotli
    if 'brotli' in form.keys():
        brotli = form.getvalue('brotli')
        yaml_parsed_profileyaml['brotli'] = brotli
    else:
        commoninclude.print_error('Error: Forbidden::brotli')
        sys.exit(0)
    # gzip
    if 'gzip' in form.keys():
        gzip = form.getvalue('gzip')
        yaml_parsed_profileyaml['gzip'] = gzip
    else:
        commoninclude.print_error('Error: Forbidden::gzip')
        sys.exit(0)
    # http2
    if 'http2' in form.keys():
        http2 = form.getvalue('http2')
        yaml_parsed_profileyaml['http2'] = http2
    else:
        commoninclude.print_error('Error: Forbidden::http2')
        sys.exit(0)
    # access_log
    if 'access_log' in form.keys():
        access_log = form.getvalue('access_log')
        yaml_parsed_profileyaml['access_log'] = access_log
    else:
        commoninclude.print_error('Error: Forbidden::access_log')
        sys.exit(0)
    # open_file_cache
    if 'open_file_cache' in form.keys():
        open_file_cache = form.getvalue('open_file_cache')
        dev_check = yaml_parsed_profileyaml.get('dev_mode', 'disabled')
        if dev_check == 'enabled':
            open_file_cache = 'disabled'
        else:
            yaml_parsed_profileyaml['open_file_cache'] = open_file_cache
    else:
        commoninclude.print_error('Error: Forbidden::open_file_cache')
        sys.exit(0)
    # security_headers
    if 'security_headers' in form.keys():
        security_headers = form.getvalue('security_headers')
        yaml_parsed_profileyaml['security_headers'] = security_headers
    else:
        commoninclude.print_error('Error: Forbidden::security_headers')
        sys.exit(0)
    # dos_mitigate
    if 'dos_mitigate' in form.keys():
        dos_mitigate = form.getvalue('dos_mitigate')
        yaml_parsed_profileyaml['dos_mitigate'] = dos_mitigate
    else:
        commoninclude.print_error('Error: Forbidden::dos_mitigate')
        sys.exit(0)
    # test_cookie
    if 'test_cookie' in form.keys():
        test_cookie = form.getvalue('test_cookie')
        yaml_parsed_profileyaml['test_cookie'] = test_cookie
    else:
        commoninclude.print_error('Error: Forbidden::test_cookie')
        sys.exit(0)
    # symlink_protection
    if 'symlink_protection' in form.keys():
        symlink_protection = form.getvalue('symlink_protection')
        yaml_parsed_profileyaml['symlink_protection'] = symlink_protection
    else:
        commoninclude.print_error('Error: Forbidden::symlink_protection')
        sys.exit(0)
    # redirect_to_ssl
    if 'redirect_to_ssl' in form.keys():
        redirect_to_ssl = form.getvalue('redirect_to_ssl')
        yaml_parsed_profileyaml['redirect_to_ssl'] = redirect_to_ssl
    else:
        commoninclude.print_error('Error: Forbidden::redirect_to_ssl')
        sys.exit(0)
    # proxy_to_master
    if 'proxy_to_master' in form.keys():
        proxy_to_master = form.getvalue('proxy_to_master')
        dev_check = yaml_parsed_profileyaml.get('dev_mode', 'disabled')
        if dev_check == 'enabled':
            proxy_to_master = 'disabled'
        else:
            yaml_parsed_profileyaml['proxy_to_master'] = proxy_to_master
    else:
        commoninclude.print_error('Error: Forbidden::proxy_to_master')
        sys.exit(0)
    # redirect_aliases
    if 'redirect_aliases' in form.keys():
        redirect_aliases = form.getvalue('redirect_aliases')
        yaml_parsed_profileyaml['redirect_aliases'] = redirect_aliases
    else:
        commoninclude.print_error('Error: Forbidden::redirect_aliases')
        sys.exit(0)
    # wwwredirect
    if 'wwwredirect' in form.keys():
        wwwredirect = form.getvalue('wwwredirect')
        yaml_parsed_profileyaml['wwwredirect'] = wwwredirect
    else:
        commoninclude.print_error('Error: Forbidden::wwwredirect')
        sys.exit(0)
    # redirectstatus
    if 'redirectstatus' in form.keys():
        redirectstatus = form.getvalue('redirectstatus')
        yaml_parsed_profileyaml['redirectstatus'] = redirectstatus
    else:
        commoninclude.print_error('Error: Forbidden::redirectstatus')
        sys.exit(0)
    # redirecturl
    if redirectstatus != "none":
        if 'redirecturl' in form.keys():
            redirecturl = form.getvalue('redirecturl')
            if not redirecturl == "noredirection":
                regex = re.compile(
                    r'^(?:http|ftp)s?://'
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                    r'localhost|'
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                    r'(?::\d+)?'
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                it_matches = regex.match(redirecturl)
                if not it_matches:
                    commoninclude.print_error('Error: Invalid Redirect URL. The URL must be something like https://google.com ')
                    sys.exit(0)
                else:
                    yaml_parsed_profileyaml['redirecturl'] = redirecturl
            else:
                yaml_parsed_profileyaml['redirecturl'] = current_redirecturl
    # append_requesturi
    if 'append_requesturi' in form.keys():
        append_requesturi = form.getvalue('append_requesturi')
        yaml_parsed_profileyaml['append_requesturi'] = append_requesturi
    else:
        commoninclude.print_error('Error: Forbidden::append_requesturi')
        sys.exit(0)
    # dev_mode
    if 'dev_mode' in form.keys():
        dev_mode = form.getvalue('dev_mode')
        current_dev_mode = yaml_parsed_profileyaml.get('dev_mode', 'disabled')
        if dev_mode == 'enabled' and current_dev_mode == 'disabled':
            yaml_parsed_profileyaml['dev_open_file_cache'] = yaml_parsed_profileyaml.get('open_file_cache')
            yaml_parsed_profileyaml['dev_set_expire_static'] = yaml_parsed_profileyaml.get('set_expire_static')
            yaml_parsed_profileyaml['dev_proxy_to_master'] = yaml_parsed_profileyaml.get('proxy_to_master')
            yaml_parsed_profileyaml['dev_mode'] = 'enabled'
            yaml_parsed_profileyaml['open_file_cache'] = 'disabled'
            yaml_parsed_profileyaml['set_expire_static'] = 'disabled'
            yaml_parsed_profileyaml['proxy_to_master'] = 'enabled'
        elif dev_mode == 'disabled' and current_dev_mode == 'enabled':
            yaml_parsed_profileyaml['dev_mode'] = 'disabled'
            yaml_parsed_profileyaml['open_file_cache'] = yaml_parsed_profileyaml.get('dev_open_file_cache', 'enabled')
            yaml_parsed_profileyaml['set_expire_static'] = yaml_parsed_profileyaml.get('dev_set_expire_static', 'enabled')
            yaml_parsed_profileyaml['proxy_to_master'] = yaml_parsed_profileyaml.get('dev_proxy_to_master', 'disabled')
    else:
        commoninclude.print_error('Error: Forbidden::dev_mode')
        sys.exit(0)
with open(profileyaml, 'w') as yaml_file:
    yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)

commoninclude.print_success('Server settings saved!')

print_simple_footer()
