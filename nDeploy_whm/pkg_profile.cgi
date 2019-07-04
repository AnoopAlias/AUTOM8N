#!/usr/bin/python

import cgi
import cgitb
import os
import shutil
import yaml
import sys
from commoninclude import print_nontoast_error, return_label, return_disabled, bcrumb, print_header, print_modals, print_loader, cardheader, cardfooter


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
default_domain_data_file = installation_path+'/conf/domain_data_default.yaml'
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_header('Edit cPanel Package')
bcrumb('Edit cPanel Package','fas fa-box-open')


if form.getvalue('cpanelpkg'):
    if form.getvalue('cpanelpkg') == 'default':
        pkgdomaindata = installation_path+'/conf/domain_data_default_local.yaml'
    else:
        pkgdomaindata = installation_path+'/conf/domain_data_default_local_'+form.getvalue('cpanelpkg')+'.yaml'
    if not os.path.isfile(pkgdomaindata):
        shutil.copyfile(default_domain_data_file, pkgdomaindata)

    # Get all config settings from the domains domain-data config file
    with open(pkgdomaindata, 'r') as profileyaml_data_stream:
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)

    # App settings
    backend_category = yaml_parsed_profileyaml.get('backend_category')
    backend_version = yaml_parsed_profileyaml.get('backend_version')
    backend_path = yaml_parsed_profileyaml.get('backend_path')
    apptemplate_code = yaml_parsed_profileyaml.get('apptemplate_code')
    mod_security = yaml_parsed_profileyaml.get('mod_security', 'disabled')
    auth_basic = yaml_parsed_profileyaml.get('auth_basic', 'disabled')
    set_expire_static = yaml_parsed_profileyaml.get('set_expire_static', 'disabled')

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
    proxy_to_master = yaml_parsed_profileyaml.get('proxy_to_master', 'disabled')
    redirect_aliases = yaml_parsed_profileyaml.get('redirect_aliases', 'disabled')
    security_headers = yaml_parsed_profileyaml.get('security_headers', 'disabled')
    dos_mitigate = yaml_parsed_profileyaml.get('dos_mitigate', 'disabled')
    pagespeed_filter = yaml_parsed_profileyaml.get('pagespeed_filter', 'CoreFilters')
    redirecturl = yaml_parsed_profileyaml.get('redirecturl', 'none')
    redirectstatus = yaml_parsed_profileyaml.get('redirectstatus', 'none')
    append_requesturi = yaml_parsed_profileyaml.get('append_requesturi', 'disabled')
    test_cookie = yaml_parsed_profileyaml.get('test_cookie', 'disabled')
    symlink_protection = yaml_parsed_profileyaml.get('symlink_protection', 'disabled')
    user_config = yaml_parsed_profileyaml.get('user_config', 'disabled')
    subdir_apps = yaml_parsed_profileyaml.get('subdir_apps', None)
    phpmaxchildren = yaml_parsed_profileyaml.get('phpmaxchildren', '2')
    settings_lock = yaml_parsed_profileyaml.get('settings_lock', 'disabled')

    # Get the human friendly name of the app template
    if os.path.isfile(app_template_file):
        with open(app_template_file, 'r') as apptemplate_data_yaml:
            apptemplate_data_yaml_parsed = yaml.safe_load(apptemplate_data_yaml)
        apptemplate_dict = apptemplate_data_yaml_parsed.get(backend_category)
        apptemplate_description = apptemplate_dict.get(apptemplate_code)
    else:
        print_nontoast_error('Error: Application Template Data File Error')
        sys.exit(0)
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    else:
        print_nontoast_error('Error: Backend Configuration File Error')
        sys.exit(0)

    # Ok we are done with getting the settings, now lets present it to the user
    print('            <!-- WHM Starter Row -->')
    print('            <div class="row">')
    print('                <!-- First Column Start -->')
    print('                <div class="col-lg-6">') #Column
    print('')

    cardheader('Edit '+form.getvalue('cpanelpkg')+' cPanel Package','fas fa-users-cog')
    
    # Current Profile Status
    print('                        <form class="form mb-0" action="pkg_app_settings.cgi" method="get"> <!-- Form Start -->')
    print('                        <div class="card-body p-0"> <!-- Card Body Start -->') #Card Body Start
    print('                            <div class="row no-gutters align-items-center"> <!-- Row Start -->') #Row Start

    if backend_category == 'PROXY':
        if backend_version == 'httpd':

            # Running
            print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-play"></i>&nbsp;Running</div>')
            print('                                <div class="col-md-6 alert alert-success">Nginx</div>')

            # Backend
            print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-server"></i>&nbsp;Upstream</div>')
            print('                                <div class="col-md-6 alert alert-success">'+backend_version+'</div>')

            # Description
            print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-cog"></i>&nbsp;Config Template</div>')
            print('                                <div class="col-md-6 alert alert-success">'+apptemplate_description+'</div>')

            # .htaccess
            print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-file-code"></i>&nbsp;.htaccess</div>')
            print('                                <div class="col-md-6 alert alert-success"><i class="fas fa-check"></i>&nbsp;</div>')
        else:
            # Running
            print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-play"></i>&nbsp;Running</div>')
            print('                                <div class="col-md-6 alert alert-success">Nginx</div>')

            # Backend
            print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-server"></i>&nbsp;Upstream</div>')
            print('                                <div class="col-md-6 alert alert-success">'+backend_version+'</div>')

            # Description
            print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-cog"></i>&nbsp;Config Template</div>')
            print('                                <div class="col-md-6 alert alert-success">'+apptemplate_description+'</div>')

            # .htaccess
            print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-file-code"></i>&nbsp;.htaccess</div>')
            print('                                <div class="col-md-6 alert alert-danger"><i class="fas fa-times"></i>&nbsp;Ignored</div>')
    else:
        # Running
        print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-play"></i>&nbsp;Running</div>')
        print('                                <div class="col-md-6 alert alert-success">Nginx</div>')

        # Backend
        print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-server"></i>&nbsp;Upstream</div>')
        print('                                <div class="col-md-6 alert alert-success">'+backend_version+'</div>')

        # Description
        print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-cog"></i>&nbsp;Config Template</div>')
        print('                                <div class="col-md-6 alert alert-success">'+apptemplate_description+'</div>')

        # .htaccess
        print('                                <div class="col-md-6 alert alert-light"><i class="fas fa-file-code"></i>&nbsp;.htaccess</div>')
        print('                                <div class="col-md-6 alert alert-danger"><i class="fas fa-times"></i>&nbsp;Ignored</div>')

    print('                            </div> <!-- Row End -->') #Row End
    print('                        </div> <!-- Card Body End -->') #Card End

    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
    print('                            <div class="input-group">')
    print('                                <select name="backend" class="custom-select">')
    for backends_defined in backend_data_yaml_parsed.keys():
        if backends_defined == backend_category:
            print(('                                    <option selected value="'+backends_defined+'">'+backends_defined+'</option>'))
        else:
            print(('                                    <option value="'+backends_defined+'">'+backends_defined+'</option>'))
    print('                                </select>')
    
    #Pass on the domain name to the next stage
    print('                                <div class="input-group-append">')
    print(('                                    <input hidden name="cpanelpkg" value="'+form.getvalue('cpanelpkg')+'">'))
    print('                                    <button class="btn btn-outline-primary" type="submit">Select</button>')
    print('                                </div>')
    print('                            </div>')
    print('                        </div> <!-- Card Body End -->') #Card End
    print('                        </form> <!-- Form End -->')
    cardfooter('To change the upstream, choose a category above.')
    

    # General App Settings
    cardheader('General Application Settings','fas fa-sliders-h')
    print('                        <form class="form" id="toastForm17" onsubmit="return false;" method="post"> <!-- Form Start -->')
    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
    print('                            <div class="row"> <!-- Row Start -->') #Row Start

    # PHPMAXCHILDREN
    print('                                <div class="col-md-12">')
    print('                                    <div class="input-group btn-group mt-0 mb-2">')
    print('                                        <div class="input-group-prepend">')
    print('                                            <span class="input-group-text">')
    phpmaxchildren_hint = " The Maximum amount of PHP processes that can be spawned. "
    print('                                                '+return_label("PHP MAXCHILDREN", phpmaxchildren_hint))
    print('                                            </span>')
    print('                                        </div>')
    print(('                                        <input class="form-control" placeholder='+phpmaxchildren+' value='+phpmaxchildren+' type="text" name="phpmaxchildren">'))
    print('                                    </div>')
    print('                                </div>')

    # autoindex
    autoindex_hint = " Enable for Native NGINX directory listing. "
    print('                                '+return_label("autoindex", autoindex_hint))
    if autoindex == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="autoindex" value="enabled" id="AutoIndexOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="autoindex" value="disabled" id="AutoIndexOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="autoindex" value="enabled" id="AutoIndexOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="autoindex" value="disabled" id="AutoIndexOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # ssl_offload
    ssl_offload_hint = " Enable for a performance increase. Disable if a redirect loop error occurs. "
    print('                                '+return_label("ssl_offload", ssl_offload_hint))
    if ssl_offload == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="ssl_offload" value="enabled" id="SslOffloadOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="ssl_offload" value="disabled" id="SslOffloadOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="ssl_offload" value="enabled" id="SslOffloadOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="ssl_offload" value="disabled" id="SslOffloadOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # proxy_to_master
    proxy_to_master_hint = " When running in a cluster, PROXY to MASTER instead of local server. "
    print('                                '+return_label("proxy_to_master", proxy_to_master_hint))
    if proxy_to_master == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="proxy_to_master" value="enabled" id="ProxyMasterOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="proxy_to_master" value="disabled" id="ProxyMasterOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="proxy_to_master" value="enabled" id="ProxyMasterOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="proxy_to_master" value="disabled" id="ProxyMasterOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # access_log
    access_log_hint = " Disabling access_log will increase performance, but cPanel stats fail to work. "
    print('                                '+return_label("access_log", access_log_hint))
    if access_log == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="access_log" value="enabled" id="AccessLogOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="access_log" value="disabled" id="AccessLogOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="access_log" value="enabled" id="AccessLogOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="access_log" value="disabled" id="AccessLogOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # open_file_cache
    open_file_cache_hint = " Enable for performance increase. Disable on development environment to not cache. "
    print('                                '+return_label("open_file_cache", open_file_cache_hint))
    if open_file_cache == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="open_file_cache" value="enabled" id="OpenFileCacheOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="open_file_cache" value="disabled" id="OpenFileCacheOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="open_file_cache" value="enabled" id="OpenFileCacheOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="open_file_cache" value="disabled" id="OpenFileCacheOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    print('                            </div> <!-- Row End -->') #End Row
    print('                        </div> <!-- Card Body End -->') #Card End

    cardfooter('')

    # Security Settings
    cardheader('Security Settings','fas fa-shield-alt')
    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
    print('                            <div class="row"> <!-- Row Start -->') #Row Start
    
    # settings_lock
    settings_lock_hint = " Lock Application Server and Security Settings within cPanel. "
    print('                                '+return_label("settings_lock", settings_lock_hint))
    if settings_lock == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="settings_lock" value="enabled" id="SettingsLockOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="settings_lock" value="disabled" id="SettingsLockOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="settings_lock" value="enabled" id="SettingsLockOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="settings_lock" value="disabled" id="SettingsLockOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # security_headers
    security_headers_hint = " X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, HSTS "
    print('                                '+return_label("security_headers", security_headers_hint))
    if security_headers == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="security_headers" value="enabled" id="SecurityHeadersOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="security_headers" value="disabled" id="SecurityHeadersOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="security_headers" value="enabled" id="SecurityHeadersOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        label class="btn btn-light active">')
        print('                                            <input type="radio" name="security_headers" value="disabled" id="SecurityHeadersOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # dos_mitigate
    dos_mitigate_hint = " Enable ONLY when under a (D)DOS Attack. "
    print('                                '+return_label("dos_mitigate", dos_mitigate_hint))
    if dos_mitigate == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="dos_mitigate" value="enabled" id="DosMitigateOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="dos_mitigate" value="disabled" id="DosMitigateOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="dos_mitigate" value="enabled" id="DosMitigateOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="dos_mitigate" value="disabled" id="DosMitigateOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # test_cookie
    test_cookie_hint = " Allow good bots in (like Google/Yahoo). Disable most bad bots by using a cookie challenge. "
    print('                                '+return_label("bot_mitigate", test_cookie_hint))
    if os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):
        if test_cookie == 'enabled':
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('                                        label class="btn btn-light active">')
            print('                                            <input type="radio" name="test_cookie" value="enabled" id="TestCookieOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="test_cookie" value="disabled" id="TestCookieOff" autocomplete="off"> Disabled')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
        else:
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="test_cookie" value="enabled" id="TestCookieOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="test_cookie" value="disabled" id="TestCookieOff" autocomplete="off" checked> Disabled')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
    else:
        print('                                '+return_disabled())
        print(('                                <input hidden name="test_cookie" value="'+test_cookie+'">'))

    # symlink_protection
    symlink_protection_hint = " Access to a file is denied if any component of the pathname is a symbolic link, and if the link and object that the link points to has different owners. "
    print('                                '+return_label("symlink_protection", symlink_protection_hint))
    if symlink_protection == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="symlink_protection" value="enabled" id="SymlinkProtectionOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="symlink_protection" value="disabled" id="SymlinkProtectionOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="symlink_protection" value="enabled" id="SymlinkProtectionOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="symlink_protection" value="disabled" id="SymlinkProtectionOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # mod_security
    mod_security_hint = " Mod Security v3 Web Application Firewall "
    print('                                '+return_label("mod_security", mod_security_hint))
    if os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
        if mod_security == 'enabled':
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="mod_security" value="enabled" id="ModSecurityOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="mod_security" value="disabled" id="ModSecurityOff" autocomplete="off"> Disabled')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
        else:
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="mod_security" value="enabled" id="ModSecurityOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="mod_security" value="disabled" id="ModSecurityOff" autocomplete="off" checked> Disabled')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
    else:
        print('                                '+return_disabled())
        print(('                                <input hidden name="mod_security" value="'+mod_security+'">'))

    print('                            </div> <!-- Row End -->') #End Row
    print('                        </div> <!-- Card Body End -->') #Card End
    cardfooter('')

    #First Column End
    print('                <!-- First Column End -->')
    print('                </div>')
    print('')

    #Second Column
    print('                <!-- Second Column Start -->')
    print('                <div class="col-lg-6">') #Right Column
    print('')

    # Content Optimizations
    cardheader('Content Optimizations','fas fa-dumbbell')
    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
    print('                            <div class="row"> <!-- Row Start -->') #Row Start

    # set_expire_static
    set_expire_static_hint = " Set Expires/Cache-Control headers for STATIC content. "
    print('                                '+return_label("set expires header", set_expire_static_hint))
    if set_expire_static == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="set_expire_static" value="enabled" id="SetExpireStaticOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="set_expire_static" value="disabled" id="SetExpireStaticOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # pagespeed
    pagespeed_hint = " Delivers PageSpeed-optimized pages, but is resource intensive. "
    print('                                '+return_label("pagespeed", pagespeed_hint))
    if os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
        if pagespeed == 'enabled':
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="pagespeed" value="enabled" id="PagespeedOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="pagespeed" value="disabled" id="PagespeedOff" autocomplete="off"> Disabled')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
        else:
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="pagespeed" value="enabled" id="PagespeedOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="pagespeed" value="disabled" id="PagespeedOff" autocomplete="off" checked> Disabled')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
    else:
        print('                                '+return_disabled())
        print(('                                <input hidden name="pagespeed" value="'+pagespeed+'">'))

    # pagespeed filter level
    pagespeed_filter_hint = " CoreFilters loads the Core Filters, PassThrough allows you to enable individual filters via a custom NGINX Configuration. "
    print('                                '+return_label("pagespeed filters", pagespeed_filter_hint))
    if os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
        if pagespeed_filter == 'CoreFilters':
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="pagespeed_filter" value="CoreFilters" id="PagespeedFilterOn" autocomplete="off" checked> Core')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="pagespeed_filter" value="PassThrough" id="PagespeedFilterOff" autocomplete="off"> Pass')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
        else:
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="pagespeed_filter" value="CoreFilters" id="PagespeedFilterOn" autocomplete="off"> Core')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="pagespeed_filter" value="PassThrough" id="PagespeedFilterOff" autocomplete="off" checked> Pass')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
    else:
        print('                                '+return_disabled())
        print(('                                <input hidden name="pagespeed_filter" value="'+pagespeed_filter+'">'))


    # brotli
    brotli_hint = " A newer bandwidth optimization created by Google. It is resource intensive and applies to TLS (HTTPS) ONLY. "
    print('                                '+return_label("brotli", brotli_hint))
    if os.path.isfile('/etc/nginx/modules.d/brotli.load'):
        if brotli == 'enabled':
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="brotli" value="enabled" id="BrotliOn" autocomplete="off" checked> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="brotli" value="disabled" id="BrotliOff" autocomplete="off"> Disabled')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
        else:
            print('                                <div class="col-md-6">')
            print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
            print('                                        <label class="btn btn-light">')
            print('                                            <input type="radio" name="brotli" value="enabled" id="BrotliOn" autocomplete="off"> Enabled')
            print('                                        </label>')
            print('                                        <label class="btn btn-light active">')
            print('                                            <input type="radio" name="brotli" value="disabled" id="BrotliOff" autocomplete="off" checked> Disabled')
            print('                                        </label>')
            print('                                    </div>')
            print('                                </div>')
    else:
        print('                                '+return_disabled())
        print(('                                <input hidden name="brotli" value="'+brotli+'">'))


    # gzip
    gzip_hint = " A bandwidth optimization that is mildly resource intensive. "
    print('                                '+return_label("gzip", gzip_hint))
    if gzip == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="gzip" value="enabled" id="GzipOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="gzip" value="disabled" id="GzipOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="gzip" value="enabled" id="GzipOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="gzip" value="disabled" id="GzipOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # http2
    http2_hint = " A newer protocol that works with TLS (HTTPS) Only. "
    print('                                '+return_label("http2", http2_hint))
    if http2 == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="http2" value="enabled" id="Http2On" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="http2" value="disabled" id="Http2Off" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mb-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="http2" value="enabled" id="Http2On" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="http2" value="disabled" id="Http2Off" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    print('                            </div> <!-- Row End -->') #End Row
    print('                        </div> <!-- Card Body End -->') #Card End

    cardfooter('')
    

    # Redirections
    cardheader('Redirections','fas fa-directions')
    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
    print('                            <div class="row"> <!-- Row Start -->') #Row Start

    # redirect_to_ssl
    redirect_to_ssl_hint = " Redirect HTTP -> HTTPS. "
    print('                                '+return_label("redirect_to_ssl", redirect_to_ssl_hint))
    if redirect_to_ssl == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="redirect_to_ssl" value="enabled" id="RedirectSslOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="redirect_to_ssl" value="disabled" id="RedirectSslOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:

        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="redirect_to_ssl" value="enabled" id="RedirectSslOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="redirect_to_ssl" value="disabled" id="RedirectSslOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # redirect_aliases
    redirect_aliases_hint = " Redirect all cPanel aliases to the main domain. "
    print('                                '+return_label("redirect_aliases", redirect_aliases_hint))
    if redirect_aliases == 'enabled':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="redirect_aliases" value="enabled" id="RedirectAliasesOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="redirect_aliases" value="disabled" id="RedirectAliasesOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="redirect_aliases" value="enabled" id="RedirectAliasesOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="redirect_aliases" value="disabled" id="RedirectAliasesOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # www redirect
    www_redirect_hint = " Select WWW redirection mode. "
    print('                                '+return_label("www redirect", www_redirect_hint))
    print('                                <div class="col-md-6">')
    print('                                    <div class="input-group btn-group">')
    print('                                        <select name="wwwredirect" class="custom-select">')
    if wwwredirect == 'none':
        print(('                                            <option selected value="none">No Redirection</option>'))
        print(('                                            <option value="tononwww">WWW -> Non-WWW</option>'))
        print(('                                            <option value="towww">Non-WWW -> WWW</option>'))
    elif wwwredirect == 'towww':
        print(('                                            <option value="none">No Redirection</option>'))
        print(('                                            <option value="tononwww">WWW -> Non-WWW</option>'))
        print(('                                            <option selected value="towww">Non-WWW -> WWW</option>'))
    elif wwwredirect == 'tononwww':
        print(('                                            <option value="none">No Redirection</option>'))
        print(('                                            <option selected value="tononwww">WWW -> Non-WWW</option>'))
        print(('                                            <option value="towww">Non-WWW -> WWW</option>'))
    print('                                        </select>')
    print('                                    </div>')
    print('                                </div>')

    # URL Redirect
    url_redirect_hint = " Select URL redirection type. "
    print('                                '+return_label("URL redirect", url_redirect_hint))
    print('                                <div class="col-md-6">')
    print('                                    <div class="input-group btn-group">')
    print('                                        <select name="redirectstatus" class="custom-select">')
    if redirectstatus == 'none':
        print(('                                            <option selected value="none">No Redirection</option>'))
        print(('                                            <option value="301">Permanent (301)</option>'))
        print(('                                            <option value="307">Temporary (307)</option>'))
    elif redirectstatus == '301':
        print(('                                            <option value="none">No Redirection</option>'))
        print(('                                            <option value="307">Temporary (307)</option>'))
        print(('                                            <option selected value="301">Permanent (301)</option>'))
    elif redirectstatus == '307':
        print(('                                            <option value="none">No Redirection</option>'))
        print(('                                            <option selected value="307">Temporary (307)</option>'))
        print(('                                            <option value="301">Permanent (301)</option>'))
    print('                                        </select>')
    print('                                    </div>')
    print('                                </div>')

    # Append request_uri to redirect
    append_requesturi_hint = ' Maintain the original Request URI ($request_uri (with arguments)). '
    print('                                '+return_label("append redirecturl", append_requesturi_hint))
    if append_requesturi == 'enabled' and redirectstatus != 'none':
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="append_requesturi" value="enabled" id="AppendRequesturiOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                           <input type="radio" name="append_requesturi" value="disabled" id="AppendRequesturiOff" autocomplete="off"> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')
    else:
        print('                                <div class="col-md-6">')
        print('                                    <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="append_requesturi" value="enabled" id="AppendRequesturiOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="append_requesturi" value="disabled" id="AppendRequesturiOff" autocomplete="off" checked> Disabled')
        print('                                        </label>')
        print('                                    </div>')
        print('                                </div>')

    # Redirect URL
    redirecturl_hint = "A Valid URL, eg: http://mynewurl.tld"

    print('                                <div class="col-md-12">')
    print('                                    <div class="input-group btn-group mb-0">')
    print('                                        <div class="input-group-prepend">')
    print('                                            <span class="input-group-text">')
    print('                                                '+return_label("Redirect to URL", redirecturl_hint))
    print('                                            </span>')
    print('                                        </div>')
    print(('                                        <input class="form-control" value='+redirecturl+' type="text" name="redirecturl">'))
    print('                                    </div>')
    print('                                </div>')

    print('                            </div> <!-- Row End -->') #End Row
    print('                        </div> <!-- Card Body End -->') #Card End
    cardfooter('')

    # Save settings
    cardheader('Save cPanel Package Settings')
    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
    print('                            <div class="row"> <!-- Row Start -->') #Row Start
    print('                                <div class="col-md-12">')

    # Pass on the package name to the next stage
    print(('                                    <input hidden name="cpanelpkg" value="'+form.getvalue('cpanelpkg')+'">'))
    print('                                    <button class="btn btn-outline-primary btn-block" type="submit">Save Settings</button>')
    print('                                </div>')
    print('                            </div> <!-- Row End -->') #End Row
    print('                        </div> <!-- Card Body End -->') #Card End
    print('                    </form> <!-- Form End -->')
    cardfooter('')

else:
    print_nontoast_error('<h3>Forbidden!</h3>Though shall not Pass!')
    sys.exit(0)

#Second Column End
print('                <!-- Second Column End -->')
print('                </div>')
print('')
print('            <!-- WHM End Row -->')
print('            </div>')
print('')
print('        </div> <!-- Main Container End -->')
print('')

print_modals()
print_loader()

print('    <!-- Body End -->')
print('    </body>')
print('</html>')