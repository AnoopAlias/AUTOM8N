#!/usr/bin/env python

import commoninclude
import os
import cgitb
import subprocess
import yaml
import psutil
import platform
import socket
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
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"

cgitb.enable()

commoninclude.print_header()

print('<body>')

commoninclude.print_branding()

print('<div id="main-container" class="container">')    # main container

print('		<nav aria-label="breadcrumb">')
print('			<ol class="breadcrumb">')
print('				<li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">Server Config</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row">')

print('			<div class="col-md-12">')  # top dash

nginx_status = False
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
    else:
        mycmdline = myprocess.cmdline()
    if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
        nginx_status = True
        break

watcher_status = False
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
    else:
        mycmdline = myprocess.cmdline()
    if '/opt/nDeploy/scripts/watcher.py' in mycmdline:
        watcher_status = True
        break

# System Status
print('				<div class="card">')  # card
print('					<div class="card-body p-0">')  # card-body
print('						<div class="row no-gutters row-3-col">')
print('					        <div class="col-md-4">')
print('					            <div class="p-3 bg-light border-bottom text-center">')
print('					                <h4 class="mb-0">Nginx Status</h4>')
print('                                 <ul class="list-unstyled mb-0">')
print('					                    <li><small>v1.2.4</small></li>')
if nginx_status:
    print('					                <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('					                <li class="mt-2 text-danger">Stopped <i class="fas fa-power-off ml-1"></i></li>')
print('                                 </ul>')
print('                             </div>')
print('					            <button class="btn btn-text btn-block">Reload</button>')
print('                         </div>')
print('					        <div class="col-md-4">')
print('					            <div class="p-3 bg-light border-bottom text-center">')
print('					                <h4 class="mb-0">Watcher Status</h4>')
print('                                 <ul class="list-unstyled mb-0">')
print('					                    <li><small>v1.2</small></li>')
if watcher_status:
    print('					                <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('					                <li class="mt-2 text-danger">Stopped <i class="fas fa-power-off ml-1"></i></li>')
print('                                 </ul>')
print('                             </div>')
print('					            <button class="btn btn-text btn-block">Restart</button>')
print('                         </div>')
print('					        <div class="col-md-4">')
print('					            <div class="p-3 bg-light border-bottom text-center">')
print('					                <h4 class="mb-0">Clear Caches</h4>')
print('                                 <ul class="list-unstyled mb-0">')
print('					                    <li><small>Redis</small></li>')
print('					                    <li class="mt-2"><i class="fas fa-memory ml-1"></i></li>')
print('                                 </ul>')
print('                             </div>')
print('					            <button class="btn btn-text btn-block">Flush All</button>')
print('                         </div>')
print('                     </div>')
print('                 </div>')
print('             </div>')

print('         </div>')  # end top dash

print('			<div class="col-lg-6">')  # col left

# System Health & Backup
print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fas fa-cogs float-right"></i> System Health & Backup</h5>')
print('					</div>')
print('					<div class="card-body p-0">')  # card-body
print('						<div class="row no-gutters row-2-col">')

# Net Data
myhostname = socket.gethostname()
print('							<div class="col-md-6">')
print('                             <a class="btn btn-text btn-block" href="https://'+myhostname+'/netdata/" target="_blank"><i class="fas fa-heartbeat"></i> Netdata <i class="fas fa-external-link-alt"></i></a>')
print('							</div>')

# Glances
print('							<div class="col-md-6">')
print('                             <a class="btn btn-text btn-block" href="https://'+myhostname+'/glances/" target="_blank"><i class="fas fa-eye"></i> Glances <i class="fas fa-external-link-alt"></i></a>')
print('							</div>')

# Borg Backup
print('							<div class="col-md-6">')

print('								<form class="form" method="get" action="setup_borg_backup.cgi">')
print('									<button class="btn btn-text btn-block" type="submit"><i class="fas fa-database"></i> Borg Backup</button>')
print('								</form>')

print('							</div>')

# Process Tracker
print('							<div class="col-md-6">')

print('								<form class="form" id="modalForm3" onsubmit="return false;">')
print('									<button type="submit" class="btn btn-text btn-block"><i class="fas fa-bug"></i> Check Processes</button>')
print('								</form>')

print('							</div>')

print('						</div>')  # row end
print('					</div>')  # card-body

print('				</div>')  # card end

# Cluster Status
if os.path.isfile(cluster_config_file):
    print('			<div class="card">')  # card
    print('				<div class="card-header">')
    print('					<h5 class="card-title mb-0"><i class="fas fa-align-justify float-right"></i> Cluster Status</h5>')
    print('				</div>')
    print('				<div class="card-body p-0">')  # card-body
    print('					<div class="row no-gutters row-1">')
    with open(cluster_config_file, 'r') as cluster_data_yaml:
        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    with open(homedir_config_file, 'r') as homedir_data_yaml:
        homedir_data_yaml_parsed = yaml.safe_load(homedir_data_yaml)
    homedir_list = homedir_data_yaml_parsed.get('homedir')
    for servername in cluster_data_yaml_parsed.keys():
        for myhome in homedir_list:
            filesync_status = False
            for myprocess in psutil.process_iter():
                # Workaround for Python 2.6
                if platform.python_version().startswith('2.6'):
                    mycmdline = myprocess.cmdline
                else:
                    mycmdline = myprocess.cmdline()
                if '/usr/bin/unison' in mycmdline and myhome+'_'+servername in mycmdline:
                    filesync_status = True
                    break
            if filesync_status:
                print(('		<div class="col-md-9 alert alert-light">'+myhome+'_'+servername+'</div>'))
                print(('		<div class="col-md-3 alert alert-success">In Sync</div>'))
            else:
                print(('		<div class="col-md-9 alert alert-light">'+myhome+'_'+servername+'</div>'))
                print(('		<div class="col-md-3 alert alert-danger">Out of Sync</div>'))
    print('					</div>')  # row end
    print('				</div>')  # card-body

    print('				<div class="card-body">')  # card-body

    print('					<form class="form mb-3" id="toastForm4" onsubmit="return false;">')
    print(('					<input class="hidden" name="mode" value="restart">'))
    print('						<button type="submit" class="btn btn-outline-primary btn-block ">Soft Restart Unison Sync</button>')
    print('					</form>')

    print('					<form class="form mb-0" id="toastForm5" onsubmit="return false;">')
    print(('					<input class="hidden" name="mode" value="reset">'))
    print('						<button type="submit" class="btn btn-outline-primary btn-block">Hard Reset Unison Sync</button>')
    print('					</form>')

    print('				</div>')  # card-body

    print('				<div class="card-footer">')
    print('					<small>Only perform a hard reset if the unison archive is corrupt. Unison archive rebuild is time consuming.</small>')
    print('				</div>')
    print('			</div>')  # card end

# Sync GeoDNS zone
if os.path.isfile(cluster_config_file):
    print('			<div class="card">')  # card
    print('				<div class="card-header">')
    print('					<h5 class="card-title mb-0"><i class="fas fa-sync float-right"></i>Sync gdnsd zone</h5>')
    print('				</div>')
    print('				<div class="card-body">')  # card-body

    print('					<form class="form" id="toastForm7" onsubmit="return false;">')
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('    							<label class="input-group-text">Zone</label>')
    print('							</div>')
    print('							<select name="user" class="custom-select">')
    user_list = os.listdir("/var/cpanel/users")
    for cpuser in sorted(user_list):
        if cpuser != 'nobody' and cpuser != 'system':
            print(('					<option value="'+cpuser+'">'+cpuser+'</option>'))
    print('					</select>')
    print('				</div>')
    print('				<button type="submit" class="btn btn-outline-primary btn-block ">Sync Dns Zone</button>')
    print('			</form>')
    print('				</div>')  # card-body end
    print('			</div>')  # card end

# Set Default PHP for AutoConfig
print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fab fa-php float-right"></i> Default PHP for Autoswitch</h5>')
print('					</div>')
print('                 <div class="card-body p-0">')  # card-body
print('					    <div class="row no-gutters row-1">')

# Default PHP
if os.path.isfile(installation_path+"/conf/preferred_php.yaml"):
    preferred_php_yaml = open(installation_path+"/conf/preferred_php.yaml", 'r')
    preferred_php_yaml_parsed = yaml.safe_load(preferred_php_yaml)
    preferred_php_yaml.close()
    phpversion = preferred_php_yaml_parsed.get('PHP')
    print(('					<div class="col-6 alert alert-light"><i class="fab fa-php"></i> Default PHP</div>'))
    print(('					<div class="col-6 alert alert-success">'+phpversion.keys()[0])+'</div>')
print('					    </div>')
print('                 </div>')  # end card-body

print('                 <div class="card-body">')  # card-body
print('						<form class="form" id="toastForm6" onsubmit="return false;">')
print('							<div class="input-group">')
print('								<div class="input-group-prepend">')
print('    								<label class="input-group-text">PHP</label>')
print('								</div>')

print('								<select name="phpversion" class="custom-select">')
backend_config_file = installation_path+"/conf/backends.yaml"
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()
if "PHP" in backend_data_yaml_parsed:
    php_backends_dict = backend_data_yaml_parsed["PHP"]
    for versions_defined in list(php_backends_dict.keys()):
        print(('						<option value="'+versions_defined+'">'+versions_defined+'</option>'))
print('								</select>')
print('							</div>')
print('							<button type="submit" class="btn btn-outline-primary btn-block ">Set Default PHP</button>')
print('						</form>')

print('					</div>')  # card-body end
print('					<div class="card-footer">')
print('						<small>If MultiPHP is enabled, the PHP version selected by MultiPHP is used by autoconfig. For best results, it is recommended to enable MultiPHP across all accounts.</small>')
print('					</div>')
print('				</div>')  # card end

# DDOS Protection
print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fas fa-user-shield float-right"></i> DDOS Protection</h5>')
print('					</div>')
print('					<div class="card-body p-0">')  # card-body
print('						<div class="row no-gutters row-2-col row-no-btm">')

if os.path.isfile('/etc/nginx/conf.d/dos_mitigate_systemwide.enabled'):
    print('						<div class="col-md-6 alert alert-light"><i class="fas fa-shield-alt"></i> Nginx</div>')
    print('						<div class="col-md-6">')
    print('							<div class="row no-gutters">')
    print('								<div class="col-6 alert alert-success">Enabled</div>')
    print('								<div class="col-6">')
    print('									<form id="toastForm1" class="form" onsubmit="return false;">')
    print('										<button type="submit" class="alert alert-info btn btn-info ">Disable</button>')
    print(('									<input class="hidden" name="ddos" value="disable">'))
    print('									</form>')
    print('								</div>')
    print('							</div>')
    print('						</div>')
else:
    print('						<div class="col-md-6 alert alert-light"><i class="fas fa-shield-alt"></i> Nginx</div>')
    print('						<div class="col-md-6">')
    print('							<div class="row no-gutters">')
    print('								<div class="col-6 alert alert-secondary">Disabled</div>')
    print('								<div class="col-6">')
    print('									<form id="toastForm1" class="form" onsubmit="return false;">')
    print('										<button type="submit" class="alert alert-info btn btn-info ">Enable</button>')
    print(('									<input class="hidden" name="ddos" value="enable">'))
    print('									</form>')
    print('								</div>')
    print('							</div>')
    print('						</div>')
try:
    with open(os.devnull, 'w') as FNULL:
        subprocess.call(['systemctl', '--version'], stdout=FNULL, stderr=subprocess.STDOUT)
except OSError:
    pass
else:
    with open(os.devnull, 'w') as FNULL:
        firehol_enabled = subprocess.call("systemctl is-active firehol.service", stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
    if firehol_enabled == 0:
        print('					<div class="col-md-6 alert alert-light"><i class="fas fa-shield-alt"></i> SYNPROXY</div>')
        print('					<div class="col-md-6">')
        print('						<div class="row no-gutters">')
        print('							<div class="col-6 alert alert-success">Enabled</div>')
        print('								<div class="col-6">')
        print('								<form id="toastForm2" class="form" onsubmit="return false;">')
        print('									<button type="submit" class="alert alert-info btn btn-info ">Disable</button>')
        print(('								<input class="hidden" name="ddos" value="disable">'))
        print('								</form>')
        print('							</div>')
        print('						</div>')
        print('					</div>')
    else:
        print('					<div class="col-md-6 alert alert-light"><i class="fas fa-shield-alt"></i> SYNPROXY</div>')
        print('					<div class="col-md-6">')
        print('						<div class="row no-gutters">')
        print('							<div class="col-6 alert alert-secondary">Disabled</div>')
        print('							<div class="col-6">')
        print('								<form id="toastForm2" class="form" onsubmit="return false;">')
        print('									<button type="submit" class="alert alert-info btn btn-info ">Enable</button>')
        print(('								<input class="hidden" name="ddos" value="enable">'))
        print('								</form>')
        print('							</div>')
        print('						</div>')
        print('					</div>')

print('						</div>')  # row end
print('					</div>')  # card-body end
print('					<div class="card-footer">')
print('						<small>Turn these settings on when you are under a DDOS Attack.</small><br>')
print('						<small>Disable CSF or any other firewall before turning on SYNPROXY (FireHol).</small>')
print('					</div>')
print('				</div>')  # card end

print('			</div>')  # col left end

print('			<div class="col-lg-6">')  # col right

# PHP-FPM Pool Editor
print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fas fa-sitemap float-right"></i> PHP-FPM Pool Editor</h5>')
print('					</div>')
print('					<div class="card-body">')  # card-body

print('						<form class="form" action="phpfpm_pool_editor.cgi" method="get">')
print('							<div class="input-group">')
print('								<div class="input-group-prepend">')
print('    								<label class="input-group-text" for="inputGroupSelect01">Account</label>')
print('								</div>')
print('								<select name="poolfile" class="custom-select">')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    conf_list = os.listdir("/opt/nDeploy/secure-php-fpm.d")
    for filename in sorted(conf_list):
        user, extension = filename.split('.')
        if user != 'nobody':
            print(('					<option value="/opt/nDeploy/secure-php-fpm.d/'+filename+'">'+user+'</option>'))
else:
    conf_list = os.listdir("/opt/nDeploy/php-fpm.d")
    for filename in sorted(conf_list):
        user, extension = filename.split('.')
        if user != 'nobody':
            print(('					<option value="/opt/nDeploy/php-fpm.d/'+filename+'">'+user+'</option>'))
print('								</select>')
print('							</div>')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    print(('					<input class="hidden" name="section" value="1">'))
else:
    print(('					<input class="hidden" name="section" value="0">'))
print('							<button class="btn btn-outline-primary btn-block" type="submit">Edit Settings</button>')
print('						</form>')

print('					</div>')  # card-body end
print('					<div class="card-footer">')
print('						<small>Settings such as: pm.max_requests, pm.max_spare_servers, session.save_path, pm.max_children.</small>')
print('					</div>')
print('				</div>')  # card end

# Map cPanel pkg to nginx setting
print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fas fa-box-open float-right"></i> Map cPanel pkg to nginx setting</h5>')
print('					</div>')
print('					<div class="card-body p-0">')  # card-body
print('						<div class="row no-gutters row-1">')

if os.path.isfile(installation_path+'/conf/lock_domaindata_to_package'):
    print('						<div class="col-md-6 alert alert-light"><i class="fas fa-box"></i>sync nginx to pkg</div>')
    print('						<div class="col-md-6">')
    print('							<div class="row no-gutters">')
    print('								<div class="col-6 alert alert-success">Enabled</div>')
    print('								<div class="col-6">')
    print('									<form class="form" method="post" id="toastForm16" onsubmit="return false;">')
    print('										<button type="submit" class="alert alert-info btn btn-info ">Disable</button>')
    print(('									<input class="hidden" name="package_lock" value="disabled">'))
    print('									</form>')
    print('								</div>')
    print('							</div>')
    print('						</div>')
else:
    print('						<div class="col-md-6 alert alert-light"><i class="fas fa-box"></i>sync nginx to pkg</div>')
    print('						<div class="col-md-6">')
    print('							<div class="row no-gutters">')
    print('								<div class="col-6 alert alert-secondary">Disabled</div>')
    print('								<div class="col-6">')
    print('									<form class="form" method="post" id="toastForm16" onsubmit="return false;">')
    print('										<button type="submit" class="alert alert-info btn btn-info ">Enable</button>')
    print(('									<input class="hidden" name="package_lock" value="enabled">'))
    print('									</form>')
    print('								</div>')
    print('							</div>')
    print('						</div>')

print('						</div>')  # row end
print('					</div>')  # card-body end

print('					<div class="card-body">')  # card-body
# Workaround for python 2.6
if platform.python_version().startswith('2.6'):
    listpkgs = subprocess.Popen('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', stdout=subprocess.PIPE, shell=True).communicate()[0]
else:
    listpkgs = subprocess.check_output('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', shell=True)
mypkgs = json.loads(listpkgs)
print('						<form class="form" action="pkg_profile.cgi" method="get">')
print('							<div class="input-group">')
print('								<div class="input-group-prepend">')
print('    								<label class="input-group-text" for="inputGroupSelect07">PKG</label>')
print('								</div>')

print('								<select name="cpanelpkg" class="custom-select">')
for thepkg in sorted(mypkgs.get('package')):
    pkgname = thepkg.get('name').encode('utf-8').replace(' ', '_')
    print(('							<option value="'+pkgname+'">'+pkgname+'</option>'))
print('								</select>')
print('							</div>')
print('							<button class="btn btn-outline-primary btn-block" type="submit">Edit Pkg</button>')
print('						</form>')

print('					</div>')  # card-body end
print('					<div class="card-footer">')
print('						<small>Sync nginx to pkg when enabled will reset all nginx config/settings on plan upgrade/downgrade.</small>')
print('					</div>')
print('				</div>')  # card end

# System Resource Limit
print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fas fa-compress float-right"></i> System Resource Limit</h5>')
print('					</div>')
print('					<div class="card-body">')  # card-body

with open('/etc/redhat-release', 'r') as releasefile:
    osrelease = releasefile.read().split(' ')[0]
if not osrelease == 'CloudLinux':
    if os.path.isfile('/usr/bin/systemctl'):
        # Next sub-section start here
        if os.path.isfile(installation_path+"/conf/secure-php-enabled"):  # if per user php-fpm master process is set
            userlist = os.listdir("/var/cpanel/users")
            print('			<form class="form" action="resource_limit.cgi" method="get">')
            print('				<div class="input-group">')
            print('					<div class="input-group-prepend">')
            print('    					<label class="input-group-text">User</label>')
            print('					</div>')
            print('					<select name="unit" class="custom-select">')
            for cpuser in sorted(userlist):
                if cpuser != 'nobody' and cpuser != 'system':
                    print(('			<option value="'+cpuser+'">'+cpuser+'</option>'))
            print('					</select>')
            print(('				<input class="hidden" name="mode" value="user">'))
            print('				</div>')
            print('				<button class="btn btn-outline-primary btn-block" type="submit">Set Limit</button>')
            print('			</form>')

            print('			<form class="form mt-4" action="resource_limit.cgi" method="get">')
            print('				<div class="input-group">')
            print('					<div class="input-group-prepend">')
            print('    					<label class="input-group-text">Service</label>')
            print('					</div>')
            print('					<select name="unit" class="custom-select">')
            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm", "ea-php73-php-fpm":
                print(('				<option value="'+service+'">'+service+'</option>'))
            print('					</select>')
            print(('				<input class="hidden" name="mode" value="service">'))
            print('				</div>')
            print('				<button class="btn btn-outline-primary btn-block" type="submit">Set Limit</button>')
            print('			</form>')
        else:
            print('			<form class="form" action="resource_limit.cgi" method="get">')
            print('				<div class="input-group">')
            print('					<div class="input-group-prepend">')
            print('    					<label class="input-group-text">Resource</label>')
            print('					</div>')
            print('					<select name="unit" class="custom-select">')
            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm", "ea-php73-php-fpm":
                print(('				<option value="'+service+'">'+service+'</option>'))
            print('					</select>')
            print(('				<input class="hidden" name="mode" value="service">'))
            print('				</div>')
            print('				<button class="btn btn-outline-primary btn-block" type="submit">Set Limit</button>')
            print('			</form>')

print('					</div>')  # card-body end
print('					<div class="card-footer">')
print('						<small>BlockIOWeight range is 10-1000, CPUShares range is 0-1024, MemoryLimit range is calculated using available memory.</small>')
print('					</div>')
print('				</div>')  # card end

print('			</div>')  # col right end
print('		</div>')  # row end

print('</div>')  # main-container end

commoninclude.print_modals()
commoninclude.print_loader()

print('</body>')
print('</html>')
