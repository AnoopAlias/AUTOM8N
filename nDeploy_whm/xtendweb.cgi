#!/usr/bin/env python

import os
import cgitb
import subprocess
import yaml
import psutil
import platform
import socket
from requests import get
try:
    import simplejson as json
except ImportError:
    import json
from commoninclude import bcrumb, return_prepend, print_header, print_footer, cardheader, cardfooter, print_input_fn, print_select_fn


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"
master_config_file = installation_path+"/conf/ndeploy_master.yaml"
autom8n_version_info_file = installation_path+"/conf/version.yaml"
nginx_version_info_file = "/etc/nginx/version.yaml"
branding_file = installation_path+"/conf/branding.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"
ansible_inventory_file = "/opt/nDeploy/conf/nDeploy-cluster/hosts"
php_secure_mode_file = installation_path+"/conf/secure-php-enabled"

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
    if '/usr/sbin/nginx' in mycmdline:
        nginx_status = True
    if '/opt/nDeploy/scripts/watcher.py' in mycmdline:
        watcher_status = True


# Read in PHP Backend Status for Dash
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()

if not os.path.isfile(php_secure_mode_file):
    if "PHP" in backend_data_yaml_parsed:
        installed_php_count = len(backend_data_yaml_parsed["PHP"].keys())
    else:
        installed_php_count = 0

    running_process_count = 0
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            myexe = myprocess.cmdline
        else:
            myexe = myprocess.cmdline()
        if 'php-fpm: master process (/opt/nDeploy/conf/php-fpm.conf)' in myexe:
            running_process_count = running_process_count + 1


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

print('            <h1 class="sr-only">AUTOM8N Configuration Center</h1>')

print('            <!-- Dash Widgets Start -->')
print('            <div id="dashboard" class="row flex-row">')
print('')

# Nginx Status
print('                <div id="nginx_status_widget" class="col-sm-6 col-xl-3"> <!-- Dash Item Start -->')
cardheader('')
print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
print('                        <h2 class="mb-0">Nginx Status</h2>')
print('                        <ul class="list-unstyled mb-0">')
print('                            <li><small>'+nginx_version+'</small></li>')
if nginx_status:
    print('                        <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                        <li class="mt-2 text-danger">Stopped <i class="fas fa-power-off ml-1"></i></li>')
print('                        </ul>')
print('                    </div> <!-- Card Body End -->')
print('                    <form class="form" id="nginx_status" onsubmit="return false;">')
print('                        <label hidden for="nginx_reload">Nginx Reload</label>')
print('                        <input hidden name="action" id="nginx_reload" value="nginxreload">')
print('                        <button id="nginx-status-btn" class="btn btn-secondary btn-block mb-0">Reload</button>')
print('                    </form>')
cardfooter('')
print('                </div> <!-- Dash Item End -->')

# Autom8n Version Status
print('                <div id="watcher_status_widget" class="col-sm-6 col-xl-3"> <!-- Dash Item Start -->')
cardheader('')
print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
print('                        <h2 class="mb-0">Watcher Status</h2>')
print('                        <ul class="list-unstyled mb-0">')
print('                            <li><small>'+brand+' '+autom8n_version.replace("Autom8n ", '')+'</small></li>')
if watcher_status:
    print('                        <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                        <li class="mt-2 text-danger">Stopped <i class="fas fa-power-off ml-1"></i></li>')
print('                        </ul>')
print('                    </div> <!-- Card Body End -->')
print('                    <form class="form" id="watcher_status" onsubmit="return false;">')
print('                        <label hidden for="watcher_restart">Watcher Restart</label>')
print('                        <input hidden name="action" id="watcher_restart" value="watcherrestart">')
print('                        <button id="watcher-status-btn" class="btn btn-secondary btn-block mb-0">Restart</button>')
print('                    </form>')
cardfooter('')
print('                </div> <!-- Dash Item End -->')

# Cache/Redis Status
print('                <div id="clear_caches_widget" class="col-sm-6 col-xl-3"> <!-- Dash Item Start -->')
cardheader('')
print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
print('                        <h2 class="mb-0">Clear Caches</h2>')
print('                        <ul class="list-unstyled mb-0">')
print('                            <li><small>Redis</small></li>')
print('                            <li class="mt-2"><i class="fas fa-memory ml-1"></i></li>')
print('                        </ul>')
print('                    </div> <!-- Card Body End -->')
print('                    <form class="form" id="clear_caches" onsubmit="return false;">')
print('                        <label hidden for="redis_flush">Redis Flush</label>')
print('                        <input hidden name="action" id="redis_flush" value="redisflush">')
print('                        <button id="clear-caches-btn" class="btn btn-secondary btn-block mb-0">Flush All</button>')
print('                    </form>')
cardfooter('')
print('                </div> <!-- Dash Item End -->')

# Restart Backends
print('                <div id="restart_backends_widget" class="col-sm-6 col-xl-3"> <!-- Dash Item Start -->')
cardheader('')
print('                    <div class="card-body text-center"> <!-- Card Body Start -->')
print('                        <h2 class="mb-0">PHP Backends</h2>')
print('                        <ul class="list-unstyled mb-0">')

# Add real status to PHP Backend widget
livePHPStatus = get('http://localhost/pingphpfpm')
if livePHPStatus.status_code == 502:
    print('                            <li><small>PHP-FPM Status: <span class="text-danger">'+str(livePHPStatus.status_code)+'</span></small></li>')
elif livePHPStatus.status_code == 200:
    print('                            <li><small>PHP-FPM Status: <span class="text-success">'+str(livePHPStatus.status_code)+'</span></small></li>')
else:
    print('                            <li><small>PHP-FPM Status: <span class="text-info">'+str(livePHPStatus.status_code)+'</span></small></li>')

if not os.path.isfile(php_secure_mode_file):
    if running_process_count == installed_php_count:
        php_status = True
    else:
        php_status = False

    if php_status:
        print('                        <li class="mt-2 text-success">Single Master <i class="fas fa-power-off ml-1"></i></li>')
    else:
        print('                        <li class="mt-2 text-warning">Issue Detected <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                        <li class="mt-2 text-success">Multi-Master <i class="fas fa-power-off ml-1"></i></li>')

print('                        </ul>')
print('                    </div> <!-- Card Body End -->')
print('                    <form class="form" id="restart_backends" onsubmit="return false;">')
print('                        <label hidden for="restart_php_backends">Restart PHP Backends</label>')
print('                        <input hidden name="action" id="restart_php_backends" value="restart_backends">')
print('                        <button id="restart-backends-btn" class="btn btn-secondary btn-block mb-0">Restart</button>')
print('                    </form>')
cardfooter('')
print('                </div> <!-- Dash Item End -->')
print('')
print('            </div> <!-- Dash Widgets End -->')
print('')
print('            <!-- WHM Tabs Row -->')
print('            <div class="row justify-content-lg-center flex-nowrap">')
print('')
print('                <!-- Secondary Navigation -->')
print('                <div class="pl-3 col-md-3 nav flex-column nav-pills d-none d-lg-block d-xl-block d-xs-none d-sm-none" id="v-pills-tab" role="tablist" aria-orientation="vertical">')
print('                    <a class="nav-link active" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab" aria-selected="true">System Health & Backup</a>')
print('                    <a class="nav-link" id="v-pills-cluster-tab" data-toggle="pill" href="#v-pills-cluster" role="tab" aria-controls="v-pills-cluster" aria-selected="false">Cluster Status</a>')
print('                    <a class="nav-link" id="v-pills-zone-tab" data-toggle="pill" href="#v-pills-zone" role="tab" aria-controls="v-pills-zone" aria-selected="false">Cluster Sync</a>')
print('                    <a class="nav-link" id="v-pills-php-tab" data-toggle="pill" href="#v-pills-php" role="tab" aria-controls="v-pills-php" aria-selected="false">Default PHP for Autoswitch</a>')
print('                    <a class="nav-link" id="v-pills-dos-tab" data-toggle="pill" href="#v-pills-dos" role="tab" aria-controls="v-pills-dos" aria-selected="false">DDOS Protection</a>')
print('                    <a class="nav-link" id="v-pills-php_fpm-tab" data-toggle="pill" href="#v-pills-php_fpm" role="tab" aria-controls="v-pills-php_fpm" aria-selected="false">PHP-FPM Pool Editor</a>')
print('                    <a class="nav-link" id="v-pills-map-tab" data-toggle="pill" href="#v-pills-map" role="tab" aria-controls="v-pills-map" aria-selected="false">Package Editor</a>')
print('                    <a class="nav-link" id="v-pills-limit-tab" data-toggle="pill" href="#v-pills-limit" role="tab" aria-controls="v-pills-limit" aria-selected="false">System Resource Limit</a>')
print('                </div>')
print('')
print('                <div class="tab-content col-md-12 col-lg-9" id="v-pills-tabContent">')
print('')
print('                    <!-- Secondary Mobile Navigation -->')
print('                    <div class="d-lg-none d-xl-none dropdown nav">')
print('                        <button class="btn btn-primary btn-block dropdown-toggle mb-3" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">')
print('                            Config Menu')
print('                        </button>')
print('                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">')
print('                            <a class="dropdown-item" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab" aria-selected="true">System Health & Backup</a>')
print('                            <a class="dropdown-item" id="v-pills-cluster-tab" data-toggle="pill" href="#v-pills-cluster" role="tab" aria-controls="v-pills-cluster" aria-selected="false">Cluster Status</a>')
print('                            <a class="dropdown-item" id="v-pills-zone-tab" data-toggle="pill" href="#v-pills-zone" role="tab" aria-controls="v-pills-zone" aria-selected="false">Sync GDNSD Zone</a>')
print('                            <a class="dropdown-item" id="v-pills-php-tab" data-toggle="pill" href="#v-pills-php" role="tab" aria-controls="v-pills-php" aria-selected="false">Default PHP for Autoswitch</a>')
print('                            <a class="dropdown-item" id="v-pills-dos-tab" data-toggle="pill" href="#v-pills-dos" role="tab" aria-controls="v-pills-dos" aria-selected="false">DDOS Protection</a>')
print('                            <a class="dropdown-item" id="v-pills-php_fpm-tab" data-toggle="pill" href="#v-pills-php_fpm" role="tab" aria-controls="v-pills-php_fpm" aria-selected="false">PHP-FPM Pool Editor</a>')
print('                            <a class="dropdown-item" id="v-pills-map-tab" data-toggle="pill" href="#v-pills-map" role="tab" aria-controls="v-pills-map" aria-selected="false">Package Editor</a>')
print('                            <a class="dropdown-item" id="v-pills-limit-tab" data-toggle="pill" href="#v-pills-limit" role="tab" aria-controls="v-pills-limit" aria-selected="false">System Resource Limit</a>')
print('                        </div>')
print('                    </div>')

# System Tab
print('')
print('                    <!-- System Tab -->')
print('                    <div class="tab-pane fade show active" id="v-pills-system" role="tabpanel" aria-labelledby="v-pills-system-tab">')

# System Health & Backup
cardheader('System Health & Backup', 'fas fa-cogs')
print('                        <div class="card-body p-0">  <!-- Card Body Start -->')
print('                            <div class="row no-gutters row-2-col row-no-btm-bdr"> <!-- Row Start -->')

# Netdata
myhostname = socket.gethostname()
print('                                <div class="col-md-6">')
print('                                    <a class="btn btn-block btn-icon" href="https://'+myhostname+'/netdata/" target="_blank"><i class="fas fa-heartbeat"></i> Netdata <i class="fas fa-external-link-alt"></i></a>')
print('                                </div>')

# Glances
print('                                <div class="col-md-6">')
print('                                    <a class="btn btn-block btn-icon" href="https://'+myhostname+'/glances/" target="_blank"><i class="fas fa-eye"></i> Glances <i class="fas fa-external-link-alt"></i></a>')
print('                                </div>')

# Borg Backup
print('                                <div class="col-md-6">')
print('                                    <form class="form" method="get" action="setup_borg_backup.cgi">')
print('                                        <button class="btn btn-block btn-icon" type="submit"><i class="fas fa-database"></i> Borg Backup</button>')
print('                                    </form>')
print('                                </div>')

# Process Tracker
print('                                <div class="col-md-6">')
print('                                    <form class="form" id="check_process" onsubmit="return false;">')
print('                                        <button id="check_process_btn" class="btn btn-block btn-icon" type="submit"><i class="fas fa-bug"></i> Check Processes</button>')
print('                                    </form>')
print('                                </div>')
print('                            </div> <!-- Row End -->')
print('                        </div> <!-- Card Body End -->')
cardfooter('')

print('             </div> <!-- End System Tab -->')

# Cluster Tab
print('')
print('             <!-- Cluster Tab -->')
print('             <div class="tab-pane fade" id="v-pills-cluster" role="tabpanel" aria-labelledby="v-pills-cluster-tab">')

# Cluster Status
if os.path.isfile(cluster_config_file):
    cardheader('Cluster Status', 'fas fa-align-justify')
    print('             <div class="card-body p-0">  <!-- Card Body Start -->')
    print('                 <div id="cluster-status-info" class="row no-gutters row-1"> <!-- Row Start -->')

    with open(cluster_config_file, 'r') as cluster_data_yaml:
        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    with open(master_config_file, 'r') as master_data_yaml:
        master_data_yaml_parsed = yaml.safe_load(master_data_yaml)
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
                print('         <div class="col-6 col-md-9 alert"><i class="fas fa-home"></i> '+myhome+'_'+servername.split('.')[0]+'</div>')
                print('         <div class="col-6 col-md-3 alert text-success">In Sync <i class="fa fa-check-circle"></i></div>')
            else:
                print('         <div class="col-6 col-md-9 alert"><i class="fas fa-home"></i> '+myhome+'_'+servername.split('.')[0]+'</div>')
                print('         <div class="col-6 col-md-3 alert text-danger">Out of Sync <i class="fa fa-times-circle"></i></div>')

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
            print('             <div class="col-6 col-md-9 alert"><i class="fab fa-php"></i> phpsessions_'+servername.split('.')[0]+'</div>')
            print('             <div class="col-6 col-md-3 alert text-success">In Sync <i class="fa fa-check-circle"></i></div>')
        else:
            print('             <div class="col-6 col-md-9 alert"><i class="fab fa-php"></i> phpsessions_'+servername.split('.')[0]+'</div>')
            print('             <div class="col-6 col-md-3 alert text-danger">Out of Sync <i class="fa fa-times-circle"></i></div>')

    print('                 </div> <!-- Row End -->')
    print('             </div> <!-- Card Body End -->')

    print('             <div class="card-body"> <!-- Card Body Start -->')

    print('                 <form class="form" id="cluster_soft_restart" onsubmit="return false;">')
    print('                     <label hidden for="cluster_soft_restart2">Cluster Soft Restart</label>')
    print('                     <input hidden name="mode" id="cluster_soft_restart2" value="restart">')
    print('                 </form>')

    print('                 <form class="form" id="cluster_hard_reset" onsubmit="return false;">')
    print('                     <label hidden for="cluster_hard_reset2">Cluster Hard Reset</label>')
    print('                     <input hidden name="mode" id="cluster_hard_reset2" value="reset">')
    print('                 </form>')

    print('                 <form class="form" id="cluster_csync2_reset" onsubmit="return false;">')
    print('                     <label hidden for="cluster_csync2_reset2">Cluster Csync2 Reset</label>')
    print('                     <input hidden name="mode" id="cluster_csync2_reset2" value="reset">')
    print('                 </form>')

    print('                 <div id="cluster-reset-btns" class="btn-group btn-block">')
    print('                     <button id="cluster-soft-restart-btn" type="submit" class="btn btn-outline-primary" form="cluster_soft_restart">Soft Restart</button>')
    print('                     <button id="cluster-hard-reset-btn" type="submit" class="btn btn-outline-primary" form="cluster_hard_reset">Hard Reset</button>')
    print('                     <button id="cluster-csync2-reset-btn" type="submit" class="btn btn-outline-primary" form="cluster_csync2_reset">Reset Csync2</button>')
    print('                 </div>')

    # This is case where conf/ndeploy_cluster.yaml and conf/nDeploy-cluster/hosts both exists
    # This means the user has setup the ansible inventory and has successfully setup the cluster

    # If the inventory file exists
    if os.path.isfile(ansible_inventory_file):

        # Parse the inventory and display its contents
        with open(ansible_inventory_file, 'r') as my_inventory:
            ansible_inventory_file_parsed = yaml.safe_load(my_inventory)
        master_hostname = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'].keys()[0]
        master_server_id = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['server_id']
        master_ssh_port = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['ansible_port']
        master_main_ip = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['mainip']
        master_db_ip = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['dbip']
        master_dbmode = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['dbmode']
        master_lat = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['latitude']
        master_lon = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['longitude']
        master_repo = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['repo']
        master_dns = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['dns']

        dbslave_hostname = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'].keys()[0]
        dbslave_server_id = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['server_id']
        dbslave_ssh_port = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['ansible_port']
        dbslave_main_ip = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['mainip']
        dbslave_db_ip = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['dbip']
        dbslave_dbmode = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['dbmode']
        dbslave_lat = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['latitude']
        dbslave_lon = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['longitude']
        dbslave_repo = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['repo']
        dbslave_dns = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['dns']

        # Navigation tabs start here
        print('             <ul class="nav nav-tabs mt-4 mb-4" id="clusterTabs" role="tablist">')
        print('                 <li class="nav-item"><a class="nav-link active" id="master-tab" data-toggle="tab" href="#master-content" role="tab" aria-controls="master-content" aria-selected="true">Master</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="slave-tab" data-toggle="tab" href="#slave-content" role="tab" aria-controls="slave-content" aria-selected="false">Slaves</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="add-tab" data-toggle="tab" href="#add-content" role="tab" aria-controls="add-content" aria-selected="false">Add Slave</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="ip-add-tab" data-toggle="tab" href="#ip-add-content" role="tab" aria-controls="ip-add-content" aria-selected="false">Add IP</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="ip-tab" data-toggle="tab" href="#ip-content" role="tab" aria-controls="ip-content" aria-selected="false">IP Resource</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="home-tab" data-toggle="tab" href="#home-content" role="tab" aria-controls="home-content" aria-selected="false">Home Directory</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="playbook-tab" data-toggle="tab" href="#playbook-content" role="tab" aria-controls="playbook-content" aria-selected="false">Deploy</a></li>')
        print('             </ul>')

        print('                     <div class="tab-content" id="clusterTabsContent">')

        # Tab Start / Tab1 ###########################
        # Master data
        print('                         <div class="tab-pane fade show active" id="master-content" role="tabpanel" aria-labelledby="master-tab">')
        print('                            <form class="form needs-validation" method="post" id="save_cluster_settings_master" onsubmit="return false;" novalidate>')

        print_input_fn("Master Node FQDN", " Enter the master server's fully qualified domain name. ", master_hostname, "master_hostname")
        print_input_fn("Master Main IP", " Enter the master server's main IP address. ", master_main_ip, "master_main_ip")
        print_input_fn("Master DB IP", " Enter the master server's database IP address. ", master_db_ip, "master_db_ip")
        print_input_fn("Master SSH Port", " Enter the master server's SSH port. ", master_ssh_port, "master_ssh_port")
        print_input_fn("Master Server ID", " Enter the master server's ID (Usually 1). ", master_server_id, "master_server_id")
        print_input_fn("Master Latitude", " Enter the master server's latitude coordinate. ", master_lat, "master_lat")
        print_input_fn("Master Longitude", " Enter the master server's longitude coordinate. ", master_lon, "master_lon")

        print_select_fn("RPM Repo", " Select desired RPM Repo for the application's cluster build process. ", master_repo, "master_repo", "ndeploy", "ndeploy-edge")
        print_select_fn("DB Mode", " Select desired MaxScale database mode for this node. ", master_dbmode, "master_dbmode", "readconnroute", "rwsplit")
        print_select_fn("DNS Type", " Select desired MaxScale Mode for this node. ", master_dns, "master_dns", "bind", "geodns")

        print('                                <label hidden for="cluster_edit_master">Cluster Edit Master</label>')
        print('                                <input hidden name="action" id="cluster_edit_master" value="editmaster">')

        print('                                <button id="save-cluster-settings-master-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Save Master Settings</button>')
        print('                            </form>')
        print('                        </div>')

        # Tab Start / Tab2 ###########################
        # DBSlave data
        print('                         <div class="tab-pane fade show" id="slave-content" role="tabpanel" aria-labelledby="slave-tab">')
        print('                            <form class="form needs-validation" method="post" id="save_cluster_settings_slave" onsubmit="return false;" novalidate>')

        print_input_fn("DBSlave Node FQDN", " Enter the slave server's fully qualified domain name. ", dbslave_hostname, "dbslave_hostname")
        print_input_fn("DBSlave Main IP", " Enter the slave server's main IP address. ", dbslave_main_ip, "dbslave_main_ip")
        print_input_fn("DBSlave DB IP", " Enter the slave server's database IP address. ", dbslave_db_ip, "dbslave_db_ip")
        print_input_fn("DBSlave SSH Port", " Enter the slave server's SSH port. ", dbslave_ssh_port, "dbslave_ssh_port")
        print_input_fn("DBSlave Server ID", " Enter the slave server's ID (Usually 2). ", dbslave_server_id, "dbslave_server_id")
        print_input_fn("DBSlave Latitude", " Enter the slave server's latitude coordinate. ", dbslave_lat, "dbslave_lat")
        print_input_fn("DBSlave Longitude", " Enter the slave server's longitude coordinate. ", dbslave_lon, "dbslave_lon")

        print_select_fn("RPM Repo", " Select desired RPM Repo for the application's cluster build process. ", dbslave_repo, "dbslave_repo", "ndeploy", "ndeploy-edge")
        print_select_fn("DB Mode", " Select desired MaxScale database mode for this node. ", dbslave_dbmode, "dbslave_dbmode", "readconnroute", "rwsplit")
        print_select_fn("DNS Type", " Select desired MaxScale Mode for this node. ", dbslave_dns, "dbslave_dns", "bind", "geodns")

        print('                                <label hidden for="cluster_edit_db_slave">Cluster Edit DB Slave</label>')
        print('                                <input hidden name="action" id="cluster_edit_db_slave" value="editdbslave">')

        print('                                <button id="save-cluster-settings-slave-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Save DBSlave Settings</button>')
        print('                            </form>')

        # Additional slaves
        for myslave in ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'].keys():
            if myslave != dbslave_hostname:

                # Lets get all the details of this slave server and present to the user for editing
                slave_hostname = myslave
                slave_server_id = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['server_id']
                slave_ssh_port = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['ansible_port']
                slave_main_ip = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['mainip']
                slave_db_ip = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['dbip']
                slave_dbmode = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['dbmode']
                slave_lat = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['latitude']
                slave_lon = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['longitude']
                slave_repo = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['repo']
                slave_dns = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['dns']

                # Slave data
                print('     <div class="accordion mt-4" id="accordionSlaves-'+str(slave_server_id)+'">')
                print('         <div class="card mb-0">')
                print('             <div class="card-header" id="heading'+str(slave_server_id)+'">')
                print('                 <h2 class="mb-0">')
                print('                     <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse'+str(slave_server_id)+'" aria-expanded="false" aria-controls="collapse'+str(slave_server_id)+'">')
                print('                         Slave #'+str(slave_server_id)+'')
                print('                     </button>')
                print('                 </h2>')
                print('             </div>')

                print('             <div id="collapse'+str(slave_server_id)+'" class="collapse" aria-labelledby="heading'+str(slave_server_id)+'" data-parent="#accordionSlaves-'+str(slave_server_id)+'">')
                print('                 <div class="card-body">')
                print('                     <form class="form needs-validation" method="post" id="save_cluster_settings_slave_add-'+str(slave_server_id)+'" onsubmit="return false;" novalidate>')

                print_input_fn("Slave Node FQDN", " Enter the slave server's fully qualified domain name. ", slave_hostname, "slave_hostname")
                print_input_fn("Slave Main IP", " Enter the slave server's main IP address. ", slave_main_ip, "slave_main_ip")
                print_input_fn("Slave DB IP", " Enter the slave server's database IP address. ", slave_db_ip, "slave_db_ip")
                print_input_fn("Slave SSH Port", " Enter the slave server's SSH port. ", slave_ssh_port, "slave_ssh_port")
                print_input_fn("Slave Server ID", " Enter the slave server's ID (Usually 1). ", slave_server_id, "slave_server_id")
                print_input_fn("Slave Latitude", " Enter the slave server's latitude coordinate. ", slave_lat, "slave_lat")
                print_input_fn("Slave Longitude", " Enter the slave server's longitude coordinate. ", slave_lon, "slave_lon")

                print_select_fn("RPM Repo", " Select desired RPM Repo for the application's cluster build process. ", slave_repo, "slave_repo", "ndeploy", "ndeploy-edge")
                print_select_fn("DB Mode", " Select desired MaxScale database mode for this node. ", slave_dbmode, "slave_dbmode", "readconnroute", "rwsplit")
                print_select_fn("DNS Type", " Select desired MaxScale Mode for this node. ", slave_dns, "slave_dns", "bind", "geodns")



                print('                         <label hidden for="cluster_edit_slave">Cluster Edit Slave</label>')
                print('                         <input hidden name="action" id="cluster_edit_slave" value="editslave">')

                print('                     </form>')

                # Delete the Additional Slave
                print('                     <form class="form delete_cluster_settings_slave" method="post" id="delete_cluster_settings_slave-'+str(slave_server_id)+'" onsubmit="return false;">')
                print('                         <label hidden for="cluster_delete_slave">Cluster Delete Slave</label>')
                print('                         <input hidden name="action" id="cluster_delete_slave" value="deleteslave">')
                print('                         <label hidden for="cluster_slave_hostname2">Cluster Save Hostname</label>')
                print('                         <input hidden name="slave_hostname" id="cluster_slave_hostname2" value="'+myslave+'">')
                print('                     </form>')
                print('                     <div class="btn-group btn-block mt-4">')
                print('                         <button id="save-cluster-settings-slave-add-btn-'+str(slave_server_id)+'" class="btn btn-outline-primary btn-block" type="submit" form="save_cluster_settings_slave_add-'+str(slave_server_id)+'">Save Slave Settings</button>')
                print('                         <button id="delete-cluster-settings-slave-btn-'+str(slave_server_id)+'" class="btn btn-outline-danger btn-block" type="submit" form="delete_cluster_settings_slave-'+str(slave_server_id)+'">Delete Slave</button>')
                print('                     </div>')

                print('                 </div>')
                print('             </div>')
                print('         </div>')
                print('     </div>')
        print('</div>')

        # Tab Start / Tab3 ###########################
        # Add additional Slave
        print('                         <div class="tab-pane fade" id="add-content" role="tabpanel" aria-labelledby="add-tab">')
        print('                            <form class="form needs-validation" method="post" id="save_cluster_settings_addi_slave_add" onsubmit="return false;" novalidate>')

        # Slave data
        print_input_fn("Slave Node FQDN", " Enter the slave server's fully qualified domain name. ", "", "slave_hostname")
        print_input_fn("Slave Main IP", " Enter the slave server's main IP address. ", "", "slave_main_ip")
        print_input_fn("Slave DB IP", " Enter the slave server's database IP address. ", "", "slave_db_ip")
        print_input_fn("Slave SSH Port", " Enter the slave server's SSH port. ", "", "slave_ssh_port")

        print('                                <label hidden for="cluster_add_additional_slave">Cluster Add Additional Slave</label>')
        print('                                <input hidden name="action" id="cluster_add_additional_slave" value="addadditionalslave">')

        print('                                <button id="save-cluster-settings-addi-slave-add-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Add New Slave</button>')
        print('                            </form>')
        print('                         </div>')

        # Tab Start / Tab4 ###########################
        # Display, Edit, Delete IPMapping
        print('                         <div class="tab-pane fade" id="ip-content" role="tabpanel" aria-labelledby="ip-tab">')
        master_ip_list = master_data_yaml_parsed[myhostname]['dnsmap'].keys()
        for myip in master_ip_list:
            master_ip_resource = master_data_yaml_parsed[myhostname]['dnsmap'].get(myip)

            # Provide public IP for Nat environment
            if os.path.isfile('/var/cpanel/cpnat'):
                with open('/var/cpanel/cpnat') as f:
                    content = f.readlines()
                content = [x.strip() for x in content]
                if content:
                    for line in content:
                        internalip, externalip = line.split()
                        if internalip == myip:
                            master_ip_resource_actual = externalip
                            break
                        else:
                            master_ip_resource_actual = myip
                else:
                    master_ip_resource_actual = myip
            else:
                master_ip_resource_actual = myip

            # Get corresponding slave IP for this master IP
            mykeypos = 1
            for theslave in cluster_data_yaml_parsed.keys():
                slave_mapped_dns_ip = cluster_data_yaml_parsed[theslave]['dnsmap'].get(myip, "NULL")
                slave_mapped_web_ip = cluster_data_yaml_parsed[theslave]['ipmap'].get(myip, "NULL")

                # Display form for IP address mapping
                print('     <div class="accordion" id="accordionIps-'+master_ip_resource+'-'+str(mykeypos)+'">')
                print('         <div class="card mb-0 text-white dg-dark">')
                print('             <div class="card-header" id="heading'+'-'+master_ip_resource+'-'+str(mykeypos)+'">')
                print('                 <h2 class="mb-0">')
                print('                     <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse'+'-'+master_ip_resource+'-'+str(mykeypos)+'" aria-expanded="false" aria-controls="collapse'+'-'+str(mykeypos)+'">')
                print('                         '+master_ip_resource+'-'+theslave+'')
                print('                     </button>')
                print('                 </h2>')
                print('             </div>')
                print('             <div id="collapse'+'-'+master_ip_resource+'-'+str(mykeypos)+'" class="collapse" aria-labelledby="heading'+'-'+master_ip_resource+'-'+str(mykeypos)+'" data-parent="#accordionIps-'+master_ip_resource+'-'+str(mykeypos)+'">')
                print('                 <div class="card-body">')
                print('                     <form class="form needs-validation" method="post" id="edit_ip_resource'+'-'+master_ip_resource+'-'+str(mykeypos)+'" onsubmit="return false;" novalidate>')

                # Master data
                print_input_fn(" Master IP Resource Name", " Enter the IP address resource name (EG: IP1). ", master_ip_resource, "master_ip_resource")
                print_input_fn(" Master LAN IP", " Enter the Local Area Network (LAN) IP. ", myip, "master_lan_ip")
                print_input_fn(" Master WAN IP", " Enter the Wide Area Network (WAN) IP. ", master_ip_resource_actual, "master_wan_ip")

                # Slave data
                print_input_fn(theslave, " Enter the slave server's Local Area Network (LAN) IP. ", slave_mapped_web_ip, "slave_lan_ip")
                print_input_fn(theslave, " Enter the slave server's Wide Area Network (WAN) IP. ", slave_mapped_dns_ip, "slave_wan_ip")

                print('                         <label hidden for="cluster_master_hostname">Master Host Name</label>')
                print('                         <input hidden name="master_hostname" id="cluster_master_hostname" value="'+myhostname+'">')
                print('                         <label hidden for="cluster_slave_hostname">Slave Host Name</label>')
                print('                         <input hidden name="slave_hostname" id="cluster_slave_hostname" value="'+theslave+'">')
                print('                         <label hidden for="cluster_edit_ip">Edit IP</label>')
                print('                         <input hidden name="action" id="cluster_edit_ip" value="editip">')

                print('                         <button id="edit-ip-resource'+'-'+master_ip_resource+'-'+str(mykeypos)+'" class="btn btn-outline-primary btn-block mt-4" type="submit">Edit IP resource</button>')
                print('                     </form>')
                print('                 </div>')
                print('             </div>')
                print('         </div>')
                print('     </div>')
                mykeypos = mykeypos + 1
            if master_ip_resource != "ip0":

                # Display form for IP address deletion
                print('                            <form class="form" method="post" id="delete_ip'+'-'+master_ip_resource+'" onsubmit="return false;">')
                print('                                <label hidden for="cluster_delete_ip_master_hostname">Delete Master Hostname IP</label>')
                print('                                <input hidden name="master_hostname" id="cluster_delete_ip_master_hostname" value="'+myhostname+'">')
                print('                                <label hidden for="cluster_delete_master_lan_ip">Delete Master LAN IP</label>')
                print('                                <input hidden name="master_lan_ip" id="cluster_delete_master_lan_ip" value="'+myip+'">')
                print('                                <label hidden for="cluster_delete_ip">Cluster Delete IP</label>')
                print('                                <input hidden name="action" id="cluster_delete_ip" value="delip">')
                print('                                <button id="delete-ip-btn'+'-'+master_ip_resource+'" class="btn btn-outline-danger btn-block mt-4 mb-4" type="submit">Delete '+master_ip_resource+'</button>')
                print('                            </form>')

            # Provide a seperation between each ip resource_

        print('                          </div>')

        # Tab Start / Tab5 ###########################
        # Display form for IP address mapping add
        print('                         <div class="tab-pane fade" id="ip-add-content" role="tabpanel" aria-labelledby="ip-add-tab">')
        print('                            <form class="form needs-validation" method="post" id="add_ip" onsubmit="return false;" novalidate>')

        # Master data
        print_input_fn("Master IP Resource Name", " Enter the IP address resource name (EG: IP1). ", "", "master_ip_resource")
        print_input_fn("Master LAN IP", " Enter the Local Area Network (LAN) IP. ", "", "master_lan_ip")

        for theslave in cluster_data_yaml_parsed.keys():

            # Slave data
            print_input_fn("LAN_IP_"+theslave, " Enter the slave server's Local Area Network (LAN) IP. ", "", theslave+"_lan_ip")
            print_input_fn("WAN_IP_"+theslave, " Enter the slave server's Wide Area Network (WAN) IP. ", "", theslave+"_wan_ip")

        print('                                <label hidden for="cluster_add_ip">Cluster Add IP</label>')
        print('                                <input hidden name="action" id="cluster_add_ip" value="addip">')
        print('                                <label hidden for="cluster_add_master_hostname">Cluster Add Master Hostname</label>')
        print('                                <input hidden name="master_hostname" id="cluster_add_master_hostname" value="'+myhostname+'">')
        print('                                <button id="add-ip-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Add IP Resource</button>')
        print('                            </form>')
        print('                         </div>')

        # Tab Start / Tab6 ###########################
        # Home directories
        print('                         <div class="tab-pane fade" id="home-content" role="tabpanel" aria-labelledby="home-tab">')
        with open('/opt/nDeploy/conf/nDeploy-cluster/group_vars/all', 'r') as group_vars_file:
            group_vars_dict = yaml.safe_load(group_vars_file)
        home_dir_list = group_vars_dict['homedir']

        if home_dir_list:
            print('                        <div class="label label-default mb-2">Currently syncing:</div>')
            print('                        <div class="clearfix">')
            mykeypos = 1
            for path in home_dir_list:
                print('                        <div class="input-group input-group-inline input-group-sm">')
                print('                            <div class="input-group-prepend">')
                print('                                <span class="input-group-text">'+path+'</span>')
                print('                            </div>')
                if path not in ['home']:
                    print('                        <div class="input-group-append">')
                    print('                            <form class="form delete_cluster_settings_directory" method="post" id="delete_cluster_settings_directory'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                    print('                                <label hidden for="cluster_the_home_dir">Cluster Home Directory</label>')
                    print('                                <input hidden name="thehomedir" id="cluster_the_home_dir" value="'+path+'">')
                    print('                                <label hidden for="cluster_delete_home_dir">Cluster Delete Home Directory</label>')
                    print('                                <input hidden name="action" id="cluster_delete_home_dir" value="deletehomedir">')
                    print('                                <button id="delete-cluster-settings-directory-btn" class="btn btn-danger btn-sm" type="submit">')
                    print('                                    <span class="sr-only">Delete</span>')
                    print('                                    <i class="fas fa-times"></i>')
                    print('                                </button>')
                    print('                            </form>')
                    print('                        </div>')
                mykeypos = mykeypos + 1
                print('                        </div>')
        print('                            </div>')
        print('                            <div class="label label-default mt-2 mb-2">Add another \'home\' directory to Unison sync:</div>')
        print('                            <form class="form" method="post" id="save_cluster_settings_directory" onsubmit="return false;">')

        print('                                <div class="input-group mb-0">')
        print('                                    <div class="input-group-prepend input-group-prepend-min">')
        print('                                        <span class="input-group-text">Path</span>')
        print('                                    </div>')
        print('                                    <label hidden for="cluster_save_home_dir">Cluster Save Home Directory</label>')
        print('                                    <input class="form-control" id="cluster_save_home_dir" placeholder="home2" type="text" name="thehomedir">')
        print('                                    <label hidden for="cluster_add_home_dir">Cluster Add Home Directory</label>')
        print('                                    <input hidden name="action" id="cluster_add_home_dir" value="addhomedir">')
        print('                                    <div class="input-group-append">')
        print('                                        <button id="save-cluster-settings-directory-btn" class="btn btn-outline-primary" type="submit">')
        print('                                            <span class="sr-only">Add</span><i class="fas fa-plus"></i>')
        print('                                        </button>')
        print('                                    </div>')
        print('                                </div>')

        print('                            </form>')
        print('                         </div>')

        # Tab Start / Tab7 ###########################
        # Run the playbook
        print('                         <div class="tab-pane fade" id="playbook-content" role="tabpanel" aria-labelledby="run-playbook">')
        print('                            <form class="form" method="post" id="deploy_playbook" onsubmit="return false;">')

        print('                                <label hidden for="deploy_cluster">Run the Playbook and Deploy the Cluster</label>')
        print('                                <input hidden name="action" id="deploy_cluster" value="releasethekraken">')

        print('                                <button id="run-playbook-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Run the Playbook and Deploy the Cluster</button>')
        print('                            </form>')
        print('                         </div>')



        # Tabs end ###########################
        print('                         </div>')

        # Main Tab Div End ###########################

    print('             </div> <!-- Card Body End -->')

    cardfooter('Only perform a hard reset if the unison archive is corrupt as the unison archive rebuild can be time consuming.')
else:
    cardheader('Setup Cluster', 'fas fa-align-justify')

    print('             <div class="card-body"> <!-- Card Body Start -->')

    # Case where conf/nDeploy-cluster/hosts exists but conf/ndeploy_cluster.yaml does not exists
    # This is when a user has setup the initial hosts file, but hasnt setup the cluster yet by running the playbook
    # If the inventory file exists
    if os.path.isfile(ansible_inventory_file):

        # Parse the inventory and display its contents
        with open(ansible_inventory_file, 'r') as my_inventory:
            ansible_inventory_file_parsed = yaml.safe_load(my_inventory)
        master_hostname = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'].keys()[0]
        master_server_id = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['server_id']
        master_ssh_port = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['ansible_port']
        master_main_ip = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['mainip']
        master_db_ip = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['dbip']
        master_dbmode = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['dbmode']
        master_lat = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['latitude']
        master_lon = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['longitude']
        master_repo = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['repo']
        master_dns = ansible_inventory_file_parsed['all']['children']['ndeploymaster']['hosts'][master_hostname]['dns']

        dbslave_hostname = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'].keys()[0]
        dbslave_server_id = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['server_id']
        dbslave_ssh_port = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['ansible_port']
        dbslave_main_ip = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['mainip']
        dbslave_db_ip = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['dbip']
        dbslave_dbmode = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['dbmode']
        dbslave_lat = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['latitude']
        dbslave_lon = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['longitude']
        dbslave_repo = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['repo']
        dbslave_dns = ansible_inventory_file_parsed['all']['children']['ndeploydbslave']['hosts'][dbslave_hostname]['dns']

        # Navigation tabs start here
        print('             <ul class="nav nav-tabs mb-4" id="clusterTabs" role="tablist">')
        print('                 <li class="nav-item"><a class="nav-link active" id="master-tab" data-toggle="tab" href="#master-content" role="tab" aria-controls="master-content" aria-selected="true">Master</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="slave-tab" data-toggle="tab" href="#slave-content" role="tab" aria-controls="slave-content" aria-selected="false">Slaves</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="add-tab" data-toggle="tab" href="#add-content" role="tab" aria-controls="add-content" aria-selected="false">Add Slave</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="home-tab" data-toggle="tab" href="#home-content" role="tab" aria-controls="home-content" aria-selected="false">Home Directory</a></li>')
        print('             </ul>')

        print('             <div class="tab-content" id="clusterTabsContent">')

        # Tab Start / Tab1 ###########################
        # Master data
        print('                         <div class="tab-pane fade show active" id="master-content" role="tabpanel" aria-labelledby="master-tab">')
        print('                            <form class="form needs-validation" method="post" id="save_cluster_settings_master" onsubmit="return false;" novalidate>')

        print_input_fn("Master Node FQDN", " Enter the master server's fully qualified domain name. ", master_hostname, "master_hostname")
        print_input_fn("Master Main IP", " Enter the master server's main IP address. ", master_main_ip, "master_main_ip")
        print_input_fn("Master DB IP", " Enter the master server's database IP address. ", master_db_ip, "master_db_ip")
        print_input_fn("Master SSH Port", " Enter the master server's SSH port. ", master_ssh_port, "master_ssh_port")
        print_input_fn("Master Server ID", " Enter the master server's ID (Usually 1). ", master_server_id, "master_server_id")
        print_input_fn("Master Latitude", " Enter the master server's latitude coordinate. ", master_lat, "master_lat")
        print_input_fn("Master Longitude", " Enter the master server's longitude coordinate. ", master_lon, "master_lon")

        print_select_fn("RPM Repo", " Select desired RPM Repo for the application's cluster build process. ", master_repo, "master_repo", "ndeploy", "ndeploy-edge")
        print_select_fn("DB Mode", " Select desired MaxScale database mode for this node. ", master_dbmode, "master_dbmode", "readconnroute", "rwsplit")
        print_select_fn("DNS Type", " Select desired MaxScale Mode for this node. ", master_dns, "master_dns", "bind", "geodns")

        print('                                <label hidden for="cluster_settings_save_master">Cluster Settings Save Master</label>')
        print('                                <input hidden name="action" id="cluster_settings_save_master" value="editmaster">')

        print('                                <button id="save-cluster-settings-master-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Save master Settings</button>')
        print('                            </form>')
        print('                        </div>')

        # Tab Start / Tab2 ###########################
        # Slave data
        print('                         <div class="tab-pane fade show" id="slave-content" role="tabpanel" aria-labelledby="slave-tab">')
        print('                            <form class="form needs-validation" method="post" id="save_cluster_settings_slave" onsubmit="return false;" novalidate>')

        print_input_fn("DBSlave Node FQDN", " Enter the slave server's fully qualified domain name. ", dbslave_hostname, "dbslave_hostname")
        print_input_fn("DBSlave Main IP", " Enter the slave server's main IP address. ", dbslave_main_ip, "dbslave_main_ip")
        print_input_fn("DBSlave DB IP", " Enter the slave server's database IP address. ", dbslave_db_ip, "dbslave_db_ip")
        print_input_fn("DBSlave SSH Port", " Enter the slave server's SSH port. ", dbslave_ssh_port, "dbslave_ssh_port")
        print_input_fn("DBSlave Server ID", " Enter the slave server's ID (Usually 2). ", dbslave_server_id, "dbslave_server_id")
        print_input_fn("DBSlave Latitude", " Enter the slave server's latitude coordinate. ", dbslave_lat, "dbslave_lat")
        print_input_fn("DBSlave Longitude", " Enter the slave server's longitude coordinate. ", dbslave_lon, "dbslave_lon")

        print_select_fn("RPM Repo", " Select desired RPM Repo for the application's cluster build process. ", dbslave_repo, "dbslave_repo", "ndeploy", "ndeploy-edge")
        print_select_fn("DB Mode", " Select desired MaxScale database mode for this node. ", dbslave_dbmode, "dbslave_dbmode", "readconnroute", "rwsplit")
        print_select_fn("DNS Type", " Select desired MaxScale Mode for this node. ", dbslave_dns, "dbslave_dns", "bind", "geodns")

        print('                                <label hidden for="cluster_settings_save_slave_db">Cluster Settings Save Slave</label>')
        print('                                <input hidden name="action" id="cluster_settings_save_slave_db" value="editdbslave">')
        print('                                <button id="save-cluster-settings-slave-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Save DBSlave Settings</button>')
        print('                            </form>')

        # Additional slaves
        for myslave in ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'].keys():
            if myslave != dbslave_hostname:

                # Lets get all the details of this slave server and present to the user for editing
                slave_hostname = myslave
                slave_server_id = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['server_id']
                slave_ssh_port = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['ansible_port']
                slave_main_ip = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['mainip']
                slave_db_ip = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['dbip']
                slave_dbmode = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['dbmode']
                slave_lat = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['latitude']
                slave_lon = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['longitude']
                slave_repo = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['repo']
                slave_dns = ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'][myslave]['dns']
                # Slave data
                print('     <div class="accordion mt-4" id="accordionSlaves-'+str(slave_server_id)+'">')
                print('         <div class="card mb-0">')
                print('             <div class="card-header" id="heading'+str(slave_server_id)+'">')
                print('                 <h2 class="mb-0">')
                print('                     <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse'+str(slave_server_id)+'" aria-expanded="false" aria-controls="collapse'+str(slave_server_id)+'">')
                print('                         Slave #'+str(slave_server_id)+'')
                print('                     </button>')
                print('                 </h2>')
                print('             </div>')

                print('             <div id="collapse'+str(slave_server_id)+'" class="collapse" aria-labelledby="heading'+str(slave_server_id)+'" data-parent="#accordionSlaves-'+str(slave_server_id)+'">')
                print('                 <div class="card-body">')
                print('                     <form class="form needs-validation" method="post" id="save_cluster_settings_slave_add-'+str(slave_server_id)+'" onsubmit="return false;" novalidate>')

                print_input_fn("Slave Node FQDN", " Enter the slave server's fully qualified domain name. ", slave_hostname, "slave_hostname")
                print_input_fn("Slave Main IP", " Enter the slave server's main IP address. ", slave_main_ip, "slave_main_ip")
                print_input_fn("Slave DB IP", " Enter the slave server's database IP address. ", slave_db_ip, "slave_db_ip")
                print_input_fn("Slave SSH Port", " Enter the slave server's SSH port. ", slave_ssh_port, "slave_ssh_port")
                print_input_fn("Slave Server ID", " Enter the slave server's ID (Usually 1). ", slave_server_id, "slave_server_id")
                print_input_fn("Slave Latitude", " Enter the slave server's latitude coordinate. ", slave_lat, "slave_lat")
                print_input_fn("Slave Longitude", " Enter the slave server's longitude coordinate. ", slave_lon, "slave_lon")

                print_select_fn("RPM Repo", " Select desired RPM Repo for the application's cluster build process. ", slave_repo, "slave_repo", "ndeploy", "ndeploy-edge")
                print_select_fn("DB Mode", " Select desired MaxScale database mode for this node. ", slave_dbmode, "slave_dbmode", "readconnroute", "rwsplit")
                print_select_fn("DNS Type", " Select desired MaxScale Mode for this node. ", slave_dns, "slave_dns", "bind", "geodns")

                print('                         <label hidden for="cluster_settings_edit_slave_add">Cluster Settings Slave Add</label>')
                print('                         <input hidden name="action" id="cluster_settings_edit_slave_add" value="editslave">')

                print('                     </form>')

                # Delete the Additional Slave
                print('                     <form class="form" method="post" id="delete_cluster_settings_slave-'+str(slave_server_id)+'" onsubmit="return false;">')
                print('                         <label hidden for="cluster_settings_delete_slave">Cluster Delete Slave</label>')
                print('                         <input hidden name="action" id="cluster_settings_delete_slave" value="deleteslave">')
                print('                         <label hidden for="cluster_settings_delete_slave_hostname">Cluster Delete Slave Hostname</label>')
                print('                         <input hidden name="slave_hostname" id="cluster_settings_delete_slave_hostname" value="'+myslave+'">')
                print('                     </form>')
                print('                     <div class="btn-group btn-block mt-4">')
                print('                         <button id="save-cluster-settings-slave-add-btn-'+str(slave_server_id)+'" class="btn btn-outline-primary btn-block" type="submit" form="save_cluster_settings_slave_add-'+str(slave_server_id)+'">Save Slave Settings</button>')
                print('                         <button id="delete-cluster-settings-slave-btn-'+str(slave_server_id)+'" class="btn btn-outline-danger btn-block" type="submit" form="delete_cluster_settings_slave-'+str(slave_server_id)+'">Delete Slave</button>')
                print('                     </div>')

                print('                 </div>')
                print('             </div>')
                print('         </div>')
                print('     </div>')
        print('</div>')

        # Tab Start / Tab3 ###########################
        # Add additional Slave
        print('                         <div class="tab-pane fade show" id="add-content" role="tabpanel" aria-labelledby="add-tab">')
        print('                            <form class="form needs-validation" method="post" id="save_cluster_settings_addi_slave_add" onsubmit="return false;" novalidate>')

        # Slave data
        print_input_fn("Slave Node FQDN", " Enter the slave server's fully qualified domain name. ", "", "slave_hostname")
        print_input_fn("Slave Main IP", " Enter the slave server's main IP address. ", "", "slave_main_ip")
        print_input_fn("Slave DB IP", " Enter the slave server's database IP address. ", "", "slave_db_ip")
        print_input_fn("Slave SSH Port", " Enter the slave server's SSH port. ", "", "slave_ssh_port")

        print('                                <label hidden for="cluster_settings_addi_slave_add">Cluster Settings Add Additional Slave</label>')
        print('                                <input hidden name="action" id="cluster_settings_addi_slave_add" value="addadditionalslave">')

        print('                                <button id="save-cluster-settings-addi-slave-add-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Add New Slave</button>')
        print('                            </form>')
        print('                         </div>')

        # Tab Start / Tab4 ###########################
        # Home directories
        print('                         <div class="tab-pane fade show" id="home-content" role="tabpanel" aria-labelledby="home-tab">')

        with open('/opt/nDeploy/conf/nDeploy-cluster/group_vars/all', 'r') as group_vars_file:
            group_vars_dict = yaml.safe_load(group_vars_file)
        home_dir_list = group_vars_dict['homedir']

        if home_dir_list:
            print('                        <div class="label label-default mb-2">Currently syncing:</div>')
            print('                        <div class="clearfix">')
            mykeypos = 1
            for path in home_dir_list:
                print('                        <div class="input-group input-group-inline input-group-sm">')
                print('                            <div class="input-group-prepend">')
                print('                                <span class="input-group-text">'+path+'</span>')
                print('                            </div>')
                if path not in ['home']:
                    print('                        <div class="input-group-append">')
                    print('                            <form class="form delete_cluster_settings_directory" method="post" id="delete_cluster_settings_directory'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                    print('                                <label hidden for="cluster_settings_dir">Cluster Settings Home Directory</label>')
                    print('                                <input hidden name="thehomedir" id="cluster_settings_dir" value="'+path+'">')
                    print('                                <label hidden for="cluster_settings_dir_delete">Cluster Settings Delete Home Directory</label>')
                    print('                                <input hidden name="action" id="cluster_settings_dir_delete" value="deletehomedir">')
                    print('                                <button id="delete-cluster-settings-directory-btn" class="btn btn-danger btn-sm" type="submit">')
                    print('                                    <span class="sr-only">Delete</span>')
                    print('                                    <i class="fas fa-times"></i>')
                    print('                                </button>')
                    print('                            </form>')
                    print('                        </div>')
                mykeypos = mykeypos + 1
                print('                        </div>')
        print('                            </div>')
        print('                            <div class="label label-default mt-2 mb-2">Add another \'home\' directory to Unison sync:</div>')
        print('                            <form class="form" method="post" id="save_cluster_settings_directory" onsubmit="return false;">')

        print('                                <div class="input-group mb-0">')
        print('                                    <div class="input-group-prepend input-group-prepend-min">')
        print('                                        <span class="input-group-text">Path</span>')
        print('                                    </div>')
        print('                                    <label hidden for="cluster_save_settings_dir">Cluster Save Settings Home Directory</label>')
        print('                                    <input class="form-control" id="cluster_save_settings_dir" placeholder="home2" type="text" name="thehomedir">')
        print('                                    <label hidden for="cluster_add_settings_dir">Cluster Add Settings Home Directory</label>')
        print('                                    <input hidden name="action" id="cluster_add_settings_dir" value="addhomedir">')
        print('                                    <div class="input-group-append">')
        print('                                        <button id="save-cluster-settings-directory-btn" class="btn btn-outline-primary" type="submit">')
        print('                                            <span class="sr-only">Add</span><i class="fas fa-plus"></i>')
        print('                                        </button>')
        print('                                    </div>')
        print('                                </div>')

        print('                            </form>')
        print('                         </div>')

        # Tab ends ###########################
        print('                         </div>')
        # Main Tab Div End ###########################

    else:

        # Case where conf/nDeploy-cluster/hosts and conf/ndeploy_cluster.yaml does not exists
        # This means the user hast tried to setup a cluster yet!
        # We present before him an option to add the initial slave( setup ansible inventory )
        # Get the server main IP
        myip = get('https://api.ipify.org').text

        # Display form for ndeploymaster
        print('                            <form class="form needs-validation" method="post" id="cluster_setup" onsubmit="return false;" novalidate>')

        print_input_fn("Master Node FQDN", " Enter the master server's fully qualified domain name. ", myhostname, "master_hostname")
        print_input_fn("Master Main IP", " Enter the master server's main IP address. ", myip, "master_main_ip")
        print_input_fn("Master DB IP", " Enter the master server's database IP address. ", myip, "master_db_ip")
        print_input_fn("Master SSH Port", " Enter the master server's SSH port. ", "", "master_ssh_port")
        print_input_fn("Slave Node FQDN", " Enter the slave server's fully qualified domain name. ", "", "slave_hostname")
        print_input_fn("Slave Main IP", " Enter the slave server's main IP address. ", "", "slave_main_ip")
        print_input_fn("Slave DB IP", " Enter the slave server's database IP address. ", "", "slave_db_ip")
        print_input_fn("Slave SSH Port", " Enter the slave server's SSH port. ", "", "slave_ssh_port")

        print('                                <label hidden for="cluster_setup2">Cluster Setup</label>')
        print('                                <input hidden name="action" id="cluster_setup2" value="setup">')

        print('                                <button id="cluster-setup-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Save cluster Settings</button>')
        print('                            </form>')

    print('             </div> <!-- Card Body End -->')

    cardfooter('Database IP will be different from main IP only if you have a LAN link for db replication')

print('                </div> <!-- End Cluster Tab -->')

# Zone Tab
print('')
print('                <!-- Sync Tab -->')
print('                <div class="tab-pane fade" id="v-pills-zone" role="tabpanel" aria-labelledby="v-pills-zone-tab">')

# Sync cluster
if os.path.isfile(cluster_config_file) and os.path.isfile(homedir_config_file):
    cardheader('Sync Cluster', 'fas fa-sync')
    print('             <div class="card-body"> <!-- Card Body Start -->')

    print('                 <form class="form mb-3" id="sync_web_files" onsubmit="return false;">')
    print('                     <div class="input-group">')
    print('                         <div class="input-group-prepend input-group-prepend-min">')
    print('                             <label for="sync_web_files_select" class="input-group-text">Files</label>')
    print('                         </div>')
    print('                         <select name="user" id="sync_web_files_select" class="custom-select">')
    user_list = os.listdir("/var/cpanel/users")
    for cpuser in sorted(user_list):
        if cpuser != 'nobody' and cpuser != 'system':
            print('                     <option value="'+cpuser+'">'+cpuser+'</option>')
    print('                         </select>')
    print('                     </div>')
    print('                     <button id="sync-web-files-btn" type="submit" class="btn btn-outline-primary btn-block mt-4">Sync web files</button>')
    print('                 </form>')

    print('                 <form class="form" id="sync_geodns_zone" onsubmit="return false;">')
    print('                     <div class="input-group">')
    print('                         <div class="input-group-prepend input-group-prepend-min">')
    print('                             <label for="sync_geodns_zone_select" class="input-group-text">Zone</label>')
    print('                         </div>')
    print('                         <select name="user" id="sync_geodns_zone_select" class="custom-select">')
    user_list = os.listdir("/var/cpanel/users")
    for cpuser in sorted(user_list):
        if cpuser != 'nobody' and cpuser != 'system':
            print('                     <option value="'+cpuser+'">'+cpuser+'</option>')
    print('                         </select>')
    print('                     </div>')
    print('                     <button id="sync-geodns-zone-btn" type="submit" class="btn btn-outline-primary btn-block mt-4">Sync GeoDNS Zone</button>')
    print('                 </form>')

    print('             </div> <!-- Card Body End -->')
    cardfooter('Choose a user to sync dns zone or web files')
else:
    cardheader('Cluster Sync Disabled', 'fas fa-sync')
    cardfooter('Cluster Sync is only available when cluster is setup')

print('                </div> <!-- End Sync Tab -->')

# PHP Tab
print('')
print('                <!-- PHP Tab -->')
print('                <div class="tab-pane fade" id="v-pills-php" role="tabpanel" aria-labelledby="v-pills-php-tab">')

# Set Default PHP for AutoConfig
cardheader('Default PHP for Autoswitch', 'fab fa-php')
print('                 <div class="card-body p-0">  <!-- Card Body Start -->')
print('                     <div id="autoswitch-php-status" class="row no-gutters row-1"> <!-- Row Start -->')

# Check if we have a Preferred PHP and allow selection.
print('                         <div class="col-md-6 alert"><i class="fab fa-php"></i> Default PHP</div>')
print('                         <div class="col-md-6">')
print('                             <div class="row no-gutters">')
if os.path.isfile(installation_path+"/conf/preferred_php.yaml"):
    preferred_php_yaml = open(installation_path+"/conf/preferred_php.yaml", 'r')
    preferred_php_yaml_parsed = yaml.safe_load(preferred_php_yaml)
    preferred_php_yaml.close()
    phpversion = preferred_php_yaml_parsed.get('PHP')
    myphpversion = phpversion.keys()[0]
    print('                             <div class="col-md-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
else:
    myphpversion = "Unset"
    print('                             <div class="col-md-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')

print('                                 <div class="col-md-9 alert">'+myphpversion+'</div>')
print('                             </div>')
print('                         </div>')
print('                     </div>')
print('                 </div> <!-- Card Body End -->')

backend_config_file = installation_path+"/conf/backends.yaml"
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()

if "PHP" in backend_data_yaml_parsed:
    print('             <div class="card-body"> <!-- Card Body Start -->')
    print('                 <form class="form" id="default_php_autoswitch" onsubmit="return false;">')
    print('                     <div class="input-group">')
    print('                         <div class="input-group-prepend input-group-prepend-min">')
    print('                             <label for="default_php_autoswitch_select" class="input-group-text">PHP</label>')
    print('                         </div>')
    print('                         <select name="phpversion" id="default_php_autoswitch_select" class="custom-select">')

    php_backends_dict = backend_data_yaml_parsed["PHP"]
    for versions_defined in list(php_backends_dict.keys()):
        if versions_defined == myphpversion:
            print('                     <option selected value="'+myphpversion+'">'+myphpversion+'</option>')
        else:
            print('                     <option value="'+versions_defined+'">'+versions_defined+'</option>')
    print('                         </select>')
    print('                     </div>')
    print('                     <button id="default-php-autoswitch-btn" type="submit" class="btn btn-outline-primary btn-block mt-4">Set Default PHP</button>')
    print('                 </form>')
    print('             </div> <!-- Card Body End -->')
cardfooter('Automatic switch to Nginx will use versions set in MultiPHP or if MultiPHP is not used the phpversion above')

print('                </div> <!-- End PHP Tab -->')

# DOS Tab
print('')
print('                <!-- DOS Tab -->')
print('                <div class="tab-pane fade" id="v-pills-dos" role="tabpanel" aria-labelledby="v-pills-dos-tab">')

# DDOS Protection
cardheader('DDOS Protection', 'fas fa-user-shield')
print('                 <div class="card-body p-0">  <!-- Card Body Start -->')
print('                     <div class="row no-gutters row-2-col row-no-btm"> <!-- Row Start -->')
print('                         <div class="col-md-6 alert"><i class="fas fa-shield-alt"></i> Nginx</div>')
print('                         <div class="col-md-6">')
print('                             <div class="row no-gutters">')

if os.path.isfile('/etc/nginx/conf.d/dos_mitigate_systemwide.enabled'):
    print('                             <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
    print('                             <div class="col-9">')
    print('                                 <form id="ddos_protection_nginx_disable" class="form" onsubmit="return false;">')
    print('                                     <label hidden for="nginx_ddos_disabled">DDOS Disabled</label>')
    print('                                     <input hidden name="ddos" id="nginx_ddos_disabled" value="disable">')
    print('                                     <button id="ddos-protection-nginx-disable-btn" type="submit" class="alert btn btn-secondary">Disable</button>')
else:
    print('                             <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
    print('                             <div class="col-9">')
    print('                                 <form id="ddos_protection_nginx_enable" class="form" onsubmit="return false;">')
    print('                                     <label hidden for="nginx_ddos_enabled">DDOS Enabled</label>')
    print('                                     <input hidden name="ddos" id="nginx_ddos_enabled" value="enable">')
    print('                                     <button id="ddos-protection-nginx-enable-btn" type="submit" class="alert btn btn-secondary">Enable</button>')

print('                                     </form>')
print('                                 </div>')
print('                             </div>')
print('                         </div>')

try:
    with open(os.devnull, 'w') as FNULL:
        subprocess.call(['systemctl', '--version'], stdout=FNULL, stderr=subprocess.STDOUT)
except OSError:
    pass
else:
    with open(os.devnull, 'w') as FNULL:
        firehol_enabled = subprocess.call("systemctl is-active firehol.service", stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
    print('                     <div class="col-md-6 alert"><i class="fas fa-shield-alt"></i> SYNPROXY</div>')
    print('                     <div class="col-md-6">')
    print('                         <div class="row no-gutters">')

    if firehol_enabled == 0:
        print('                         <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
        print('                         <div class="col-9">')
        print('                             <form id="ddos_protection_synproxy_disable" class="form" onsubmit="return false;">')
        print('                                 <label hidden for="synproxy_ddos_disabled">DDOS Disabled</label>')
        print('                                 <input hidden name="ddos" id="synproxy_ddos_disabled" value="disable">')
        print('                                 <button id="ddos-protection-synproxy-disable-btn" type="submit" class="alert btn btn-secondary">Disable</button>')
    else:
        print('                         <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
        print('                         <div class="col-9">')
        print('                             <form id="ddos_protection_synproxy_enable" class="form" onsubmit="return false;">')
        print('                                 <label hidden for="synproxy_ddos_enabled">DDOS Enabled</label>')
        print('                                 <input hidden name="ddos" id="synproxy_ddos_enabled" value="enable">')
        print('                                 <button id="ddos-protection-synproxy-enable-btn" type="submit" class="alert btn btn-secondary">Enable</button>')

    print('                                 </form>')
    print('                             </div>')
    print('                         </div>')
    print('                     </div>')

print('                     </div> <!-- Row End -->')
print('                 </div> <!-- Card Body End -->')
cardfooter('Turn these settings on when you are under a DDOS Attack but remember to disable CSF or any other firewall before turning on SYNPROXY (FireHol).')

print('                </div> <!-- End DOS Tab -->')

# PHP_FPM Tab
print('')
print('                <!-- PHP_FPM Tab -->')
print('                <div class="tab-pane fade" id="v-pills-php_fpm" role="tabpanel" aria-labelledby="v-pills-php_fpm-tab">')

# PHP-FPM Pool Editor
phpfpmpool_hint = " Secure and non secure PHP-FPM Pools attached to cPanel users for use with Native NGINX. "
cardheader('PHP-FPM Pool Editor', 'fas fa-sitemap')
print('                 <div class="card-body"> <!-- Card Body Start -->')
print('                     <form class="form" action="phpfpm_pool_editor.cgi" method="get">')
print('                         <div class="input-group">')
print('                             <div class="input-group-prepend input-group-prepend-min">')
print('                                 <label for="phpfpm_pool_editor" class="input-group-text">')
print('                                     '+return_prepend("cPanel User", phpfpmpool_hint))
print('                                 </label>')
print('                             </div>')
print('                             <select name="poolfile" id="phpfpm_pool_editor" class="custom-select">')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    conf_list = os.listdir("/opt/nDeploy/secure-php-fpm.d")
    for filename in sorted(conf_list):
        user, extension = filename.split('.')
        if user != 'nobody':
            print('                     <option value="/opt/nDeploy/secure-php-fpm.d/'+filename+'">'+user+'</option>')
else:
    conf_list = os.listdir("/opt/nDeploy/php-fpm.d")
    for filename in sorted(conf_list):
        user, extension = filename.split('.')
        if user != 'nobody':
            print('                     <option value="/opt/nDeploy/php-fpm.d/'+filename+'">'+user+'</option>')
print('                             </select>')
print('                         </div>')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    print('                     <label hidden for="phpfpm_pool_editor_on">Phpfpm Pool Editor Enabled</label>')
    print('                     <input hidden name="section" id="phpfpm_pool_editor_on" value="1">')
else:
    print('                     <label hidden for="phpfpm_pool_editor_off">Phpfpm Pool Editor Disabled</label>')
    print('                     <input hidden name="section" id="phpfpm_pool_editor_off" value="0">')
print('                         <button class="btn btn-outline-primary btn-block mt-4" type="submit">Edit Settings</button>')
print('                     </form>')
print('                 </div> <!-- Card Body End -->')
cardfooter('Settings such as: pm.max_requests, pm.max_spare_servers, session.save_path, pm.max_children')

print('                </div> <!-- End PHP_FPM Tab -->')

# Map Tab
print('')
print('                <!-- Map Tab -->')
print('                <div class="tab-pane fade" id="v-pills-map" role="tabpanel" aria-labelledby="v-pills-map-tab">')

# Map cPanel Package to NGINX
cardheader('Map cPanel Package to NGINX', 'fas fa-box-open')
print('                 <div class="card-body p-0"> <!-- Card Body Start -->')
print('                     <div class="row no-gutters row-1"> <!-- Row Start -->')
print('                         <div class="col-md-6 alert"><i class="fas fa-box"></i> NGINX -> Package</div>')
print('                         <div class="col-md-6">')
print('                             <div class="row no-gutters">')

if os.path.isfile(installation_path+'/conf/lock_domaindata_to_package'):
    print('                             <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
    print('                             <div class="col-9">')
    print('                                 <form class="form" method="post" id="package_lock_disable" onsubmit="return false;">')
    print('                                     <label hidden for="lock_domaindata_to_package">Lock Domaindata To Package</label>')
    print('                                     <input hidden name="package_lock" id="lock_domaindata_to_package" value="disabled">')
    print('                                     <button id="package-lock-disable-btn" type="submit" class="alert btn btn-secondary">Disable</button>')
    print('                                 </form>')
    print('                             </div>')
    print('                         </div>')
else:
    print('                         <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
    print('                             <div class="col-9">')
    print('                                 <form class="form" method="post" id="package_lock_enable" onsubmit="return false;">')
    print('                                     <label hidden for="lock_domaindata_to_package">Lock Domaindata To Package</label>')
    print('                                     <input hidden name="package_lock" id="lock_domaindata_to_package" value="enabled">')
    print('                                     <button id="package-lock-enable-btn" type="submit" class="alert btn btn-secondary">Enable</button>')
    print('                                 </form>')
    print('                             </div>')
    print('                         </div>')

print('                         </div>')
print('                     </div> <!-- Row End -->')
print('                 </div> <!-- Card Body End -->')
print('                 <div class="card-body"> <!-- Card Body Start -->')

cpanpackage_hint = " Map a NGINX configuration to an installed cPanel package. "

# Workaround for python 2.6
if platform.python_version().startswith('2.6'):
    listpkgs = subprocess.Popen('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', stdout=subprocess.PIPE, shell=True).communicate()[0]
else:
    listpkgs = subprocess.check_output('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', shell=True)
mypkgs = json.loads(listpkgs)

print('                     <form class="form" action="pkg_profile.cgi" method="get">')
print('                         <div class="input-group">')
print('                             <div class="input-group-prepend input-group-prepend-min">')
print('                                 <label for="connect_cpanel_nginx" class="input-group-text">')
print('                                     '+return_prepend("cPanel Package", cpanpackage_hint))
print('                                 </label>')
print('                             </div>')
print('                             <select name="cpanelpkg" id="connect_cpanel_nginx" class="custom-select">')

for thepkg in sorted(mypkgs.get('package')):
    pkgname = thepkg.get('name').encode('utf-8').replace(' ', '_')
    print('                             <option value="'+pkgname+'">'+pkgname+'</option>')

print('                             </select>')
print('                         </div>')
print('                         <button class="btn btn-outline-primary btn-block mt-4" type="submit">Edit Pkg</button>')
print('                     </form>')
print('                 </div> <!-- Card Body End -->')
cardfooter('This option will automatically assign NGINX Config/Settings to a cPanel Package when enabled. This will also reset any NGINX Config/Settings the user has configured if the cPanel Package undergoes an Upgrade/Downgrade process.')

print('                </div> <!-- End Map Tab -->')

# Limit Tab
print('')
print('                <!-- Limit Tab -->')
print('                <div class="tab-pane fade" id="v-pills-limit" role="tabpanel" aria-labelledby="v-pills-limit-tab">')

# System Resource Limit
cardheader('System Resource Limit', 'fas fa-compress')
print('                        <div class="card-body"> <!-- Card Body Start -->')

with open('/etc/redhat-release', 'r') as releasefile:
    osrelease = releasefile.read().split(' ')[0]
if not osrelease == 'CloudLinux':
    if os.path.isfile('/usr/bin/systemctl'):

        # Next sub-section start here
        if os.path.isfile(installation_path+"/conf/secure-php-enabled"):  # if per user php-fpm master process is set
            userlist = os.listdir("/var/cpanel/users")
            print('                            <form class="form" action="resource_limit.cgi" method="get">')
            print('                                <div class="input-group">')
            print('                                    <div class="input-group-prepend input-group-prepend-min">')
            print('                                        <label for="set_user_resource" class="input-group-text">User</label>')
            print('                                    </div>')
            print('                                    <select name="unit" id="set_user_resource" class="custom-select">')

            for cpuser in sorted(userlist):
                if cpuser != 'nobody' and cpuser != 'system':
                    print('                                <option value="'+cpuser+'">'+cpuser+'</option>')

            print('                                    </select>')
            print('                                    <label hidden for="set_user_resource_limit">Set User Resource Limit</label>')
            print('                                    <input hidden name="mode" id="set_user_resource_limit" value="user">')
            print('                                </div>')
            print('                                <button class="btn btn-outline-primary btn-block mt-4" type="submit">Set Limit</button>')
            print('                            </form>')

            print('                            <form class="form mt-4" action="resource_limit.cgi" method="get">')
            print('                                <div class="input-group">')
            print('                                    <div class="input-group-prepend input-group-prepend-min">')
            print('                                        <label for="resource_limit_select" class="input-group-text">Service</label>')
            print('                                    </div>')
            print('                                    <select name="unit" id="resource_limit_select" class="custom-select">')

            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm", "ea-php73-php-fpm":
                print('                                        <option value="'+service+'">'+service+'</option>')

            print('                                    </select>')
            print('                                    <label hidden for="set_resource_limit">Set Resource Limit</label>')
            print('                                    <input hidden name="mode" id="set_resource_limit" value="service">')
            print('                               </div>')
            print('                               <button class="btn btn-outline-primary btn-block mt-4" type="submit">Set Limit</button>')
            print('                           </form>')
        else:
            print('                           <form class="form" action="resource_limit.cgi" method="get">')
            print('                               <div class="input-group">')
            print('                                   <div class="input-group-prepend input-group-prepend-min">')
            print('                                       <label for="resource_limit_select" class="input-group-text">Resource</label>')
            print('                                   </div>')
            print('                                   <select name="unit" id="resource_limit_select" class="custom-select">')

            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm", "ea-php73-php-fpm":
                print('                                       <option value="'+service+'">'+service+'</option>')

            print('                                   </select>')
            print('                                   <label hidden for="set_resource_limit">Set Resource Limit</label>')
            print('                                   <input hidden name="mode" id="set_resource_limit" value="service">')
            print('                               </div>')
            print('                               <button class="btn btn-outline-primary btn-block mt-4" type="submit">Set Limit</button>')
            print('                           </form>')
print('                        </div> <!-- Card Body End -->')
cardfooter('BlockIOWeight range is 10-1000, CPUShares range is 0-1024, MemoryLimit range is calculated using available memory')

print('                </div> <!-- End Limit Tab -->')
print('            </div>')
print('        </div> <!-- End WHM Tabs Row -->')

print_footer()
