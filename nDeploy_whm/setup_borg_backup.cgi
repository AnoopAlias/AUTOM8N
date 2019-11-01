#!/usr/bin/python

import cgi
import cgitb
import subprocess
import os
import yaml
import platform
import psutil
import signal
import jinja2
import codecs
import sys
import json
from commoninclude import return_label, return_multi_input, bcrumb, print_header, display_term, print_modals, print_loader, cardheader, cardfooter

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backup_config_file = "/opt/nDeploy/conf/backup_config.yaml"
borgmatic_config_file = "/etc/borgmatic/config.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_header('BorgBackup Configuration')
bcrumb('BorgBackup Configuration', 'fas fa-database')

if os.path.isdir('/etc/borgmatic'):

    # Check if backup config file is present or initilize otherwise
    if os.path.isfile(backup_config_file):

        # Get all config settings from the backup config file
        with open(backup_config_file, 'r') as backup_config_file_stream:
            yaml_parsed_backupyaml = yaml.safe_load(backup_config_file_stream)

        # Backup settings
        pkgacct_backup = yaml_parsed_backupyaml.get('pkgacct_backup', 'enabled')
        system_files = yaml_parsed_backupyaml.get('system_files', 'enabled')
        mysql_backup = yaml_parsed_backupyaml.get('mysql_backup', 'enabled')
        backup_path = yaml_parsed_backupyaml.get('backup_path', '/backup')
    else:
        pkgacct_backup = "enabled"
        system_files = "enabled"
        mysql_backup = "enabled"
        backup_path = "/backup"
        backup_config_dict = {"pkgacct_backup": "enabled", "system_files": "enabled", "mysql_backup": "enabled", "backup_path": "/backup"}
        with open(backup_config_file, 'w') as backup_config_file_stream:
            yaml.dump(backup_config_dict, backup_config_file_stream, default_flow_style=False)
    if not os.path.isfile('/opt/nDeploy/scripts/borgmatic_cpanel_backup_hook.sh'):

        # We create the borgmatic hook now
        # Initiate Jinja2 templateEnv
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        templateVars = {"BACKUP_PATH": backup_path,
                        "PKGACCT_BACKUP": pkgacct_backup,
                        "SYSTEM_FILES": system_files,
                        "MYSQL_BACKUP": mysql_backup
                        }
        borgmatic_hook_template = templateEnv.get_template("borgmatic_cpanel_backup_hook.sh.j2")
        borgmatic_hook_script = borgmatic_hook_template.render(templateVars)
        with codecs.open('/opt/nDeploy/scripts/borgmatic_cpanel_backup_hook.sh', 'w', 'utf-8') as borgmatic_hook_myscript:
            borgmatic_hook_myscript.write(borgmatic_hook_script)
        os.chmod("/opt/nDeploy/scripts/borgmatic_cpanel_backup_hook.sh", 0o755)

    print('            <!-- WHM Tabs Row -->')
    print('            <div class="row justify-content-lg-center flex-nowrap">')
    print('')
    print('                <!-- Secondary Navigation -->')
    print('                <div class="pl-3 col-md-3 nav flex-column nav-pills d-none d-lg-block d-xl-block d-xs-none d-sm-none" id="v-pills-tab" role="tablist" aria-orientation="vertical">')
    print('                    <a class="nav-link active" id="v-pills-configure-tab" data-toggle="pill" href="#v-pills-configure" role="tab" aria-controls="v-pills-configure-tab">Backup Configuration</a>')
    print('                    <a class="nav-link" id="v-pills-additional-tab" data-toggle="pill" href="#v-pills-additional" role="tab" aria-controls="v-pills-additional">Additional Directories</a>')
    print('                    <a class="nav-link" id="v-pills-settings-tab" data-toggle="pill" href="#v-pills-settings" role="tab" aria-controls="v-pills-settings">Settings</a>')
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
    print('                            <a class="dropdown-item" id="v-pills-configure-tab" data-toggle="pill" href="#v-pills-configure" role="tab" aria-controls="v-pills-configure-tab" aria-selected="false">Backup Configuration</a>')
    print('                            <a class="dropdown-item" id="v-pills-additional-tab" data-toggle="pill" href="#v-pills-additional" role="tab" aria-controls="v-pills-additional" aria-selected="false">Additional Directories</a>')
    print('                            <a class="dropdown-item" id="v-pills-settings-tab" data-toggle="pill" href="#v-pills-settings" role="tab" aria-controls="v-pills-settings" aria-selected="false">Settings</a>')
    print('                        </div>')
    print('                    </div>')

    print('')
    print('                    <!-- Configure Tab -->')
    print('                    <div class="tab-pane fade show active" id="v-pills-configure" role="tabpanel" aria-labelledby="v-pills-configure-tab">')

    # System Status
    cardheader('Borg Backup Settings', 'fas fa-database')
    print('                        <div class="card-body"> <!-- Card Body Start -->')

    print('                            <form class="form" method="post" id="save_backup_settings" onsubmit="return false;">')
    print('                                <div class="row align-items-center row-btn-group-toggle"> <!-- Row Start -->')

    # system_files
    system_files_hint = " Enable to backup the cPanel system files. "
    print('                                    '+return_label("System Files", system_files_hint))
    print('                                    <div class="col-md-6">')
    print('                                        <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')

    if system_files == 'enabled':
        print('                                            <label class="btn btn-light active">')
        print('                                                <input type="radio" name="system_files" value="enabled" id="BuFilesOn" autocomplete="off" checked> Enabled')
        print('                                            </label>')
        print('                                            <label class="btn btn-light">')
        print('                                                <input type="radio" name="system_files" value="disabled" id="BuFilesOff" autocomplete="off"> Disabled')
    else:
        print('                                            <label class="btn btn-light">')
        print('                                                <input type="radio" name="system_files" value="enabled" id="BuFilesOn" autocomplete="off"> Enabled')
        print('                                            </label>')
        print('                                            <label class="btn btn-light active">')
        print('                                                <input type="radio" name="system_files" value="disabled" id="BuFilesOff" autocomplete="off" checked> Disabled')

    print('                                            </label>')
    print('                                        </div>')
    print('                                    </div>')

    # mysql_backup
    mysql_backup_hint = " Enable MariaBackup to backup the FULL MySQL data directory. "
    print('                                    '+return_label("Maria Backup", mysql_backup_hint))
    print('                                    <div class="col-md-6">')
    print('                                        <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')

    if mysql_backup == 'enabled':
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="mysql_backup" value="enabled" id="BuDataOn" autocomplete="off" checked> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="mysql_backup" value="disabled" id="BuDataOff" autocomplete="off"> Disabled')
    else:
        print('                                        <label class="btn btn-light">')
        print('                                            <input type="radio" name="mysql_backup" value="enabled" id="BuDataOn" autocomplete="off"> Enabled')
        print('                                        </label>')
        print('                                        <label class="btn btn-light active">')
        print('                                            <input type="radio" name="mysql_backup" value="disabled" id="BuDataOff" autocomplete="off" checked> Disabled')

    print('                                            </label>')
    print('                                        </div>')
    print('                                    </div>')

    # backup_path
    backup_path_hint = " The directory where the cPanel package accounts, SQL backups, and system files are stored. "
    print('                                    <div class="col-md-12">')
    print('                                        <div class="input-group mt-2 mb-2">')
    print('                                            <div class="input-group-prepend">')
    print('                                                <span class="input-group-text">')
    print('                                                    '+return_multi_input("PKGacct Backup Path", backup_path_hint))
    print('                                                </span>')
    print('                                            </div>')
    print('                                            <input class="form-control" value="'+backup_path+'" type="text" name="backup_path">')
    print('                                        </div>')
    print('                                    </div>')
    print('                                    <div class="col-md-12">')
    print('                                        <button id="save_backup_settings_btn" class="btn btn-outline-primary btn-block mt-3" type="submit">Save Backup Settings</button>')
    print('                                    </div>')
    print('                                </div> <!-- Row End -->')
    print('                            </form>')
    print('                        </div> <!-- Card Body End -->')
    cardfooter('Configure the Borg backup settings to control what content is backed up, and at what location to create the backups.')

    # Check if borgmatic config file is present or initilize otherwise
    if not os.path.isfile(borgmatic_config_file):

        # We create the borgmatic config now
        # Initiate Jinja2 templateEnv
        templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        templateVars = {"BACKUP_PATH": backup_path}
        borgmatic_conf_template = templateEnv.get_template("borgmatic_sample_config.yaml.j2")
        borgmatic_conf = borgmatic_conf_template.render(templateVars)
        with codecs.open(borgmatic_config_file, 'w', 'utf-8') as borgmatic_conf_file:
            borgmatic_conf_file.write(borgmatic_conf)
        os.chmod(borgmatic_config_file, 0o640)

    # Since we have a borgmatic config now, let's load it up and present to the user
    if os.path.isfile(borgmatic_config_file):

        # Get all config settings from the borgmatic config file
        with open(borgmatic_config_file, 'r') as borgmatic_config_file_stream:
            yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_config_file_stream)

    # List backup and allow restore
    if os.path.isfile('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE'):
        if not os.path.exists('/root/borg_restore_point'):
            os.makedirs('/root/borg_restore_point')

        cardheader('Restore Points', 'fas fa-database')
        print('                    <div class="card-body"> <!-- Card Body Start -->')

        if os.path.ismount('/root/borg_restore_point'):
            with open('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE', 'r') as restore_point_conf:
                yaml_parsed_restorepoint = yaml.safe_load(restore_point_conf)
            restore_point = yaml_parsed_restorepoint.get('restore_point', 'snapshot')
            print('                    <p class="text-center">currently mounted</p><hr>'+restore_point)
            print('                    <form class="form mb-3" id="toastForm24" onsubmit="return false;">')
            print('                        <input hidden name="action" value="umount">')
            print('                        <button type="submit" class="btn btn-outline-primary btn-block ">Umount Restore Point</button>')
            print('                    </form>')
            mount_flag = True
        else:
            mount_flag = False
        proc = subprocess.Popen('borgmatic --list --json', shell=True, stdout=subprocess.PIPE)
        try:
            output = json.loads(proc.stdout.read())
        except ValueError, e:
            pass
        else:
            myarchives = output[0].get('archives')
            if myarchives:
                mykeypos = 1
                print('                <div class="input-group">')
                print('                    <select name="myarchives" class="custom-select">')
                for backup in myarchives:
                    print('                    <option selected value="'+backup.get('archive')+'">'+backup.get('archive')+'</option>')
                print('                    </select>')
                if not mount_flag:
                    print('                <div class="input-group-append">')
                    print('                    <form class="m-0 toastForm25-wrap" id="toastForm25'+'-'+str(mykeypos)+'"  method="post" onsubmit="return false;">')
                    print('                        <input hidden name="restorepoint" value="'+backup.get('archive')+'">')
                    print('                        <input hidden name="action" value="mount">')
                    print('                        <button class="btn btn-outline-primary btn-block" type="submit">Mount <i class="fas fa-upload"></i></button>')
                    print('                    </form>')
                    print('                </div>')
                    mykeypos = mykeypos + 1
                print('                </div>')

        print('                    </div> <!-- Card Body End -->')
        cardfooter('Mount point: <kbd>/root/borg_restore_point</kbd>')

    print('                    </div> <!-- Configure Tab End -->')

    print('                    <!-- Additional Directories Tab -->')
    print('                    <div class="tab-pane fade show" id="v-pills-additional" role="tabpanel" aria-labelledby="v-pills-additional-tab">')

    cardheader('Additional \'home\' Directory Backup', 'fas fa-database')
    print('                        <div class="card-body"> <!-- Card Body Start -->')

    # backup directories
    backup_dir_list = yaml_parsed_borgmaticyaml['location']['source_directories']

    if backup_dir_list:
        print('                        <div class="label label-default mb-2">Currently backing up:</div>')
        print('                        <div class="clearfix">')
        mykeypos = 1
        for path in backup_dir_list:
            print('                        <div class="input-group input-group-inline input-group-sm">')
            print('                            <div class="input-group-prepend">')
            print('                                <span class="input-group-text">'+path+'</span>')
            print('                            </div>')
            if path not in ['/home', backup_path]:
                print('                        <div class="input-group-append">')
                print('                            <form class="form borg-rm-dir-wrap" method="post" id="borg_rm_dir-'+str(mykeypos)+'" onsubmit="return false;">')
                print('                                <input hidden name="thehomedir" value="'+path+'">')
                print('                                <input hidden name="action" value="delete">')
                print('                                <button id="borg_rm_dir_btn-'+str(mykeypos)+'" class="btn btn-danger btn-sm" type="submit">')
                print('                                    <span class="sr-only">Delete</span>')
                print('                                    <i class="fas fa-times"></i>')
                print('                                </button>')
                print('                            </form>')
                print('                        </div>')
            mykeypos = mykeypos + 1
            print('                        </div>')
    print('                            </div>')
    print('                            <div class="label label-default mt-2 mb-2">Add another \'home\' directory to backup:</div>')
    print('                            <form class="form" method="post" id="borg_add_dir" onsubmit="return false;">')

    print('                                <div class="input-group mb-0">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">Path</span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="/home2" type="text" name="thehomedir">')
    print('                                    <input hidden name="action" value="add">')
    print('                                    <div class="input-group-append">')
    print('                                        <button id="borg_add_dir_btn" class="btn btn-outline-primary" type="submit">')
    print('                                            <span class="sr-only">Add</span><i class="fas fa-plus"></i>')
    print('                                        </button>')
    print('                                    </div>')
    print('                                </div>')

    print('                            </form>')
    print('                        </div> <!-- Card Body End -->')
    cardfooter('Configure additional \'home\' directories that you would like to backup.')

    print('                    </div> <!-- Additional Directories Tab End -->')

    print('                    <!-- Settings Tab -->')
    print('                    <div class="tab-pane fade show" id="v-pills-settings" role="tabpanel" aria-labelledby="v-pills-settings-tab">')

    cardheader('Borg Settings', 'fas fa-database')
    print('                        <div class="card-body"> <!-- Card Body Start -->')
    print('                            <form class="form input-group-prepend-min" method="post" id="toastForm12" onsubmit="return false;"> ')

    # repositories
    repositories_hint = " Eg: user@backupserver:sourcehostname.borg "
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("Repositories", repositories_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" value="'+yaml_parsed_borgmaticyaml['location']['repositories'][0]+'" type="text" name="repositories">')
    print('                                </div>')

    # ssh_command
    ssh_command_hint = " Enter additional options for SSH. "
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("SSH Command", ssh_command_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" value="'+yaml_parsed_borgmaticyaml['storage']['ssh_command']+'" type="text" name="ssh_command">')
    print('                                </div>')

    # encryption_passphrase
    encryption_passphrase_hint = " Enter your passphrase used to encrypt the backup. "
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("Passphrase", encryption_passphrase_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" value="'+yaml_parsed_borgmaticyaml['storage']['encryption_passphrase']+'" type="text" name="encryption_passphrase">')
    print('                                </div>')

    # remote_rate_limit
    remote_rate_limit_hint = " Set the network upload rate limit in KB/s. "
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("Remote Rate Limit", remote_rate_limit_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['storage']['remote_rate_limit'])+'" type="text" name="remote_rate_limit">')
    print('                                </div>')

    # retention
    print('                                <label class="label mt-2 mb-2">Backup Retention</label>')

    # keep_hourly
    keep_hourly_hint = " Enter the number of hourly backups to keep. "
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("Hourly Keep", keep_hourly_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['retention']['keep_hourly'])+'" type="text" name="keep_hourly">')
    print('                                </div>')

    # keep_daily
    keep_daily_hint = " Enter the number of daily backups to keep. "
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("Daily Keep", keep_daily_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['retention']['keep_daily'])+'" type="text" name="keep_daily">')
    print('                                </div>')

    # keep_weekly
    keep_weekly_hint = " Enter the number of weekly backups to keep. "
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("Weekly Keep", keep_weekly_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['retention']['keep_weekly'])+'" type="text" name="keep_weekly">')
    print('                                </div>')

    # keep_monthly
    keep_monthly_hint = " Enter the number of monthly backups to keep. "
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("Monthly Keep", keep_monthly_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['retention']['keep_monthly'])+'" type="text" name="keep_monthly">')
    print('                                </div>')

    print('                            </form>')
    print('                            <form class="form" id="modalForm5" onsubmit="return false;">')
    print('                                <input hidden name="action" value="initrepo">')
    print('                            </form>')

    print('                            <div class="btn-group btn-block mt-2">')
    print('                                <button class="btn btn-outline-primary" type="submit" form="toastForm12">Init Repo</button>')
    print('                                <button class="btn btn-outline-primary" type="submit" form="modalForm5">Save Settings</button>')
    print('                            </div>')

    print('                        </div> <!-- Card Body End -->')
    cardfooter('Keep your encryption passphrase in a safe place as losing it would make data recovery impossible on a server crash. <br>Repositories must be either a local folder: <kbd>/mnt/backup</kbd> or a SSH URI: <kbd>ssh://user@backupserver.com:22/home/user/backup</kbd>')

else:
    cardheader('Install and Setup BorgBackup')
    print('                        <div class="card-body text-center p-4"> <!-- Card Body Start -->')
    print('                            <p>BorgBackup (short: Borg) is a deduplicating backup program. Optionally, it supports compression and authenticated encryption. The main goal of Borg is to provide an efficient and secure way to backup data. The data deduplication technique used makes Borg suitable for daily backups since only changes are stored. The authenticated encryption technique makes it suitable for backups to not fully trusted targets. <em>Would you like to install and setup BorgBackup?</em></p>')
    print('                            <form class="form" id="install_borg" onsubmit="return false;">')
    print('                                <input hidden name="action" value="installborg">')
    print('                                <button id="install_borg_btn" class="btn btn-outline-primary btn-block">Install</button>')
    print('                            </form>')
    print('                        </div> <!-- Card Body End -->')
    cardfooter('')

    print('                    </div> <!-- Settings Tab End -->')

    print('                </div><!-- Container Tabs End -->')
    print('            </div><!-- WHM Row End -->')

print('            </div>')

print('        </div> <!-- Main Container End -->')

display_term()

print('')

print_modals()

print('    </body> <!-- Body End -->')
print('</html>')
