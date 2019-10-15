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
from commoninclude import bcrumb, return_prepend, print_header, print_footer, print_modals, print_loader, cardheader, cardfooter, return_multi_input


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

# Read in PHP Backend Status for Dash
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()

php_status = False
php_status_dict = {}
if "PHP" in backend_data_yaml_parsed:
    php_backends_dict = backend_data_yaml_parsed["PHP"]
    for php, path in list(php_backends_dict.items()):
        for myprocess in psutil.process_iter():
            # Workaround for Python 2.6
            if platform.python_version().startswith('2.6'):
                myexe = myprocess.exe
            else:
                myexe = myprocess.exe()
            if path+"/usr/sbin/php-fpm" in myexe:
                php_status_dict[php] = "ACTIVE"
                break
            else:
                php_status_dict[php] = "NOT ACTIVE"

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

print('            <!-- Dash Widgets Start -->')
print('            <div id="dashboard" class="row flex-row">')
print('')

# Nginx Status
print('                <div class="col-sm-6 col-xl-3"> <!-- Dash Item Start -->')
cardheader('')
print('                        <div class="card-body text-center"> <!-- Card Body Start -->')
print('                            <h4 class="mb-0">Nginx Status</h4>')
print('                            <ul class="list-unstyled mb-0">')
print('                                <li><small>'+nginx_version+'</small></li>')
if nginx_status:
    print('                                <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                                <li class="mt-2 text-danger">Stopped <i class="fas fa-power-off ml-1"></i></li>')
print('                            </ul>')
print('                        </div> <!-- Card Body End -->')
print('                        <form class="form" id="toastForm21" onsubmit="return false;">')
print('                            <input hidden name="action" value="nginxreload">')
print('                            <button class="btn btn-secondary btn-block mb-0">Reload</button>')
print('                        </form>')
cardfooter('')
print('                </div> <!-- Dash Item End -->')

# Autom8n Version Status
print('                <div class="col-sm-6 col-xl-3"> <!-- Dash Item Start -->')
cardheader('')
print('                        <div class="card-body text-center"> <!-- Card Body Start -->')
print('                            <h4 class="mb-0">Watcher Status</h4>')
print('                            <ul class="list-unstyled mb-0">')
print('                                <li><small>'+brand+' '+autom8n_version.replace("Autom8n ",'')+'</small></li>')
if watcher_status:
    print('                                <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                                <li class="mt-2 text-danger">Stopped <i class="fas fa-power-off ml-1"></i></li>')
print('                            </ul>')
print('                        </div> <!-- Card Body End -->')
print('                        <form class="form" id="toastForm22" onsubmit="return false;">')
print('                            <input hidden name="action" value="watcherrestart">')
print('                            <button class="btn btn-secondary btn-block mb-0">Restart</button>')
print('                        </form>')
cardfooter('')
print('                </div> <!-- Dash Item End -->')

# Cache/Redis Status
print('                <div class="col-sm-6 col-xl-3"> <!-- Dash Item Start -->')
cardheader('')
print('                        <div class="card-body text-center"> <!-- Card Body Start -->')
print('                            <h4 class="mb-0">Clear Caches</h4>')
print('                            <ul class="list-unstyled mb-0">')
print('                                <li><small>Redis</small></li>')
print('                                <li class="mt-2"><i class="fas fa-memory ml-1"></i></li>')
print('                            </ul>')
print('                        </div> <!-- Card Body End -->')
print('                        <form class="form" id="toastForm23" onsubmit="return false;">')
print('                            <input hidden name="action" value="redisflush">')
print('                            <button class="btn btn-secondary btn-block mb-0">Flush All</button>')
print('                        </form>')
cardfooter('')
print('                </div> <!-- Dash Item End -->')

# Restart Backends
print('                <div class="col-sm-6 col-xl-3"> <!-- Dash Item Start -->')
cardheader('')
print('                        <div class="card-body text-center"> <!-- Card Body Start -->')
print('                            <h4 class="mb-0">PHP Backends</h4>')
print('                            <ul class="list-unstyled mb-0">')
print('                                <li><small>PHP-FPM</small></li>')

for service, status in list(php_status_dict.items()):
    if status == "NOT ACTIVE":
        php_status = "True"
        break


if not php_status:
    print('                                <li class="mt-2 text-success">Running <i class="fas fa-power-off ml-1"></i></li>')
else:
    print('                                <li class="mt-2 text-danger">Issue Detected <i class="fas fa-power-off ml-1"></i></li>')
print('                            </ul>')
print('                        </div> <!-- Card Body End -->')
print('                        <form class="form" id="restart-backends" onsubmit="return false;">')
print('                            <input hidden name="action" value="restart_backends">')
print('                            <button class="btn btn-secondary btn-block mb-0">Restart</button>')
print('                        </form>')
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
print('                    <a class="nav-link active" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab">System Health & Backup</a>')
print('                    <a class="nav-link" id="v-pills-cluster-tab" data-toggle="pill" href="#v-pills-cluster" role="tab" aria-controls="v-pills-cluster">Cluster Status</a>')
print('                    <a class="nav-link" id="v-pills-zone-tab" data-toggle="pill" href="#v-pills-zone" role="tab" aria-controls="v-pills-zone">Cluster Sync</a>')
print('                    <a class="nav-link" id="v-pills-php-tab" data-toggle="pill" href="#v-pills-php" role="tab" aria-controls="v-pills-php">Default PHP for Autoswitch</a>')
print('                    <a class="nav-link" id="v-pills-dos-tab" data-toggle="pill" href="#v-pills-dos" role="tab" aria-controls="v-pills-dos">DDOS Protection</a>')
print('                    <a class="nav-link" id="v-pills-php_fpm-tab" data-toggle="pill" href="#v-pills-php_fpm" role="tab" aria-controls="v-pills-php_fpm">PHP-FPM Pool Editor</a>')
print('                    <a class="nav-link" id="v-pills-map-tab" data-toggle="pill" href="#v-pills-map" role="tab" aria-controls="v-pills-map">Package Editor</a>')
print('                    <a class="nav-link" id="v-pills-limit-tab" data-toggle="pill" href="#v-pills-limit" role="tab" aria-controls="v-pills-limit">System Resource Limit</a>')
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
print('                            <a class="dropdown-item" id="v-pills-system-tab" data-toggle="pill" href="#v-pills-system" role="tab" aria-controls="v-pills-system-tab" aria-selected="false">System Health & Backup</a>')
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
cardheader('System Health & Backup','fas fa-cogs')
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
print('                                    <form class="form" id="modalForm3" onsubmit="return false;">')
print('                                        <button class="btn btn-block btn-icon" type="submit"><i class="fas fa-bug"></i> Check Processes</button>')
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
    cardheader('Cluster Status','fas fa-align-justify')
    print('             <div class="card-body p-0">  <!-- Card Body Start -->')
    print('                 <div class="row no-gutters row-1"> <!-- Row Start -->')

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

    print('                 <form class="form" id="toastForm4" onsubmit="return false;">')
    print('                     <input hidden name="mode" value="restart">')
    print('                 </form>')

    print('                 <form class="form" id="toastForm5" onsubmit="return false;">')
    print('                     <input hidden name="mode" value="reset">')
    print('                 </form>')

    print('                 <form class="form" id="toastForm26" onsubmit="return false;">')
    print('                     <input hidden name="mode" value="reset">')
    print('                 </form>')

    print('                 <div class="btn-group btn-block">')
    print('                     <button type="submit" class="btn btn-outline-primary" form="toastForm4">Soft Restart</button>')
    print('                     <button type="submit" class="btn btn-outline-primary" form="toastForm5">Hard Reset</button>')
    print('                     <button type="submit" class="btn btn-outline-primary" form="toastForm26">Reset Csync2</button>')
    print('                 </div>')

    # If the inventory file exists
    if os.path.isfile(ansible_inventory_file):
        # parse the inventory and display its contents
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

        # master data
        print('             <ul class="nav nav-tabs mt-4 mb-4" id="clusterTabs" role="tablist">')
        print('                 <li class="nav-item"><a class="nav-link active" id="master-tab" data-toggle="tab" href="#master-content" role="tab" aria-controls="master-content" aria-selected="true">Master</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="slave-tab" data-toggle="tab" href="#slave-content" role="tab" aria-controls="slave-content" aria-selected="true">Slaves</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="add-tab" data-toggle="tab" href="#add-content" role="tab" aria-controls="add-content" aria-selected="true">Add Slave</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="ip-add-tab" data-toggle="tab" href="#ip-add-content" role="tab" aria-controls="ip-add-content" aria-selected="true">Add IP</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="ip-tab" data-toggle="tab" href="#ip-content" role="tab" aria-controls="ip-content" aria-selected="true">IP Resource</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="home-tab" data-toggle="tab" href="#home-content" role="tab" aria-controls="home-content" aria-selected="true">Home Directory</a></li>')
        print('             </ul>')

        print('                     <div class="tab-content" id="clusterTabsContent">')

        # master data
        print('                         <div class="tab-pane fade show active" id="master-content" role="tabpanel" aria-labelledby="master-tab">')
        print('                            <form class="form needs-validation" method="post" id="toastForm29" novalidate>')

        master_hostname_hint = " Masters FQDN "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master server FQDN", master_hostname_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip01" value="'+master_hostname+'" type="text" name="master_hostname" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_main_ip_hint = " Masters Main IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master Main IP", master_main_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip02" value="'+master_main_ip+'" type="text" name="master_main_ip" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_db_ip_hint = " Masters Database IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master Database IP", master_db_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip03" value="'+master_db_ip+'" type="text" name="master_db_ip" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_ssh_port_hint = " Masters ssh port "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master ssh port", master_ssh_port_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(master_ssh_port)+'" type="text" name="master_ssh_port" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_server_id_hint = " Masters server id "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master server id", master_server_id_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip04" value="'+str(master_server_id)+'" type="text" name="master_server_id" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_lat_hint = " Masters server latitude "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master latitude", master_lat_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip05" value="'+str(master_lat)+'" type="text" name="master_lat" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_lon_hint = " Masters severs longitude"
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master longitude", master_lon_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip06" value="'+str(master_lon)+'" type="text" name="master_lon" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_repo_hint = " RPM repo "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("RPM repo", master_repo_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip07" value="'+master_repo+'" type="text" name="master_repo" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_dbmode_hint = " MaxScale Mode "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("DBMode", master_dbmode_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip08" value="'+master_dbmode+'" type="text" name="master_dbmode" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        master_dns_hint = " Master DNS server "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("DNS", master_dns_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip09" value="'+master_dns+'" type="text" name="master_dns" required>')
        print('                                            <div class="invalid-tooltip">Needs some info</div>')
        print('                                        </div>')

        print('                                    <input hidden name="action" value="editmaster">')

        print('                                        <button class="btn btn-outline-primary btn-block mt-4" type="submit">Save Master Settings</button>')
        print('                            </form>')
        print('                         </div>')

        # slave data
        print('                         <div class="tab-pane fade" id="slave-content" role="tabpanel" aria-labelledby="slave-tab">')
        print('                            <form class="form" method="post" id="toastForm30" onsubmit="return false;">')

        dbslave_hostname_hint = " Slave FQDN "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave server FQDN", dbslave_hostname_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_hostname+'" type="text" name="dbslave_hostname">')
        print('                                        </div>')

        dbslave_main_ip_hint = " Slaves Main IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Main IP", dbslave_main_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_main_ip+'" type="text" name="dbslave_main_ip">')
        print('                                        </div>')

        dbslave_db_ip_hint = " Slaves Database IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Database IP", dbslave_db_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_db_ip+'" type="text" name="dbslave_db_ip">')
        print('                                        </div>')

        dbslave_ssh_port_hint = " Slaves ssh port "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave ssh port", dbslave_ssh_port_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(dbslave_ssh_port)+'" type="text" name="dbslave_ssh_port">')
        print('                                        </div>')

        dbslave_server_id_hint = " Slaves server id "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave server id", dbslave_server_id_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(dbslave_server_id)+'" type="text" name="dbslave_server_id">')
        print('                                        </div>')

        dbslave_lat_hint = " Slave server latitude "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave latitude", dbslave_lat_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(dbslave_lat)+'" type="text" name="dbslave_lat">')
        print('                                        </div>')

        dbslave_lon_hint = " Slave sever longitude"
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave longitude", dbslave_lon_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(dbslave_lon)+'" type="text" name="dbslave_lon">')
        print('                                        </div>')

        dbslave_repo_hint = " RPM repo "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("RPM repo", dbslave_repo_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_repo+'" type="text" name="dbslave_repo">')
        print('                                        </div>')

        dbslave_dbmode_hint = " MaxScale Mode "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("DBMode", dbslave_dbmode_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_dbmode+'" type="text" name="dbslave_dbmode">')
        print('                                        </div>')

        dbslave_dns_hint = " Slave DNS server "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("DNS", dbslave_dns_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_dns+'" type="text" name="dbslave_dns">')
        print('                                        </div>')

        print('                                    <input hidden name="action" value="editdbslave">')

        print('                                    <button class="btn btn-outline-primary btn-block mt-3" type="submit">Save slave Settings</button>')
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
                # slave data
                print('                            <form class="form toastForm32-wrap" method="post" id="toastForm32-'+str(slave_server_id)+'" onsubmit="return false;">')

                slave_hostname_hint = " Slave FQDN "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave server FQDN", slave_hostname_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_hostname+'" type="text" name="slave_hostname">')
                print('                                        </div>')

                slave_main_ip_hint = " Slaves Main IP "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave Main IP", slave_main_ip_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_main_ip+'" type="text" name="slave_main_ip">')
                print('                                        </div>')

                slave_db_ip_hint = " Slaves Database IP "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave Database IP", slave_db_ip_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_db_ip+'" type="text" name="slave_db_ip">')
                print('                                        </div>')

                slave_ssh_port_hint = " Slave ssh port "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave ssh port", slave_ssh_port_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+str(slave_ssh_port)+'" type="text" name="slave_ssh_port">')
                print('                                        </div>')

                slave_server_id_hint = "Slave server id "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave server id", slave_server_id_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+str(slave_server_id)+'" type="text" name="slave_server_id">')
                print('                                        </div>')

                slave_lat_hint = " Slave server latitude "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave latitude", slave_lat_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+str(slave_lat)+'" type="text" name="slave_lat">')
                print('                                        </div>')

                slave_lon_hint = " Slave sever longitude"
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave longitude", slave_lon_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+str(slave_lon)+'" type="text" name="slave_lon">')
                print('                                        </div>')

                slave_repo_hint = " RPM repo "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("RPM repo", slave_repo_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_repo+'" type="text" name="slave_repo">')
                print('                                        </div>')

                slave_dbmode_hint = " MaxScale Mode "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("DBMode", slave_dbmode_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_dbmode+'" type="text" name="slave_dbmode">')
                print('                                        </div>')

                slave_dns_hint = " Slave DNS server "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("DNS", slave_dns_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_dns+'" type="text" name="slave_dns">')
                print('                                        </div>')

                print('                                    <input hidden name="action" value="editslave">')

                print('                                        <button class="btn btn-outline-primary btn-block mt-3" type="submit">Save slave Settings</button>')
                print('                            </form>')

                # Delete the Additional Slave
                print('                            <form class="form toastForm33-wrap" method="post" id="toastForm33-'+str(slave_server_id)+'" onsubmit="return false;">')
                print('                                    <input hidden name="action" value="deleteslave">')
                print('                                    <input hidden name="slave_hostname" value="'+myslave+'">')
                print('                                        <button class="btn btn-outline-primary btn-block mt-3" type="submit">Delete this Slave</button>')
                print('                            </form>')

        print('                         </div>')

        # Add additional Slave
        print('                         <div class="tab-pane fade" id="add-content" role="tabpanel" aria-labelledby="add-tab">')
        print('                            <form class="form" method="post" id="toastForm31" onsubmit="return false;">')

        # slave data
        slave_hostname_hint = " Slaves FQDN "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave server FQDN", slave_hostname_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_hostname">')
        print('                                        </div>')

        slave_main_ip_hint = " Slave Main IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Main IP", slave_main_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_main_ip">')
        print('                                        </div>')

        slave_db_ip_hint = " slaves Database IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Database IP", slave_db_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_db_ip">')
        print('                                        </div>')

        slave_ssh_port_hint = " Slaves ssh port "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave ssh port", slave_ssh_port_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_ssh_port">')
        print('                                        </div>')

        print('                                    <input hidden name="action" value="addadditionalslave">')

        print('                                        <button class="btn btn-outline-primary btn-block mt-4" type="submit">Add New Slave</button>')
        print('                            </form>')
        print('                         </div>')

        # Display, Edit, Delete IPMapping
        print('                         <div class="tab-pane fade" id="ip-content" role="tabpanel" aria-labelledby="ip-tab">')
        master_ip_list = master_data_yaml_parsed[myhostname]['dnsmap'].keys()
        for myip in master_ip_list:
            master_ip_resource = master_data_yaml_parsed[myhostname]['dnsmap'].get(myip)
            # provide public IP for Nat environment
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
            # get corresponding slave IP for this master IP
            mykeypos = 1
            for theslave in cluster_data_yaml_parsed.keys():
                slave_mapped_dns_ip = cluster_data_yaml_parsed[theslave]['dnsmap'].get(myip,"NULL")
                slave_mapped_web_ip = cluster_data_yaml_parsed[theslave]['ipmap'].get(myip,"NULL")
                # Display form for IP address mapping
                print('     <div class="accordion" id="accordionIPs">')
                print('         <div class="card mb-0 text-white dg-dark">')
                print('             <div class="card-header" id="heading'+'-'+str(mykeypos)+'">')
                print('                 <h2 class="mb-0">')
                print('                     <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse'+'-'+str(mykeypos)+'" aria-expanded="false" aria-controls="collapse'+'-'+str(mykeypos)+'">')
                print('                         IP #'+'-'+str(mykeypos)+'')
                print('                     </button>')
                print('                 </h2>')
                print('             </div>')
                print('             <div id="collapse'+'-'+str(mykeypos)+'" class="collapse" aria-labelledby="heading'+'-'+str(mykeypos)+'" data-parent="#accordionIPs">')
                print('                 <div class="card-body">')
                print('                     <form class="form toastForm34-wrap" method="post" id="toastForm34'+'-'+str(mykeypos)+'" onsubmit="return false;">')

                # master data
                master_ip_resource_hint = " IP address resource name like ip1 "

                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Master IP resource name", master_ip_resource_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+master_ip_resource+'" type="text" name="master_ip_resource">')
                print('                                        </div>')

                master_lan_ip_hint = " Masters LAN IP "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Master LAN IP", master_lan_ip_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+myip+'" type="text" name="master_lan_ip">')
                print('                                        </div>')

                master_wan_ip_hint = " Masters WAN IP "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Master WAN IP", master_wan_ip_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+master_ip_resource_actual+'" placeholder="'+master_ip_resource_actual+'" type="text" name="master_wan_ip" readonly>')
                print('                                        </div>')

                # Slave data

                slave_lan_ip_hint = " Slaves LAN IP "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input(theslave, slave_lan_ip_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_mapped_web_ip+'" type="text" name="slave_lan_ip">')
                print('                                        </div>')

                slave_wan_ip_hint = " Slaves WAN IP "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input(theslave, slave_wan_ip_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_mapped_dns_ip+'" type="text" name="slave_wan_ip">')
                print('                                        </div>')

                print('                                    <input hidden name="master_hostname" value="'+myhostname+'">')
                print('                                    <input hidden name="slave_hostname" value="'+theslave+'">')
                print('                                    <input hidden name="action" value="editip">')

                print('                                    <button class="btn btn-outline-primary btn-block mt-3" type="submit">Edit IP resource</button>')
                print('                            </form>')
                print('</div>')
                print('</div>')
                print('</div>')
                print('</div>')
                mykeypos = mykeypos + 1

            # Display form for IP address deletion
            print('                            <form class="form" method="post" id="toastForm35" onsubmit="return false;">')
            print('                                    <input hidden name="master_hostname" value="'+myhostname+'">')
            print('                                    <input hidden name="master_lan_ip" value="'+myip+'">')
            print('                                    <input hidden name="action" value="delip">')
            print('                            <button class="btn btn-outline-danger btn-block mt-3 mb-4" type="submit" form="toastForm35">Delete</button>')

            print('                            </form>')

        print('                          </div>')

        # Display form for IP address mapping add
        print('                         <div class="tab-pane fade" id="ip-add-content" role="tabpanel" aria-labelledby="ip-add-tab">')
        print('                            <form class="form" method="post" id="toastForm36" onsubmit="return false;">')

        # master data
        master_ip_resource_hint = " IP address resource name like ip1 "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master IP resource name", master_ip_resource_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="master_ip_resource">')
        print('                                        </div>')

        master_lan_ip_hint = " Masters LAN IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master LAN IP", master_lan_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="master_lan_ip">')
        print('                                        </div>')

        for theslave in cluster_data_yaml_parsed.keys():
            # Slave data
            slave_lan_ip_hint = " Slaves LAN IP "
            print('                                        <div class="input-group">')
            print('                                            <div class="input-group-prepend input-group-prepend-min">')
            print('                                                <span class="input-group-text">')
            print('                                                    '+return_multi_input("LAN_IP_"+theslave, slave_lan_ip_hint))
            print('                                                </span>')
            print('                                            </div>')
            print('                                            <input class="form-control" value="" type="text" name="'+theslave+'_lan_ip">')
            print('                                        </div>')

            slave_wan_ip_hint = " Slaves WAN IP "
            print('                                        <div class="input-group">')
            print('                                            <div class="input-group-prepend input-group-prepend-min">')
            print('                                                <span class="input-group-text">')
            print('                                                    '+return_multi_input("WAN_IP_"+theslave, slave_wan_ip_hint))
            print('                                                </span>')
            print('                                            </div>')
            print('                                            <input class="form-control" value="" type="text" name="'+theslave+'_wan_ip">')
            print('                                        </div>')

        print('                                    <input hidden name="action" value="addip">')
        print('                                    <input hidden name="master_hostname" value="'+myhostname+'">')
        print('                                        <button class="btn btn-outline-primary btn-block mt-4" type="submit">Add IP Resource</button>')
        print('                            </form>')
        print('                         </div>')

        # home directories
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
                    print('                            <form class="form toastForm37-wrap" method="post" id="toastForm37'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                    print('                                <input hidden name="thehomedir" value="'+path+'">')
                    print('                                <input hidden name="action" value="deletehomedir">')
                    print('                                <button class="btn btn-danger btn-sm" type="submit">')
                    print('                                    <span class="sr-only">Delete</span>')
                    print('                                    <i class="fas fa-times"></i>')
                    print('                                </button>')
                    print('                            </form>')
                    print('                        </div>')
                mykeypos = mykeypos + 1
                print('                        </div>')
        print('                            </div>')
        print('                            <div class="label label-default mt-2 mb-2">Add another \'home\' directory to Unison sync:</div>')
        print('                            <form class="form" method="post" id="toastForm38" onsubmit="return false;">')

        print('                                <div class="input-group mb-0">')
        print('                                    <div class="input-group-prepend input-group-prepend-min">')
        print('                                        <span class="input-group-text">Path</span>')
        print('                                    </div>')
        print('                                    <input class="form-control" placeholder="home2" type="text" name="thehomedir">')
        print('                                    <input hidden name="action" value="addhomedir">')
        print('                                    <div class="input-group-append">')
        print('                                        <button class="btn btn-outline-primary" type="submit">')
        print('                                            <span class="sr-only">Add</span><i class="fas fa-plus"></i>')
        print('                                        </button>')
        print('                                    </div>')
        print('                                </div>')

        print('                            </form>')
        print('                         </div>')

        print('                         </div>')

    print('             </div> <!-- Card Body End -->')

    cardfooter('Only perform a hard reset if the unison archive is corrupt as the unison archive rebuild can be time consuming.')
else:
    cardheader('Setup Cluster', 'fas fa-align-justify')

    print('             <div class="card-body"> <!-- Card Body Start -->')

    # If the inventory file exists
    if os.path.isfile(ansible_inventory_file):
        # parse the inventory and display its contents
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

        print('             <ul class="nav nav-tabs mb-4" id="clusterTabs" role="tablist">')
        print('                 <li class="nav-item"><a class="nav-link active" id="master-tab" data-toggle="tab" href="#master-content" role="tab" aria-controls="master-content" aria-selected="true">Master</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="slave-tab" data-toggle="tab" href="#slave-content" role="tab" aria-controls="slave-content" aria-selected="true">Slaves</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="add-tab" data-toggle="tab" href="#add-content" role="tab" aria-controls="add-content" aria-selected="true">Add Slave</a></li>')
        print('                 <li class="nav-item"><a class="nav-link" id="home-tab" data-toggle="tab" href="#home-content" role="tab" aria-controls="home-content" aria-selected="true">Home Directory</a></li>')
        print('             </ul>')

        # master data
        print('                     <div class="tab-content" id="clusterTabsContent">')
        print('                         <div class="tab-pane fade show active" id="master-content" role="tabpanel" aria-labelledby="master-tab">')
        print('                            <form class="form needs-validation" method="post" id="toastForm29" onsubmit="return false;" novalidate>')

        master_hostname_hint = " Masters FQDN "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master server FQDN", master_hostname_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip01" value="'+master_hostname+'" type="text" name="master_hostname" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        master_main_ip_hint = " Masters Main IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master Main IP", master_main_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip02" value="'+master_main_ip+'" type="text" name="master_main_ip" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        master_db_ip_hint = " Masters Database IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master Database IP", master_db_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip03" value="'+master_db_ip+'" type="text" name="master_db_ip" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        master_ssh_port_hint = " Masters ssh port "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master ssh port", master_ssh_port_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip04" value="'+str(master_ssh_port)+'" type="text" name="master_ssh_port" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        master_server_id_hint = " Masters server id "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master server id", master_server_id_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip05" value="'+str(master_server_id)+'" type="text" name="master_server_id" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        master_lat_hint = " Masters server latitude "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master latitude", master_lat_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip06" value="'+str(master_lat)+'" type="text" name="master_lat" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        master_lon_hint = " Masters severs longitude"
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master longitude", master_lon_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip07" value="'+str(master_lon)+'" type="text" name="master_lon" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        master_repo_hint = " RPM repo "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("RPM repo", master_repo_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+master_repo+'" type="text" name="master_repo" required>')
        print('                                            <div class="invalid-tooltip">You must enter something in '+master_repo+'</div>')
        print('                                        </div>')

        master_dbmode_hint = " MaxScale Mode "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("DBMode", master_dbmode_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" id="validationTooltip08" value="'+master_dbmode+'" type="text" name="master_dbmode" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        master_dns_hint = " Master DNS server "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("DNS", master_dns_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+master_dns+'" type="text" name="master_dns" required>')
        print('                                            <div class="invalid-tooltip">You must enter something here</div>')
        print('                                        </div>')

        print('                                    <input hidden name="action" value="editmaster">')

        print('                                    <button class="btn btn-outline-primary btn-block mt-3" type="submit">Save master Settings</button>')
        print('                            </form>')
        print('                        </div>')

        # slave data
        print('                         <div class="tab-pane fade show" id="slave-content" role="tabpanel" aria-labelledby="slave-tab">')
        print('                            <form class="form" method="post" id="toastForm30" onsubmit="return false;">')

        dbslave_hostname_hint = " Slave FQDN "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave server FQDN", dbslave_hostname_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_hostname+'" type="text" name="dbslave_hostname">')
        print('                                        </div>')

        dbslave_main_ip_hint = " Slaves Main IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Main IP", dbslave_main_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_main_ip+'" type="text" name="dbslave_main_ip">')
        print('                                        </div>')

        dbslave_db_ip_hint = " Slaves Database IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Database IP", dbslave_db_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_db_ip+'" type="text" name="dbslave_db_ip">')
        print('                                        </div>')

        dbslave_ssh_port_hint = " Slaves ssh port "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave ssh port", dbslave_ssh_port_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(dbslave_ssh_port)+'" type="text" name="dbslave_ssh_port">')
        print('                                        </div>')

        dbslave_server_id_hint = " Slaves server id "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave server id", dbslave_server_id_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(dbslave_server_id)+'" type="text" name="dbslave_server_id">')
        print('                                        </div>')

        dbslave_lat_hint = " Slave server latitude "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave latitude", dbslave_lat_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(dbslave_lat)+'" type="text" name="dbslave_lat">')
        print('                                        </div>')

        dbslave_lon_hint = " Slave sever longitude"
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave longitude", dbslave_lon_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+str(dbslave_lon)+'" type="text" name="dbslave_lon">')
        print('                                        </div>')

        dbslave_repo_hint = " RPM repo "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("RPM repo", dbslave_repo_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_repo+'" type="text" name="dbslave_repo">')
        print('                                        </div>')

        dbslave_dbmode_hint = " MaxScale Mode "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("DBMode", dbslave_dbmode_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_dbmode+'" type="text" name="dbslave_dbmode">')
        print('                                        </div>')

        dbslave_dns_hint = " Slave DNS server "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("DNS", dbslave_dns_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+dbslave_dns+'" type="text" name="dbslave_dns">')
        print('                                        </div>')

        print('                                    <input hidden name="action" value="editdbslave">')

        print('                                        <button class="btn btn-outline-primary btn-block mt-3" type="submit">Save slave Settings</button>')
        print('                            </form>')

        # Additional slaves
        for myslave in ansible_inventory_file_parsed['all']['children']['ndeployslaves']['hosts'].keys():
            if myslave != dbslave_hostname:

                print('<div class="accordion mt-4" id="accordionSlaves">')

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
                # slave data
                print('<div class="card mb-0">')
                print('<div class="card-header" id="heading'+str(slave_server_id)+'">')
                print('<h2 class="mb-0">')
                print('<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse'+str(slave_server_id)+'" aria-expanded="false" aria-controls="collapse'+str(slave_server_id)+'">')
                print('Slave #'+str(slave_server_id)+'')
                print('</button>')
                print('</h2>')
                print('</div>')

                print('<div id="collapse'+str(slave_server_id)+'" class="collapse" aria-labelledby="heading'+str(slave_server_id)+'" data-parent="#accordionSlaves">')
                print('<div class="card-body">')
                print('                            <form class="form toastForm32-wrap" method="post" id="toastForm32-'+str(slave_server_id)+'" onsubmit="return false;">')

                slave_hostname_hint = " Slave FQDN "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave server FQDN", slave_hostname_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_hostname+'" type="text" name="slave_hostname">')
                print('                                        </div>')

                slave_main_ip_hint = " Slaves Main IP "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave Main IP", slave_main_ip_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_main_ip+'" type="text" name="slave_main_ip">')
                print('                                        </div>')

                slave_db_ip_hint = " Slaves Database IP "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave Database IP", slave_db_ip_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_db_ip+'" type="text" name="slave_db_ip">')
                print('                                        </div>')

                slave_ssh_port_hint = " Slave ssh port "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave ssh port", slave_ssh_port_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+str(slave_ssh_port)+'" type="text" name="slave_ssh_port">')
                print('                                        </div>')

                slave_server_id_hint = "Slave server id "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave server id", slave_server_id_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+str(slave_server_id)+'" type="text" name="slave_server_id">')
                print('                                        </div>')

                slave_lat_hint = " Slave server latitude "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave latitude", slave_lat_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+str(slave_lat)+'" type="text" name="slave_lat">')
                print('                                        </div>')

                slave_lon_hint = " Slave sever longitude"
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("Slave longitude", slave_lon_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+str(slave_lon)+'" type="text" name="slave_lon">')
                print('                                        </div>')

                slave_repo_hint = " RPM repo "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("RPM repo", slave_repo_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_repo+'" type="text" name="slave_repo">')
                print('                                        </div>')

                slave_dbmode_hint = " MaxScale Mode "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("DBMode", slave_dbmode_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_dbmode+'" type="text" name="slave_dbmode">')
                print('                                        </div>')

                slave_dns_hint = " Slave DNS server "
                print('                                        <div class="input-group">')
                print('                                            <div class="input-group-prepend input-group-prepend-min">')
                print('                                                <span class="input-group-text">')
                print('                                                    '+return_multi_input("DNS", slave_dns_hint))
                print('                                                </span>')
                print('                                            </div>')
                print('                                            <input class="form-control" value="'+slave_dns+'" type="text" name="slave_dns">')
                print('                                        </div>')

                print('                                    <input hidden name="action" value="editslave">')

                print('                            </form>')

                # Delete the Additional Slave
                print('                            <form class="form toastForm33-wrap" method="post" id="toastForm33-'+str(slave_server_id)+'" onsubmit="return false;">')
                print('                                    <input hidden name="action" value="deleteslave">')
                print('                                    <input hidden name="slave_hostname" value="'+myslave+'">')
                print('                            </form>')
                print('                            <div class="btn-group btn-block mt-3">')
                print('                                <button class="btn btn-outline-primary btn-block" type="submit" form="toastForm32-'+str(slave_server_id)+'">Save slave Settings</button>')
                print('                                <button class="btn btn-outline-danger btn-block" type="submit" form="toastForm33-'+str(slave_server_id)+'">Delete this Slave</button>')
                print('                            </div>')

                print('</div>')
                print('</div>')
                print('</div>')
                print('                         </div>')
        print('</div>')


        # Add additional Slave
        print('                         <div class="tab-pane fade show" id="add-content" role="tabpanel" aria-labelledby="add-tab">')
        print('                            <form class="form" method="post" id="toastForm31" onsubmit="return false;">')

        # slave data
        slave_hostname_hint = " Slaves FQDN "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave server FQDN", slave_hostname_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_hostname">')
        print('                                        </div>')

        slave_main_ip_hint = " Slave Main IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Main IP", slave_main_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_main_ip">')
        print('                                        </div>')

        slave_db_ip_hint = " slaves Database IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Database IP", slave_db_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_db_ip">')
        print('                                        </div>')

        slave_ssh_port_hint = " Slaves ssh port "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave ssh port", slave_ssh_port_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_ssh_port">')
        print('                                        </div>')

        print('                                    <input hidden name="action" value="addadditionalslave">')

        print('                                        <button class="btn btn-outline-primary btn-block mt-3" type="submit">Add New Slave</button>')
        print('                            </form>')
        print('                         </div>')

        # home directories
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
                    print('                            <form class="form toastForm37-wrap" method="post" id="toastForm37'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                    print('                                <input hidden name="thehomedir" value="'+path+'">')
                    print('                                <input hidden name="action" value="deletehomedir">')
                    print('                                <button class="btn btn-danger btn-sm" type="submit">')
                    print('                                    <span class="sr-only">Delete</span>')
                    print('                                    <i class="fas fa-times"></i>')
                    print('                                </button>')
                    print('                            </form>')
                    print('                        </div>')
                mykeypos = mykeypos + 1
                print('                        </div>')
        print('                            </div>')
        print('                            <div class="label label-default mt-2 mb-2">Add another \'home\' directory to Unison sync:</div>')
        print('                            <form class="form" method="post" id="toastForm38" onsubmit="return false;">')

        print('                                <div class="input-group mb-0">')
        print('                                    <div class="input-group-prepend input-group-prepend-min">')
        print('                                        <span class="input-group-text">Path</span>')
        print('                                    </div>')
        print('                                    <input class="form-control" placeholder="home2" type="text" name="thehomedir">')
        print('                                    <input hidden name="action" value="addhomedir">')
        print('                                    <div class="input-group-append">')
        print('                                        <button class="btn btn-outline-primary" type="submit">')
        print('                                            <span class="sr-only">Add</span><i class="fas fa-plus"></i>')
        print('                                        </button>')
        print('                                    </div>')
        print('                                </div>')

        print('                            </form>')
        print('                         </div>')
        print('                         </div>')
    else:
        # Get the server main IP
        myip = get('https://api.ipify.org').text
        # Display form for ndeploymaster
        print('                            <form class="form" method="post" id="toastForm28" onsubmit="return false;">')

        # master data

        master_hostname_hint = " Masters FQDN "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master server FQDN", master_hostname_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+myhostname+'" type="text" name="master_hostname">')
        print('                                        </div>')

        master_main_ip_hint = " Masters Main IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master Main IP", master_main_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+myip+'" type="text" name="master_main_ip">')
        print('                                        </div>')

        master_db_ip_hint = " Masters Database IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master Database IP", master_db_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="'+myip+'" type="text" name="master_db_ip">')
        print('                                        </div>')

        master_ssh_port_hint = " Masters ssh port "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Master ssh port", master_ssh_port_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="master_ssh_port">')
        print('                                        </div>')

        # slave data
        slave_hostname_hint = " Slaves FQDN "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave server FQDN", slave_hostname_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_hostname">')
        print('                                        </div>')

        slave_main_ip_hint = " Slave Main IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Main IP", slave_main_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_main_ip">')
        print('                                        </div>')

        slave_db_ip_hint = " slaves Database IP "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave Database IP", slave_db_ip_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_db_ip">')
        print('                                        </div>')

        slave_ssh_port_hint = " Slaves ssh port "
        print('                                        <div class="input-group">')
        print('                                            <div class="input-group-prepend input-group-prepend-min">')
        print('                                                <span class="input-group-text">')
        print('                                                    '+return_multi_input("Slave ssh port", slave_ssh_port_hint))
        print('                                                </span>')
        print('                                            </div>')
        print('                                            <input class="form-control" value="" type="text" name="slave_ssh_port">')
        print('                                        </div>')

        print('                                    <input hidden name="action" value="setup">')

        print('                                        <button class="btn btn-outline-primary btn-block mt-3" type="submit">Save cluster Settings</button>')
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
    cardheader('Sync Cluster','fas fa-sync')
    print('             <div class="card-body"> <!-- Card Body Start -->')

    print('                 <form class="form mb-3" id="toastForm27" onsubmit="return false;">')
    print('                     <div class="input-group">')
    print('                         <div class="input-group-prepend input-group-prepend-min">')
    print('                             <label class="input-group-text">Files</label>')
    print('                         </div>')
    print('                         <select name="user" class="custom-select">')
    user_list = os.listdir("/var/cpanel/users")
    for cpuser in sorted(user_list):
        if cpuser != 'nobody' and cpuser != 'system':
            print('                     <option value="'+cpuser+'">'+cpuser+'</option>')
    print('                         </select>')
    print('                     </div>')
    print('                     <button type="submit" class="btn btn-outline-primary btn-block mt-4">Sync web files</button>')
    print('                 </form>')

    print('                 <form class="form" id="toastForm7" onsubmit="return false;">')
    print('                     <div class="input-group">')
    print('                         <div class="input-group-prepend input-group-prepend-min">')
    print('                             <label class="input-group-text">Zone</label>')
    print('                         </div>')
    print('                         <select name="user" class="custom-select">')
    user_list = os.listdir("/var/cpanel/users")
    for cpuser in sorted(user_list):
        if cpuser != 'nobody' and cpuser != 'system':
            print('                     <option value="'+cpuser+'">'+cpuser+'</option>')
    print('                         </select>')
    print('                     </div>')
    print('                     <button type="submit" class="btn btn-outline-primary btn-block mt-4">Sync GeoDNS Zone</button>')
    print('                 </form>')

    print('             </div> <!-- Card Body End -->')
    cardfooter('Choose a user to sync dns zone or web files')
else:
    cardheader('Cluster Sync Disabled','fas fa-sync')
    cardfooter('Cluster Sync is only available when cluster is setup')

print('                </div> <!-- End Sync Tab -->')

# PHP Tab
print('')
print('                <!-- PHP Tab -->')
print('                <div class="tab-pane fade" id="v-pills-php" role="tabpanel" aria-labelledby="v-pills-php-tab">')

# Set Default PHP for AutoConfig
cardheader('Default PHP for Autoswitch','fab fa-php')
print('                 <div class="card-body p-0">  <!-- Card Body Start -->')
print('                     <div class="row no-gutters row-1"> <!-- Row Start -->')

# Check if we have a Preferred PHP and allow selection.
if os.path.isfile(installation_path+"/conf/preferred_php.yaml"):
    preferred_php_yaml = open(installation_path+"/conf/preferred_php.yaml", 'r')
    preferred_php_yaml_parsed = yaml.safe_load(preferred_php_yaml)
    preferred_php_yaml.close()
    phpversion = preferred_php_yaml_parsed.get('PHP')
    myphpversion = phpversion.keys()[0]
else:
    myphpversion = "Unset"
print('                         <div class="col-md-6 alert"><i class="fab fa-php"></i> Default PHP</div>')
print('                         <div class="col-md-6 alert text-success">'+myphpversion+' <i class="fa fa-check-circle"></i></div>')
print('                     </div>')
print('                 </div> <!-- Card Body End -->')

backend_config_file = installation_path+"/conf/backends.yaml"
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()

if "PHP" in backend_data_yaml_parsed:
    print('             <div class="card-body"> <!-- Card Body Start -->')
    print('                 <form class="form" id="toastForm6" onsubmit="return false;">')
    print('                     <div class="input-group">')
    print('                         <div class="input-group-prepend input-group-prepend-min">')
    print('                             <label class="input-group-text">PHP</label>')
    print('                         </div>')
    print('                         <select name="phpversion" class="custom-select">')

    php_backends_dict = backend_data_yaml_parsed["PHP"]
    for versions_defined in list(php_backends_dict.keys()):
        if versions_defined == myphpversion:
            print('                     <option selected value="'+myphpversion+'">'+myphpversion+'</option>')
        else:
            print('                     <option value="'+versions_defined+'">'+versions_defined+'</option>')
    print('                         </select>')
    print('                     </div>')
    print('                     <button type="submit" class="btn btn-outline-primary btn-block mt-4">Set Default PHP</button>')
    print('                 </form>')
    print('             </div> <!-- Card Body End -->')
cardfooter('Automatic switch to Nginx will use versions set in MultiPHP or if MultiPHP is not used the phpversion above')

print('                </div> <!-- End PHP Tab -->')

# DOS Tab
print('')
print('                <!-- DOS Tab -->')
print('                <div class="tab-pane fade" id="v-pills-dos" role="tabpanel" aria-labelledby="v-pills-dos-tab">')

# DDOS Protection
cardheader('DDOS Protection','fas fa-user-shield')
print('                 <div class="card-body p-0">  <!-- Card Body Start -->')
print('                     <div class="row no-gutters row-2-col row-no-btm"> <!-- Row Start -->')
print('                         <div class="col-md-6 alert"><i class="fas fa-shield-alt"></i> Nginx</div>')
print('                         <div class="col-md-6">')
print('                             <div class="row no-gutters">')

if os.path.isfile('/etc/nginx/conf.d/dos_mitigate_systemwide.enabled'):
    print('                             <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
    print('                             <div class="col-9">')
    print('                                 <form id="toastForm1" class="form" onsubmit="return false;">')
    print('                                     <button type="submit" class="alert btn btn-secondary">Disable</button>')
    print('                                     <input hidden name="ddos" value="disable">')
else:
    print('                             <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
    print('                             <div class="col-9">')
    print('                                 <form id="toastForm1" class="form" onsubmit="return false;">')
    print('                                     <button type="submit" class="alert btn btn-secondary">Enable</button>')
    print('                                     <input hidden name="ddos" value="enable">')

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
        print('                             <form id="toastForm2" class="form" onsubmit="return false;">')
        print('                                 <button type="submit" class="alert btn btn-secondary">Disable</button>')
        print('                                 <input hidden name="ddos" value="disable">')
    else:
        print('                         <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
        print('                         <div class="col-9">')
        print('                             <form id="toastForm2" class="form" onsubmit="return false;">')
        print('                                 <button type="submit" class="alert btn btn-secondary">Enable</button>')
        print('                                 <input hidden name="ddos" value="enable">')

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
cardheader('PHP-FPM Pool Editor','fas fa-sitemap')
print('                 <div class="card-body"> <!-- Card Body Start -->')
print('                     <form class="form" action="phpfpm_pool_editor.cgi" method="get">')
print('                         <div class="input-group">')
print('                             <div class="input-group-prepend input-group-prepend-min">')
print('                                 <span class="input-group-text">')
print('                                     '+return_prepend("cPanel User", phpfpmpool_hint))
print('                                 </span>')
print('                             </div>')
print('                             <select name="poolfile" class="custom-select">')
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
    print('                     <input hidden name="section" value="1">')
else:
    print('                     <input hidden name="section" value="0">')
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
cardheader('Map cPanel Package to NGINX','fas fa-box-open')
print('                 <div class="card-body p-0"> <!-- Card Body Start -->')
print('                     <div class="row no-gutters row-1"> <!-- Row Start -->')
print('                         <div class="col-md-6 alert"><i class="fas fa-box"></i> NGINX -> Package</div>')
print('                         <div class="col-md-6">')
print('                             <div class="row no-gutters">')

if os.path.isfile(installation_path+'/conf/lock_domaindata_to_package'):
    print('                             <div class="col-3 alert text-success"><i class="fas fa-check-circle"><span class="sr-only sr-only-focusable">Enabled</span></i></div>')
    print('                             <div class="col-9">')
    print('                                 <form class="form" method="post" id="toastForm16" onsubmit="return false;">')
    print('                                     <button type="submit" class="alert btn btn-secondary">Disable</button>')
    print('                                     <input hidden name="package_lock" value="disabled">')
    print('                                 </form>')
    print('                             </div>')
    print('                         </div>')
else:
    print('                         <div class="col-3 alert text-secondary"><i class="fas fa-times-circle"><span class="sr-only sr-only-focusable">Disabled</span></i></div>')
    print('                             <div class="col-9">')
    print('                                 <form class="form" method="post" id="toastForm16" onsubmit="return false;">')
    print('                                     <button type="submit" class="alert btn btn-secondary">Enable</button>')
    print('                                     <input hidden name="package_lock" value="enabled">')
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
print('                                 <span class="input-group-text">')
print('                                     '+return_prepend("cPanel Package", cpanpackage_hint))
print('                                 </span>')
print('                             </div>')
print('                             <select name="cpanelpkg" class="custom-select">')

for thepkg in sorted(mypkgs.get('package')):
    pkgname = thepkg.get('name').encode('utf-8').replace(' ', '_')
    print('                             <option value="'+pkgname+'">'+pkgname+'</option>')

print('                             </select>')
print('                         </div>')
print('                         <button class="btn btn-outline-primary btn-block mt-4" type="submit">Edit Pkg</button>')
print('                     </form>')
print('                 </div> <!-- Card Body End -->')
cardfooter('This option will automatically assign NGINX Config/Settings to a cPanel Package when enabled. This will also reset any NGINX Config/Settings the user has configured if the cPanel Package undergoes an Upgrade/Downgrade process.'
)

print('                </div> <!-- End Map Tab -->')

# Limit Tab
print('')
print('                <!-- Limit Tab -->')
print('                <div class="tab-pane fade" id="v-pills-limit" role="tabpanel" aria-labelledby="v-pills-limit-tab">')

# System Resource Limit
cardheader('System Resource Limit','fas fa-compress')
print('                    <div class="card-body"> <!-- Card Body Start -->')

with open('/etc/redhat-release', 'r') as releasefile:
    osrelease = releasefile.read().split(' ')[0]
if not osrelease == 'CloudLinux':
    if os.path.isfile('/usr/bin/systemctl'):

        # Next sub-section start here
        if os.path.isfile(installation_path+"/conf/secure-php-enabled"):  # if per user php-fpm master process is set
            userlist = os.listdir("/var/cpanel/users")
            print('         <form class="form" action="resource_limit.cgi" method="get">')
            print('             <div class="input-group">')
            print('                 <div class="input-group-prepend input-group-prepend-min">')
            print('                     <label class="input-group-text">User</label>')
            print('                 </div>')
            print('                 <select name="unit" class="custom-select">')

            for cpuser in sorted(userlist):
                if cpuser != 'nobody' and cpuser != 'system':
                    print('             <option value="'+cpuser+'">'+cpuser+'</option>')

            print('                 </select>')
            print('                 <input hidden name="mode" value="user">')
            print('             </div>')
            print('             <button class="btn btn-outline-primary btn-block mt-4" type="submit">Set Limit</button>')
            print('         </form>')

            print('         <form class="form mt-4" action="resource_limit.cgi" method="get">')
            print('             <div class="input-group">')
            print('                 <div class="input-group-prepend input-group-prepend-min">')
            print('                     <label class="input-group-text">Service</label>')
            print('                 </div>')
            print('                 <select name="unit" class="custom-select">')

            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm", "ea-php73-php-fpm":
                print('                 <option value="'+service+'">'+service+'</option>')

            print('                 </select>')
            print('                 <input hidden name="mode" value="service">')
            print('             </div>')
            print('             <button class="btn btn-outline-primary btn-block mt-4" type="submit">Set Limit</button>')
            print('         </form>')
        else:
            print('         <form class="form" action="resource_limit.cgi" method="get">')
            print('             <div class="input-group">')
            print('                 <div class="input-group-prepend input-group-prepend-min">')
            print('                     <label class="input-group-text">Resource</label>')
            print('                 </div>')
            print('                 <select name="unit" class="custom-select">')

            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm", "ea-php73-php-fpm":
                print('                 <option value="'+service+'">'+service+'</option>')

            print('                  </select>')
            print('                  <input hidden name="mode" value="service">')
            print('              </div>')
            print('              <button class="btn btn-outline-primary btn-block mt-4" type="submit">Set Limit</button>')
            print('          </form>')
print('                  </div> <!-- Card Body End -->')
cardfooter('BlockIOWeight range is 10-1000, CPUShares range is 0-1024, MemoryLimit range is calculated using available memory')

print('              </div> <!-- End Limit Tab -->')
print('          </div>')
print('      </div> <!-- End WHM Tabs Row -->')

print_footer()

print(' </div> <!-- Main Container End -->')
print('')

print_modals()
print_loader()

print('</body> <!-- Body End -->')
print('</html>')
