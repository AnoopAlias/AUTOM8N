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
from commoninclude import return_red, return_green, return_multi_input, bcrumb, print_header, print_modals, print_loader, cardheader, cardfooter

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backup_config_file = "/opt/nDeploy/conf/backup_config.yaml"
borgmatic_config_file = "/etc/borgmatic/config.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_header('Borg Backup Configuration')
bcrumb('Borg Backup Configuration','fas fa-database')
print('            <!-- WHM Starter Row -->')
print('            <div class="row justify-content-lg-center">')
print('                <!-- First Column Start -->')
print('                <div class="col-lg-6">') #Column
print('')


# System Status
cardheader('Borg Backup Settings','fas fa-database')
print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
print('                            <div class="row no-gutters"> <!-- Row Start -->') #Row Start

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
        backup_path = yaml_parsed_backupyaml.get('backup_path','/backup')
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

    print('                                <form class="form" method="post" id="toastForm11" onsubmit="return false;">')

    
    # system_files
    system_files_hint = "Backup the cPanel System Files"
    print('                                    <div class="row align-items-center"> <!-- Row Start -->')
    if system_files == 'enabled':
        print('                                        '+return_green("system_files", system_files_hint))
        print('                                        <div class="col-md-6">')
        print('                                            <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('                                                <label class="btn btn-light active">')
        print('                                                    <input type="radio" name="system_files" value="enabled" id="BuFilesOn" autocomplete="off" checked> Enabled')
        print('                                                </label>')
        print('                                                <label class="btn btn-light">')
        print('                                                    <input type="radio" name="system_files" value="disabled" id="BuFilesOff" autocomplete="off"> Disabled')
        print('                                                </label>')
        print('                                            </div>')
        print('                                        </div>')
    else:
        print('                                        '+return_red("system_files", system_files_hint))
        print('                                        <div class="col-md-6">')
        print('                                            <div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('                                                <label class="btn btn-light">')
        print('                                                    <input type="radio" name="system_files" value="enabled" id="BuFilesOn" autocomplete="off"> Enabled')
        print('                                                </label>')
        print('                                                <label class="btn btn-light active">')
        print('                                                    <input type="radio" name="system_files" value="disabled" id="BuFilesOff" autocomplete="off" checked> Disabled')
        print('                                                </label>')
        print('                                            </div>')
        print('                                        </div>')

    
    # mysql_backup
    mysql_backup_hint = "Use MariaBackup to Backup the FULL MySQL Data Directory"
    if mysql_backup == 'enabled':
        print('                                        '+return_green("mariabackup", mysql_backup_hint))
        print('                                        <div class="col-md-6">')
        print('                                            <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                                <label class="btn btn-light active">')
        print('                                                    <input type="radio" name="mysql_backup" value="enabled" id="BuDataOn" autocomplete="off" checked> Enabled')
        print('                                                </label>')
        print('                                                <label class="btn btn-light">')
        print('                                                    <input type="radio" name="mysql_backup" value="disabled" id="BuDataOff" autocomplete="off"> Disabled')
        print('                                                </label>')
        print('                                            </div>')
        print('                                        </div>')
    else:
        print('                                        '+return_red("mariabackup", mysql_backup_hint))
        print('                                        <div class="col-md-6">')
        print('                                            <div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('                                                <label class="btn btn-light">')
        print('                                                    <input type="radio" name="mysql_backup" value="enabled" id="BuDataOn" autocomplete="off"> Enabled')
        print('                                                </label>')
        print('                                                <label class="btn btn-light active">')
        print('                                                    <input type="radio" name="mysql_backup" value="disabled" id="BuDataOff" autocomplete="off" checked> Disabled')
        print('                                                </label>')
        print('                                            </div>')
        print('                                        </div>')

    
    # backup_path
    backup_path_hint = "This is the directory where the cPanel PKG Accounts, SQL backups, and system files are stored."
    print('                                        <div class="col-md-12">')
    print('                                            <div class="input-group mt-2 mb-2">')
    print('                                                <div class="input-group-prepend">')
    print('                                                    <span class="input-group-text">')
    print('                                                        '+return_multi_input("PKGacct Backup Path", backup_path_hint))
    print('                                                    </span>')
    print('                                                </div>')
    print('                                                <input class="form-control" placeholder="'+backup_path+'" type="text" name="backup_path">')
    print('                                            </div>')
    print('                                        </div>')
    print('                                        <div class="col-md-12">')
    print('                                            <button class="btn btn-outline-primary btn-block mt-2" type="submit">Save Backup Settings</button>')
    print('                                        </div>')
    print('                                    </div>')
    print('                                </form>')
    print('                            </div> <!-- Row End -->') #Row Start
    print('                        </div> <!-- Card Body End -->') #Card Body End
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

    # Since we have a borgmatic config now.Lets load it up and present to the user

    if os.path.isfile(borgmatic_config_file):

        # Get all config settings from the borgmatic config file

        with open(borgmatic_config_file, 'r') as borgmatic_config_file_stream:
            yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_config_file_stream)

    cardheader('Additional <kbd> /home</kbd> Directory Backup','fas fa-database')
    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start

    # backup directories

    backup_dir_list = yaml_parsed_borgmaticyaml['location']['source_directories']

    if backup_dir_list:
        print('                            <div class="label label-default mb-2">Currently backing up:</div>')
        print('                            <div class="clearfix">')
        mykeypos=1
        for path in backup_dir_list:
            print('                                <div class="input-group input-group-inline input-group-sm">')
            print('                                    <div class="input-group-prepend">')
            print('                                        <span class="input-group-text">'+path+'</span>')
            print('                                    </div>')
            if path not in ['/home', backup_path]:
                print('                                    <div class="input-group-append">')
                print('                                        <form class="form toastForm13-wrap" method="post" id="toastForm13'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                print('                                            <input hidden name="thehomedir" value="'+path+'">')
                print('                                            <input hidden name="action" value="delete">')
                print('                                            <button class="btn btn-outline-danger" type="submit">')
                print('                                                <span class="sr-only">Delete</span>')
                print('                                                <i class="fas fa-times"></i>')
                print('                                            </button>')
                print('                                        </form>')
                print('                                    </div>')
            mykeypos = mykeypos + 1
            print('                                </div>')
    print('                            </div>')
    print('                            <div class="label label-default mt-2 mb-2">Add another <kbd> /home</kbd> directory to backup:</div>')
    print('                            <form class="form" method="post" id="toastForm14" onsubmit="return false;">')

    print('                                <div class="input-group mb-0">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">Enter Path</span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="/home2" type="text" name="thehomedir">')
    print(('                                    <input hidden name="action" value="add">'))
    print('                                    <div class="input-group-append">')
    print('                                        <button class="btn btn-outline-primary" type="submit">')
    print('                                            <span class="sr-only">Add</span><i class="fas fa-plus"></i>')
    print('                                        </button>')
    print('                                    </div>')
    print('                                </div>')

    print('                            </form>')
    print('                        </div> <!-- Card Body End -->') #Card Body End    
    cardfooter('Configure additional /home directories that you would like to backup.')            


    #First Column End
    print('                <!-- First Column End -->')
    print('                </div>')
    print('')

    
    #Second Column
    print('                <!-- Second Column Start -->')
    print('                <div class="col-lg-6">') #Right Column
    print('')

    cardheader('Borg Settings','fas fa-database')
    print('                        <div class="card-body"> <!-- Card Body Start -->') #Card Body Start
    print('                            <form class="form input-group-prepend-min" method="post" id="toastForm12" onsubmit="return false;"> ')

    # repositories
    repositories_hint = "eg: user@backupserver:sourcehostname.borg"
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("repositories", repositories_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="'+yaml_parsed_borgmaticyaml['location']['repositories'][0]+'" type="text" name="repositories">')
    print('                                </div>')

    # ssh_command
    ssh_command_hint = "Additinal options for SSH"
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("ssh_command", ssh_command_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="'+yaml_parsed_borgmaticyaml['storage']['ssh_command']+'" type="text" name="ssh_command">')
    print('                                </div>')

    # encryption_passphrase
    encryption_passphrase_hint = "Your Passphrase used to Encrypt the Backup"
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("passphrase", encryption_passphrase_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="'+yaml_parsed_borgmaticyaml['storage']['encryption_passphrase']+'" type="text" name="encryption_passphrase">')
    print('                                </div>')

    # remote_rate_limit
    remote_rate_limit_hint = "Set the Network Upload Rate Limit in KB/s"
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("remote_rate_limit", remote_rate_limit_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['storage']['remote_rate_limit'])+'" type="text" name="remote_rate_limit">')
    print('                                </div>')

    # retention
    print('                                <label class="label mt-2 mb-2">Backup Retention</label>')
    # keep_hourly
    keep_hourly_hint = "Enter the number of hourly backups to keep."
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("keep_hourly", keep_hourly_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['retention']['keep_hourly'])+'" type="text" name="keep_hourly">')
    print('                                </div>')

    # keep_daily
    keep_daily_hint = "Enter the number of daily backups to keep."
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("keep_daily", keep_daily_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['retention']['keep_daily'])+'" type="text" name="keep_daily">')
    print('                                </div>')

    # keep_weekly
    keep_weekly_hint = "Enter the number of weekly backups to keep."
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("keep_weekly", keep_weekly_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['retention']['keep_weekly'])+'" type="text" name="keep_weekly">')
    print('                                </div>')

    # keep_monthly
    keep_monthly_hint = "Enter the number of monthly backups to keep."
    print('                                <div class="input-group">')
    print('                                    <div class="input-group-prepend">')
    print('                                        <span class="input-group-text">')
    print('                                            '+return_multi_input("keep_monthly", keep_monthly_hint))
    print('                                        </span>')
    print('                                    </div>')
    print('                                    <input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['retention']['keep_monthly'])+'" type="text" name="keep_monthly">')
    print('                                </div>')

    print('                                <button class="btn btn-outline-primary btn-block mt-3" type="submit">Save Borg Settings</button>')

    print('                            </form>')

    print('                        </div> <!-- Card Body End -->') #Card Body End
    cardfooter('Keep your Encryption Passphrase in a safe place. <br>Losing it would make data recovery impossible on a server crash.')

else:
    print('                                <center><h1><i class="fas fa-exclamation"></i></h1>')
    print('                                <p>Borg/Borgmatic is currently not installed.<br>To install run the following command:')
    print('                                <kbd>/opt/nDeploy/scripts/easy_borg_setup.sh</kbd></p></center>')
    print('                            </div> <!-- Row End -->') #Row End
    print('                        </div> <!-- Card Body End -->') #Card End
    cardfooter('Borg backup software is not installed.')


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
