#!/usr/bin/env python


import os
import cgitb
import subprocess
import codecs
import platform
import yaml
import psutil
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cgitb.enable()


def print_green(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_red(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


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
print('<div id="main-container" class="container text-center">')  # marker1
print('<div class="row">')  # marker2
print('<div class="col-md-6 col-md-offset-3">')  # marker3
print('<div class="logo">')
print('<a href="xtendweb.cgi" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.cgi"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li class="active">Server Config</li>')
print('</ol>')

# Next section start here
print('<div class="panel panel-default">')  # marker6
print('<div class="panel-heading"><h3 class="panel-title">System status</h3></div>')
print('<div class="panel-body">')  # marker7
print('<ul class="list-group">')
print('<li class="list-group-item">')
print('<div class="row">')
nginx_status = False
for myprocess in psutil.process_iter():
    mycmdline = myprocess.cmdline()
    if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
        nginx_status = True
        break
if nginx_status:
    print(('<div class="col-sm-6">nginx</div>'))
    print(('<div class="col-sm-6"><div class="label label-success">ACTIVE</div></div>'))
else:
    print(('<div class="col-sm-6">nginx</div>'))
    print(('<div class="col-sm-6"><div class="label label-danger">INACTIVE</div></div>'))
print('</div>')
print('</li>')
print('<li class="list-group-item">')
print('<div class="row">')
watcher_status = False
for myprocess in psutil.process_iter():
    mycmdline = myprocess.cmdline()
    if '/opt/nDeploy/scripts/watcher.py' in mycmdline:
        watcher_status = True
        break
if watcher_status:
    print(('<div class="col-sm-6">ndeploy_watcher</div>'))
    print(('<div class="col-sm-6"><div class="label label-success">ACTIVE</div></div>'))
else:
    print(('<div class="col-sm-6">ndeploy_watcher</div>'))
    print(('<div class="col-sm-6"><div class="label label-danger">INACTIVE</div></div>'))
print('</div>')
print('</li>')
print('</ul>')
print('<ul class="list-group">')
print(('<div class="alert alert-info alert-top">'))
print(('nginx does not need restart. You should only use <kbd>nginx -s reload</kbd> or after rpm upgrade <kbd>/opt/nDeploy/scripts/nginx_upgrade_inplace.sh</kbd> if nginx binary is running. To restart ndeploy_watcher run <br><kbd>service ndeploy_watcher restart</kbd> from commandline'))
print(('</div>'))
print('</ul>')
print('</div>')  # div8
print('</div>')  # div7
# Next section start here
if os.path.isfile(cluster_config_file):
    print('<div class="panel panel-default">')  # marker6
    print('<div class="panel-heading"><h3 class="panel-title">Cluster status</h3></div>')
    print('<div class="panel-body">')  # marker7
    with open(cluster_config_file, 'r') as cluster_data_yaml:
        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    print('<ul class="list-group">')
    for servername in cluster_data_yaml_parsed.keys():
        print('<li class="list-group-item">')
        print('<div class="row">')
        filesync_status = False
        for myprocess in psutil.process_iter():
            mycmdline = myprocess.cmdline()
            if '/usr/bin/unison' in mycmdline and servername in mycmdline:
                filesync_status = True
                break
        if filesync_status:
            print(('<div class="col-sm-6">'+servername+'</div>'))
            print(('<div class="col-sm-6"><div class="label label-primary">IN SYNC</div></div>'))
        else:
            print(('<div class="col-sm-6">'+servername+'</div>'))
            print(('<div class="col-sm-6"><div class="label label-danger">OUT OF SYNC</div></div>'))
        print('</div>')
        print('</li>')
    print('</ul>')
    print('<form class="form-inline" action="fix_unison.cgi" method="post">')
    print(('<input style="display:none" name="mode" value="restart">'))
    print('<input class="btn btn-primary" type="submit" value="SOFT RESTART UNISON SYNC">')
    print('</form>')
    print(('<br>'))
    print('<form class="form-inline" action="fix_unison.cgi" method="post">')
    print(('<input style="display:none" name="mode" value="reset">'))
    print('<input class="btn btn-primary" type="submit" value="HARD RESET UNISON SYNC">')
    print('</form>')
    print('<ul class="list-group">')
    print(('<div class="alert alert-info alert-top">'))
    print(('Only perform a hard reset if the unison archive is corrupt.Unison archive rebuild is time consuming'))
    print(('</div>'))
    print('</ul>')
    print('</div>')  # div8
    print('</div>')  # div7
# Next section start here
listpkgs = subprocess.check_output('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', shell=True)
mypkgs = json.loads(listpkgs)
print('<div class="panel panel-default">')  # markera1
print('<div class="panel-heading"><h3 class="panel-title">Map cPanel pkg to nginx setting</h3></div>')
print('<div class="panel-body">')  # markera2
print('<form class="form-inline" action="pkg_profile.cgi" method="post">')
print('<select name="cpanelpkg">')
for thepkg in mypkgs.get('package'):
    pkgname = thepkg.get('name').replace(' ', '_')
    print(('<option value="'+pkgname+'">'+pkgname+'</option>'))
print('</select>')
print(('<br>'))
print(('<br>'))
print('<input class="btn btn-primary" type="submit" value="EDIT PKG">')
print('</form>')
print(('<br>'))
print(('<br>'))
if os.path.isfile(installation_path+'/conf/lock_domaindata_to_package'):
    print('<form class="form-group" action="lock_domain_data_to_package.cgi">')
    print('<input class="btn btn-xs btn-primary" type="submit" value="DISABLE CONFIG CHANGE WITH PKG">')
    print(('<input class="hidden" name="package_lock" value="disabled">'))
    print('</form>')
else:
    print('<form class="form-group" action="lock_domain_data_to_package.cgi">')
    print('<input class="btn btn-xs btn-warning" type="submit" value="ENABLE CONFIG CHANGE WITH PKG">')
    print(('<input class="hidden" name="package_lock" value="enabled">'))
    print('</form>')
print('<ul class="list-group">')
print(('<div class="alert alert-info alert-top">'))
print(('If you enable config change with package, nginx config for domain will be reset to package setting on plan upgrade/downgrade and all user settings will be lost'))
print(('</div>'))
print('</ul>')
print('</div>')  # markera2
print('</div>')  # markera1

# Next section start here
print('<div class="panel panel-default">')  # markera1
print('<div class="panel-heading"><h3 class="panel-title">PHP-FPM pool editor</h3></div>')
print('<div class="panel-body">')  # markera2
print('<form class="form-inline" action="phpfpm_pool_editor.cgi" method="post">')
print('<select name="poolfile">')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    conf_list = os.listdir("/opt/nDeploy/secure-php-fpm.d")
    for filename in conf_list:
        user, extension = filename.split('.')
        if user != 'nobody':
            print(('<option value="/opt/nDeploy/secure-php-fpm.d/'+filename+'">'+user+'</option>'))
else:
    conf_list = os.listdir("/opt/nDeploy/php-fpm.d")
    for filename in conf_list:
        user, extension = filename.split('.')
        if user != 'nobody':
            print(('<option value="/opt/nDeploy/php-fpm.d/'+filename+'">'+user+'</option>'))
print('</select>')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    print(('<input class="hidden" name="section" value="1">'))
else:
    print(('<input class="hidden" name="section" value="0">'))
print(('<br>'))
print(('<br>'))
print('<input class="btn btn-primary" type="submit" value="EDIT PHP SETTINGS">')
print('</form>')
print('</div>')  # markera2
print('</div>')  # markera1

# Next section start here
with open('/etc/redhat-release', 'r') as releasefile:
    osrelease = releasefile.read().split(' ')[0]
if not osrelease == 'CloudLinux':
    if 'el7' in platform.uname()[2]:
        # Next sub-section start here
        if os.path.isfile(installation_path+"/conf/secure-php-enabled"):  # if per user php-fpm master process is set
            # The API call and ensuring slices are present
            listresellers = subprocess.check_output('/usr/local/cpanel/bin/whmapi1 listresellers --output=json', shell=True)
            myresellers = json.loads(listresellers)
            resellerdata = myresellers.get('data')
            resellerlist = resellerdata.get('reseller')
            resellerlist.append('root')
            # Ensure the reseller slice is present in the system
            for owner in resellerlist:
                ownerslice = "/etc/systemd/system/"+owner+".slice"
                if not os.path.isfile(ownerslice):
                    generated_config = '[Slice]\n'
                    with codecs.open(ownerslice, 'w', 'utf-8') as confout:
                        confout.write(generated_config)
            print('<div class="panel panel-default">')  # markera1
            print('<div class="panel-heading"><h3 class="panel-title">Resource limit</h3></div>')
            print('<div class="panel-body">')  # markera2
            print('<div class="row">')  # markerb1
            print('<div class="col-sm-6">')  # markerc1
            print('<div class="panel panel-default">')  # markerc2
            print('<div class="panel-heading"><h3 class="panel-title">Reseller</h3></div>')
            print('<div class="panel-body">')  # markerc3
            print('<form class="form-inline" action="resource_limit.cgi" method="post">')
            print('<select name="unit">')
            for reseller in resellerlist:
                print(('<option value="'+reseller+'">'+reseller+'</option>'))
            print('</select>')
            print(('<input style="display:none" name="mode" value="user">'))
            print(('<br>'))
            print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
            print('</form>')
            print('</div>')  # markerc3
            print('</div>')  # markerc2
            print('</div>')  # markerc1
            print('<div class="col-sm-6">')  # markerc1
            print('<div class="panel panel-default">')  # markerc2
            print('<div class="panel-heading"><h3 class="panel-title">Service</h3></div>')
            print('<div class="panel-body">')  # markerc3
            print('<form class="form-inline" action="resource_limit.cgi" method="post">')
            print('<select name="unit">')
            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm":
                print(('<option value="'+service+'">'+service+'</option>'))
            print('</select>')
            print(('<input style="display:none" name="mode" value="service">'))
            print(('<br>'))
            print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
            print('</form>')
            print('</div>')  # markerc3
            print('</div>')  # markerc2
            print('</div>')  # markerc1
            print('</div>')  # markerb1
            print('</div>')  # markera2
            print('</div>')  # markera1
        else:
            # Next sub-section start here
            print('<div class="panel panel-default">')  # markera1
            print('<div class="panel-heading"><h3 class="panel-title">Service resource limit</h3></div>')
            print('<div class="panel-body">')  # markera2
            print('<form class="form-inline" action="resource_limit.cgi" method="post">')
            print('<select name="unit">')
            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm":
                print(('<option value="'+service+'">'+service+'</option>'))
            print('</select>')
            print(('<input style="display:none" name="mode" value="service">'))
            print(('<br>'))
            print(('<br>'))
            print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
            print('</form>')
            print('</div>')  # markera2
            print('</div>')  # markera1
# Next section start here
print('<div class="panel panel-default">')  # markera1
print('<div class="panel-heading"><h3 class="panel-title">Set Default PHP for AutoConfig</h3></div>')
print('<div class="panel-body">')  # markera2
print('<form class="form-inline" action="set_default_php.cgi" method="post">')
print('<select name="phpversion">')
backend_config_file = installation_path+"/conf/backends.yaml"
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()
if "PHP" in backend_data_yaml_parsed:
    php_backends_dict = backend_data_yaml_parsed["PHP"]
    for versions_defined in list(php_backends_dict.keys()):
        print(('<option value="'+versions_defined+'">'+versions_defined+'</option>'))
print('</select>')
print(('<br>'))
print(('<br>'))
print('<input class="btn btn-primary" type="submit" value="SET DEFAULT PHP">')
print('</form>')
if os.path.isfile(installation_path+"/conf/preferred_php.yaml"):
    preferred_php_yaml = open(installation_path+"/conf/preferred_php.yaml", 'r')
    preferred_php_yaml_parsed = yaml.safe_load(preferred_php_yaml)
    preferred_php_yaml.close()
    phpversion = preferred_php_yaml_parsed.get('PHP')
    print('<ul class="list-group">')
    print(('<div class="alert alert-info alert-top">'))
    print(('Current default PHP: '+phpversion.keys()[0])+'<br> If MultiPHP is enabled, the PHP version selected by MultiPHP is used by autoconfig. It is recommended that MultiPHP is enabled for all accounts for best results')
    print(('</div>'))
    print('</ul>')
print('</div>')  # markera2
print('</div>')  # markera1
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')  # marker3
print('</div>')  # marker2
print('</div>')  # marker1
print('</body>')
print('</html>')
