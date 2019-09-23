#!/usr/bin/env python

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
from commoninclude import bcrumb, return_prepend, print_header, print_footer, print_modals, print_loader, cardheader, cardfooter


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"
autom8n_version_info_file = installation_path+"/conf/version.yaml"
nginx_version_info_file = "/etc/nginx/version.yaml"
branding_file = installation_path+"/conf/branding.yaml"

cgitb.enable()
print_header('Home')
bcrumb('Home')

nginx_status = False
watcher_status = False
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
    else:
        mycmdline = myprocess.cmdline()
    if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
        nginx_status = True
    if '/opt/nDeploy/scripts/watcher.py' in mycmdline:
        watcher_status = True

# Get version of Nginx and plugin
with open(autom8n_version_info_file, 'r') as autom8n_version_info_yaml:
    autom8n_version_info_yaml_parsed = yaml.safe_load(autom8n_version_info_yaml)
with open(nginx_version_info_file, 'r') as nginx_version_info_yaml:
    nginx_version_info_yaml_parsed = yaml.safe_load(nginx_version_info_yaml)
nginx_version = nginx_version_info_yaml_parsed.get('nginx_version')
autom8n_version = autom8n_version_info_yaml_parsed.get('autom8n_version')

# Branding Data Pull
if os.path.isfile(branding_file):
    with open(branding_file, 'r') as brand_data_file:
        yaml_parsed_brand = yaml.safe_load(brand_data_file)
    brand = yaml_parsed_brand.get("brand", "AUTOM8N")
else:
    brand = "AUTOM8N"

print('            <!-- WHM Starter Row -->')
print('            <div id="dashboard" class="row">')
print('')
print('                <!-- Dash Widgets Start -->')

# Nginx Status
print('                                 <div class="col-sm-6 col-xl-3">')
cardheader('')
print('                                    <div class="card-body text-center">')
print('                                        <h4 class="mb-0">Nginx Status</h4>')
print('                                        <ul class="list-unstyled mb-0">')
print('                                            <li><small>'+nginx_version+'</small></li>')
if nginx_status:
    print('                                            <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                                            <li class="mt-2 text-danger">Stopped <i class="fas fa-power-off ml-1"></i></li>')
print('                                        </ul>')
print('                                    </div>')
print('                                    <form class="form" id="toastForm21" onsubmit="return false;"><input hidden name="action" value="nginxreload"><button class="btn btn-secondary btn-block mb-0">Reload</button></form>')
cardfooter('')
print('                                    </div>')

# Autom8n Version Status
print('                                 <div class="col-sm-6 col-xl-3">')
cardheader('')
print('                                    <div class="card-body text-center">')
print('                                        <h4 class="mb-0">Watcher Status</h4>')
print('                                        <ul class="list-unstyled mb-0">')
print('                                            <li><small>'+brand+' '+autom8n_version.replace("Autom8n ",'')+'</small></li>')
if watcher_status:
    print('                                            <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                                            <li class="mt-2 text-danger">Stopped <i class="fas fa-power-off ml-1"></i></li>')
print('                                        </ul>')
print('                                    </div>')
print('                                    <form class="form" id="toastForm22" onsubmit="return false;"><input hidden name="action" value="watcherrestart"><button class="btn btn-secondary btn-block mb-0">Restart</button></form>')
cardfooter('')
print('                                    </div>')

# Cache/Redis Status
print('                                 <div class="col-sm-6 col-xl-3">')
cardheader('')
print('                                    <div class="card-body text-center">')
print('                                        <h4 class="mb-0">Clear Caches</h4>')
print('                                        <ul class="list-unstyled mb-0">')
print('                                            <li><small>Redis</small></li>')
print('                                            <li class="mt-2"><i class="fas fa-memory ml-1"></i></li>')
print('                                        </ul>')
print('                                    </div>')
print('                                    <form class="form" id="toastForm23" onsubmit="return false;"><input hidden name="action" value="redisflush"><button class="btn btn-secondary btn-block mb-0">Flush All</button></form>')
cardfooter('')
print('                                  </div>')

# Disable Status
print('                                 <div class="col-sm-6 col-xl-3">')
cardheader('')
print('                                    <div class="card-body text-center">')
print('                                        <h4 class="mb-0">Disable Plugin</h4>')
print('                                        <ul class="list-unstyled mb-0">')
print('                                            <li><small>Disable</small></li>')
print('                                            <li class="mt-2"><i class="fas fa-times-circle ml-1"></i></li>')
print('                                        </ul>')
print('                                    </div>')
print('                                    <form class="form" id="toastForm23" onsubmit="return false;"><input hidden name="action" value="redisflush"><button class="btn btn-secondary btn-block mb-0">Disable</button></form>')
cardfooter('')
print('                                  </div>')

print('')
print('            <!-- WHM End Row -->')
print('            </div>')
print('')

print('            <!-- WHM Tabs Row -->')
print('            <div class="row justify-content-lg-center flex-nowrap">')

print('')
print('                <!-- Secondary Navigation -->')
print('                <div class="pl-3 col-md-3 nav flex-column nav-pills d-none d-lg-block d-xl-block d-xs-none d-sm-none" id="v-pills-tab" role="tablist" aria-orientation="vertical">')
print('                    <a class="nav-link active" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab">System Health & Backup</a>')
print('                    <a class="nav-link" id="v-pills-cluster-tab" data-toggle="pill" href="#v-pills-cluster" role="tab" aria-controls="v-pills-cluster">Cluster Status</a>')
print('                    <a class="nav-link" id="v-pills-zone-tab" data-toggle="pill" href="#v-pills-zone" role="tab" aria-controls="v-pills-zone">Sync GDNSD Zone</a>')
print('                    <a class="nav-link" id="v-pills-php-tab" data-toggle="pill" href="#v-pills-php" role="tab" aria-controls="v-pills-php">Default PHP for Autoswitch</a>')
print('                    <a class="nav-link" id="v-pills-dos-tab" data-toggle="pill" href="#v-pills-dos" role="tab" aria-controls="v-pills-dos">DDOS Protection</a>')
print('                    <a class="nav-link" id="v-pills-php_fpm-tab" data-toggle="pill" href="#v-pills-php_fpm" role="tab" aria-controls="v-pills-php_fpm">PHP-FPM Pool Editor</a>')
print('                    <a class="nav-link" id="v-pills-map-tab" data-toggle="pill" href="#v-pills-map" role="tab" aria-controls="v-pills-map">Map cPanel Package to NGINX</a>')
print('                    <a class="nav-link" id="v-pills-limit-tab" data-toggle="pill" href="#v-pills-limit" role="tab" aria-controls="v-pills-limit">System Resource Limit</a>')

print('                </div>')
print('')
print('                <div class="tab-content col-md-12 col-lg-9" id="v-pills-tabContent">')

print('                     <!-- Secondary Mobile Navigation -->')
print('                     <div class="d-lg-none d-xl-none dropdown nav">')
print('                         <button class="btn btn-secondary btn-block dropdown-toggle mb-3" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">')
print('                             Options')
print('                         </button>')
print('                         <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">')
print('                             <a class="dropdown-item" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab" aria-selected="false">System Health & Backup</a>')
print('                             <a class="dropdown-item" id="v-pills-cluster-tab" data-toggle="pill" href="#v-pills-cluster" role="tab" aria-controls="v-pills-cluster" aria-selected="false">Cluster Status</a>')
print('                             <a class="dropdown-item" id="v-pills-zone-tab" data-toggle="pill" href="#v-pills-zone" role="tab" aria-controls="v-pills-zone" aria-selected="false">Sync GDNSD Zone</a>')
print('                             <a class="dropdown-item" id="v-pills-php-tab" data-toggle="pill" href="#v-pills-php" role="tab" aria-controls="v-pills-php" aria-selected="false">Default PHP for Autoswitch</a>')
print('                             <a class="dropdown-item" id="v-pills-dos-tab" data-toggle="pill" href="#v-pills-dos" role="tab" aria-controls="v-pills-dos" aria-selected="false">DDOS Protection</a>')
print('                             <a class="dropdown-item" id="v-pills-php_fpm-tab" data-toggle="pill" href="#v-pills-php_fpm" role="tab" aria-controls="v-pills-php_fpm" aria-selected="false">PHP-FPM Pool Editor</a>')
print('                             <a class="dropdown-item" id="v-pills-map-tab" data-toggle="pill" href="#v-pills-map" role="tab" aria-controls="v-pills-map" aria-selected="false">Map cPanel Package to NGINX</a>')
print('                             <a class="dropdown-item" id="v-pills-limit-tab" data-toggle="pill" href="#v-pills-limit" role="tab" aria-controls="v-pills-limit" aria-selected="false">System Resource Limit</a>')
print('                         </div>')
print('                     </div>')

# System Tab
print('')
print('                     <!-- System Tab -->')
print('                     <div class="tab-pane fade show active" id="v-pills-system" role="tabpanel" aria-labelledby="v-pills-system-tab">')

# System Health & Backup
cardheader('System Health & Backup','fas fa-cogs')
print('                         <div class="card-body p-0">  <!-- Card Body Start -->')  # card-body
print('                             <div class="row no-gutters row-2-col"> <!-- Row Start -->')

# Net Data
myhostname = socket.gethostname()
print('                                 <div class="col-md-6">')
print('                                     <a class="btn btn-block" href="https://'+myhostname+'/netdata/" target="_blank"><i class="fas fa-heartbeat"></i> Netdata <i class="fas fa-external-link-alt"></i></a>')
print('                                 </div>')

# Glances
print('                                 <div class="col-md-6">')
print('                                     <a class="btn btn-block" href="https://'+myhostname+'/glances/" target="_blank"><i class="fas fa-eye"></i> Glances <i class="fas fa-external-link-alt"></i></a>')
print('                                 </div>')

# Borg Backup
print('                                 <div class="col-md-6">')
print('                                     <form class="form" method="get" action="setup_borg_backup.cgi">')
print('                                         <button class="btn btn-block" type="submit"><i class="fas fa-database"></i> Borg Backup</button>')
print('                                     </form>')
print('                                 </div>')

# Process Tracker
print('                                 <div class="col-md-6">')
print('                                     <form class="form" id="modalForm3" onsubmit="return false;">')
print('                                         <button class="btn btn-block" type="submit"><i class="fas fa-bug"></i> Check Processes</button>')
print('                                     </form>')
print('                                 </div>')
print('                             </div> <!-- Row End -->')
print('                         </div> <!-- Card Body End -->')
cardfooter('')

print('                     </div> <!-- End System Tab -->')

# Cluster Tab
print('')
print('                     <!-- Cluster Tab -->')
print('                     <div class="tab-pane fade" id="v-pills-cluster" role="tabpanel" aria-labelledby="v-pills-cluster-tab">')

# Cluster Status
if os.path.isfile(cluster_config_file):
    cardheader('Cluster Status','fas fa-align-justify')
    print('                        <div class="card-body p-0">  <!-- Card Body Start -->')  # card-body
    print('                            <div class="row no-gutters row-1"> <!-- Row Start -->')

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
                print('                                <div class="col-md-9 alert"><i class="fas fa-home"></i> '+myhome+'_'+servername.split('.')[0]+'</div>')
                print('                                <div class="col-md-3 alert text-success">In Sync <i class="fa fa-check-circle"></i></div>')
            else:
                print('                                <div class="col-md-9 alert"><i class="fas fa-home"></i> '+myhome+'_'+servername.split('.')[0]+'</div>')
                print('                                <div class="col-md-3 alert text-danger">Out of Sync <i class="fa fa-times-circle"></i></div>')

        filesync_status = False
        for myprocess in psutil.process_iter():

            # Workaround for Python 2.6
            if platform.python_version().startswith('2.6'):
                mycmdline = myprocess.cmdline
            else:
                mycmdline = myprocess.cmdline()
            if '/usr/bin/unison' in mycmdline and 'phpsessions_'+servername in mycmdline:
                filesync_status = True
                break

        if filesync_status:
            print('                                <div class="col-md-9 alert"><i class="fab fa-php"></i> phpsessions_'+servername.split('.')[0]+'</div>')
            print('                                <div class="col-md-3 alert text-success">In Sync <i class="fa fa-check-circle"></i></div>')
        else:
            print('                                <div class="col-md-9 alert"><i class="fab fa-php"></i> phpsessions_'+servername.split('.')[0]+'</div>')
            print('                                <div class="col-md-3 alert text-danger">Out of Sync <i class="fa fa-times-circle"></i></div>')

    print('                            </div> <!-- Row End -->') #Row End
    print('                        </div> <!-- Card Body End -->') #Card Body End

    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body

    print('                            <form class="form mb-3" id="toastForm4" onsubmit="return false;">')
    print('                                <input hidden name="mode" value="restart">')
    print('                                <button type="submit" class="btn btn-outline-primary btn-block ">Soft Restart Unison Sync</button>')
    print('                            </form>')

    print('                            <form class="form mb-3" id="toastForm5" onsubmit="return false;">')
    print('                                <input hidden name="mode" value="reset">')
    print('                                <button type="submit" class="btn btn-outline-primary btn-block">Hard Reset Unison Sync</button>')
    print('                            </form>')

    print('                            <form class="form" id="toastForm26" onsubmit="return false;">')
    print('                                <input hidden name="mode" value="reset">')
    print('                                <button type="submit" class="btn btn-outline-primary btn-block">Reset Csync2 Sync</button>')
    print('                            </form>')
    print('                        </div> <!-- Card Body End -->') #Card Body End

    cardfooter('Only perform a hard reset if the unison archive is corrupt as the unison archive rebuild can be time consuming.')
else:
    cardheader('Cluster Unison Sync Status Disabled','fas fa-align-justify')
    cardfooter('The cluster Unison sync status is disabled so this system is not running with High Availability failover.')

print('                     </div> <!-- End Cluster Tab -->')

# Zone Tab
print('')
print('                     <!-- Zone Tab -->')
print('                     <div class="tab-pane fade" id="v-pills-zone" role="tabpanel" aria-labelledby="v-pills-zone-tab">')

# Sync GeoDNS zone
if os.path.isfile(cluster_config_file) and os.path.isfile(homedir_config_file):
    cardheader('Sync GDNSD Zone','fas fa-sync')
    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start

    print('                            <form class="form" id="toastForm7" onsubmit="return false;">')
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <label class="input-group-text">Zone</label>')
    print('                                    </div>')
    print('                                    <select name="user" class="custom-select">')
    user_list = os.listdir("/var/cpanel/users")
    for cpuser in sorted(user_list):
        if cpuser != 'nobody' and cpuser != 'system':
            print('                                        <option value="'+cpuser+'">'+cpuser+'</option>')
    print('                                    </select>')
    print('                                </div>')
    print('                                <button type="submit" class="btn btn-outline-primary btn-block ">Sync GeoDNS Zone</button>')
    print('                            </form>')
    print('                        </div> <!-- Card Body End -->') #Card Body End
    cardfooter('Choose a user to sync GDNSD Zones for.')
else:
    cardheader('GDNSD Zone Sync Disabled','fas fa-sync')
    cardfooter('The GDNSD zone sync is disabled as this system is running with cPanel DNS.')

print('                     </div> <!-- End Zone Tab -->')

# PHP Tab
print('')
print('                     <!-- PHP Tab -->')
print('                     <div class="tab-pane fade" id="v-pills-php" role="tabpanel" aria-labelledby="v-pills-php-tab">')

# Set Default PHP for AutoConfig
cardheader('Default PHP for Autoswitch','fab fa-php')
print('                        <div class="card-body p-0">  <!-- Card Body Start -->')  # card-body
print('                            <div class="row no-gutters row-1"> <!-- Row Start -->')

# Check if we have a Preferred PHP and allow selection.
if os.path.isfile(installation_path+"/conf/preferred_php.yaml"):
    preferred_php_yaml = open(installation_path+"/conf/preferred_php.yaml", 'r')
    preferred_php_yaml_parsed = yaml.safe_load(preferred_php_yaml)
    preferred_php_yaml.close()
    phpversion = preferred_php_yaml_parsed.get('PHP')
    myphpversion = phpversion.keys()[0]
else:
    myphpversion = "Unset"
print('                                <div class="col-md-6 alert"><i class="fab fa-php"></i> Default PHP</div>')
print('                                <div class="col-md-6 alert text-success">'+myphpversion+' <i class="fa fa-check-circle"></i></div>')
print('                            </div>')
print('                        </div> <!-- Card Body End -->')

backend_config_file = installation_path+"/conf/backends.yaml"
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()

if "PHP" in backend_data_yaml_parsed:
    print('                        <div class="card-body"> <!-- Card Body Start -->')
    print('                            <form class="form" id="toastForm6" onsubmit="return false;">')
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <label class="input-group-text">PHP</label>')
    print('                                    </div>')
    print('                                    <select name="phpversion" class="custom-select">')

    php_backends_dict = backend_data_yaml_parsed["PHP"]
    for versions_defined in list(php_backends_dict.keys()):
        if versions_defined == myphpversion:
            print('                                        <option selected value="'+myphpversion+'">'+myphpversion+'</option>')
        else:
            print('                                        <option value="'+versions_defined+'">'+versions_defined+'</option>')
    print('                                    </select>')
    print('                                </div>')
    print('                                <button type="submit" class="btn btn-outline-primary btn-block">Set Default PHP</button>')
    print('                            </form>')
    print('                        </div> <!-- Card Body End -->')
cardfooter('Automatic switch to Nginx will use versions set in MultiPHP or if MultiPHP is not used the phpversion above')

print('                     </div> <!-- End PHP Tab -->')

# DOS Tab
print('')
print('                     <!-- DOS Tab -->')
print('                     <div class="tab-pane fade" id="v-pills-dos" role="tabpanel" aria-labelledby="v-pills-dos-tab">')

# DDOS Protection
cardheader('DDOS Protection','fas fa-user-shield')
print('                        <div class="card-body p-0">  <!-- Card Body Start -->')  # card-body
print('                            <div class="row no-gutters row-2-col row-no-btm"> <!-- Row Start -->')
print('                                <div class="col-md-6 alert"><i class="fas fa-shield-alt"></i> Nginx</div>')
print('                                <div class="col-md-6">')
print('                                    <div class="row no-gutters">')

if os.path.isfile('/etc/nginx/conf.d/dos_mitigate_systemwide.enabled'):
    print('                                        <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
    print('                                        <div class="col-9">')
    print('                                            <form id="toastForm1" class="form" onsubmit="return false;">')
    print('                                                <button type="submit" class="alert btn btn-secondary">Disable</button>')
    print('                                                <input hidden name="ddos" value="disable">')
else:
    print('                                        <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
    print('                                        <div class="col-9">')
    print('                                            <form id="toastForm1" class="form" onsubmit="return false;">')
    print('                                                <button type="submit" class="alert btn btn-secondary">Enable</button>')
    print('                                                <input hidden name="ddos" value="enable">')

print('                                            </form>')
print('                                        </div>')
print('                                    </div>')
print('                                </div>')

try:
    with open(os.devnull, 'w') as FNULL:
        subprocess.call(['systemctl', '--version'], stdout=FNULL, stderr=subprocess.STDOUT)
except OSError:
    pass
else:
    with open(os.devnull, 'w') as FNULL:
        firehol_enabled = subprocess.call("systemctl is-active firehol.service", stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
    print('                                <div class="col-md-6 alert"><i class="fas fa-shield-alt"></i> SYNPROXY</div>')
    print('                                <div class="col-md-6">')
    print('                                    <div class="row no-gutters">')

    if firehol_enabled == 0:
        print('                                        <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
        print('                                        <div class="col-9">')
        print('                                            <form id="toastForm2" class="form" onsubmit="return false;">')
        print('                                                <button type="submit" class="alert btn btn-secondary">Disable</button>')
        print('                                               <input hidden name="ddos" value="disable">')
    else:
        print('                                        <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
        print('                                        <div class="col-9">')
        print('                                            <form id="toastForm2" class="form" onsubmit="return false;">')
        print('                                                <button type="submit" class="alert btn btn-secondary">Enable</button>')
        print('                                                <input hidden name="ddos" value="enable">')

    print('                                            </form>')
    print('                                        </div>')
    print('                                    </div>')
    print('                                </div>')

print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->') #Card Body End
cardfooter('Turn these settings on when you are under a DDOS Attack but remember to disable CSF or any other firewall before turning on SYNPROXY (FireHol).')

print('                     </div> <!-- End DOS Tab -->')

# PHP_FPM Tab
print('')
print('                     <!-- PHP_FPM Tab -->')
print('                     <div class="tab-pane fade" id="v-pills-php_fpm" role="tabpanel" aria-labelledby="v-pills-php_fpm-tab">')

# PHP-FPM Pool Editor
phpfpmpool_hint = " Secure and non secure PHP-FPM Pools attached to cPanel users for use with Native NGINX. "
cardheader('PHP-FPM Pool Editor','fas fa-sitemap')
print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <form class="form" action="phpfpm_pool_editor.cgi" method="get">')
print('                                <div class="input-group">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text">')
print('                                            '+return_prepend("cPanel User", phpfpmpool_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <select name="poolfile" class="custom-select">')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    conf_list = os.listdir("/opt/nDeploy/secure-php-fpm.d")
    for filename in sorted(conf_list):
        user, extension = filename.split('.')
        if user != 'nobody':
            print('                                        <option value="/opt/nDeploy/secure-php-fpm.d/'+filename+'">'+user+'</option>')
else:
    conf_list = os.listdir("/opt/nDeploy/php-fpm.d")
    for filename in sorted(conf_list):
        user, extension = filename.split('.')
        if user != 'nobody':
            print('                                        <option value="/opt/nDeploy/php-fpm.d/'+filename+'">'+user+'</option>')
print('                                    </select>')
print('                                </div>')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    print('                                <input hidden name="section" value="1">')
else:
    print('                                <input hidden name="section" value="0">')
print('                                <button class="btn btn-outline-primary btn-block" type="submit">Edit Settings</button>')
print('                            </form>')
print('                        </div> <!-- Card Body End -->') #Card Body End
cardfooter('Settings such as: pm.max_requests, pm.max_spare_servers, session.save_path, pm.max_children')

print('                     </div> <!-- End PHP_FPM Tab -->')

# Map Tab
print('')
print('                     <!-- Map Tab -->')
print('                     <div class="tab-pane fade" id="v-pills-map" role="tabpanel" aria-labelledby="v-pills-map-tab">')

# Map cPanel Package to NGINX
cardheader('Map cPanel Package to NGINX','fas fa-box-open')
print('                        <div class="card-body p-0"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row no-gutters row-1"> <!-- Row Start -->') #Row Start
print('                                <div class="col-md-6 alert"><i class="fas fa-box"></i> NGINX -> Package</div>')
print('                                <div class="col-md-6">')
print('                                    <div class="row no-gutters">')

if os.path.isfile(installation_path+'/conf/lock_domaindata_to_package'):
    print('                                        <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
    print('                                        <div class="col-9">')
    print('                                            <form class="form" method="post" id="toastForm16" onsubmit="return false;">')
    print('                                                <button type="submit" class="alert btn btn-secondary">Disable</button>')
    print('                                                <input hidden name="package_lock" value="disabled">')
    print('                                            </form>')
    print('                                        </div>')
    print('                                    </div>')
else:
    print('                                        <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
    print('                                        <div class="col-9">')
    print('                                            <form class="form" method="post" id="toastForm16" onsubmit="return false;">')
    print('                                                <button type="submit" class="alert btn btn-secondary">Enable</button>')
    print('                                                <input hidden name="package_lock" value="enabled">')
    print('                                            </form>')
    print('                                        </div>')
    print('                                    </div>')

print('                                </div>')
print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->') #Card Body End
print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start

cpanpackage_hint = " Map a NGINX configuration to an installed cPanel package. "

# Workaround for python 2.6
if platform.python_version().startswith('2.6'):
    listpkgs = subprocess.Popen('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', stdout=subprocess.PIPE, shell=True).communicate()[0]
else:
    listpkgs = subprocess.check_output('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', shell=True)
mypkgs = json.loads(listpkgs)

print('                            <form class="form" action="pkg_profile.cgi" method="get">')
print('                                <div class="input-group">')
print('                                    <div class="input-group-prepend">')
print('                                        <span class="input-group-text">')
print('                                            '+return_prepend("cPanel Package", cpanpackage_hint))
print('                                        </span>')
print('                                    </div>')
print('                                    <select name="cpanelpkg" class="custom-select">')

for thepkg in sorted(mypkgs.get('package')):
    pkgname = thepkg.get('name').encode('utf-8').replace(' ', '_')
    print('                                        <option value="'+pkgname+'">'+pkgname+'</option>')

print('                                    </select>')
print('                                </div>')
print('                                <button class="btn btn-outline-primary btn-block" type="submit">Edit Pkg</button>')
print('                            </form>')
print('                        </div> <!-- Card Body End -->') #Card Body End
cardfooter('This option will automatically assign NGINX Config/Settings to a cPanel Package when enabled. This will also reset any NGINX Config/Settings the user has configured if the cPanel Package undergoes an Upgrade/Downgrade process.'
)

print('                     </div> <!-- End Map Tab -->')

# Limit Tab
print('')
print('                     <!-- Limit Tab -->')
print('                     <div class="tab-pane fade" id="v-pills-limit" role="tabpanel" aria-labelledby="v-pills-limit-tab">')

# System Resource Limit
cardheader('System Resource Limit','fas fa-compress')
print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start

with open('/etc/redhat-release', 'r') as releasefile:
    osrelease = releasefile.read().split(' ')[0]
if not osrelease == 'CloudLinux':
    if os.path.isfile('/usr/bin/systemctl'):

        # Next sub-section start here
        if os.path.isfile(installation_path+"/conf/secure-php-enabled"):  # if per user php-fpm master process is set
            userlist = os.listdir("/var/cpanel/users")
            print('                            <form class="form" action="resource_limit.cgi" method="get">')
            print('                                <div class="input-group">')
            print('                                    <div class="input-group-prepend">')
            print('                                        <label class="input-group-text">User</label>')
            print('                                    </div>')
            print('                                    <select name="unit" class="custom-select">')

            for cpuser in sorted(userlist):
                if cpuser != 'nobody' and cpuser != 'system':
                    print('                                        <option value="'+cpuser+'">'+cpuser+'</option>')

            print('                                    </select>')
            print('                                    <input hidden name="mode" value="user">')
            print('                                </div>')
            print('                                <button class="btn btn-outline-primary btn-block" type="submit">Set Limit</button>')
            print('                            </form>')

            print('                            <form class="form mt-4" action="resource_limit.cgi" method="get">')
            print('                                <div class="input-group">')
            print('                                    <div class="input-group-prepend">')
            print('                                        <label class="input-group-text">Service</label>')
            print('                                    </div>')
            print('                                    <select name="unit" class="custom-select">')

            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm", "ea-php73-php-fpm":
                print('                                        <option value="'+service+'">'+service+'</option>')

            print('                                    </select>')
            print('                                    <input hidden name="mode" value="service">')
            print('                                </div>')
            print('                                <button class="btn btn-outline-primary btn-block" type="submit">Set Limit</button>')
            print('                            </form>')
        else:
            print('                            <form class="form" action="resource_limit.cgi" method="get">')
            print('                                <div class="input-group">')
            print('                                    <div class="input-group-prepend">')
            print('                                        <label class="input-group-text">Resource</label>')
            print('                                    </div>')
            print('                                    <select name="unit" class="custom-select">')

            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm", "ea-php73-php-fpm":
                print('                                        <option value="'+service+'">'+service+'</option>')

            print('                                    </select>')
            print('                                    <input hidden name="mode" value="service">')
            print('                                </div>')
            print('                                <button class="btn btn-outline-primary btn-block" type="submit">Set Limit</button>')
            print('                            </form>')
print('                        </div> <!-- Card Body End -->') #Card Body End
cardfooter('BlockIOWeight range is 10-1000, CPUShares range is 0-1024, MemoryLimit range is calculated using available memory')

print('                     </div> <!-- End Limit Tab -->')




print('                 </div>')
print('             </div>')











print_footer()

print('        </div> <!-- Main Container End -->')
print('')

print_modals()
print_loader()

print('    <!-- Body End -->')
print('    </body>')
print('</html>')
