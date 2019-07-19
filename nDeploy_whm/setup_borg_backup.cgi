#!/usr/bin/python

import commoninclude
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
import json

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backup_config_file = "/opt/nDeploy/conf/backup_config.yaml"
borgmatic_config_file = "/etc/borgmatic/config.yaml"

cgitb.enable()


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def safenginxreload():
    nginx_status = False
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if '/usr/sbin/nginx' in mycmdline and 'reload' in mycmdline:
            nginx_status = True
            break
    if not nginx_status:
        with open(os.devnull, 'w') as FNULL:
            subprocess.Popen(['/usr/sbin/nginx', '-s', 'reload'], stdout=FNULL, stderr=subprocess.STDOUT)


def sighupnginx():
    for myprocess in psutil.process_iter():
        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
            nginxpid = myprocess.pid
            os.kill(nginxpid, signal.SIGHUP)


form = cgi.FieldStorage()

commoninclude.print_header()

print('<body>')

commoninclude.print_branding()

print('<div id="main-container" class="container">')  # main container

print('		<nav aria-label="breadcrumb">')
print('			<ol class="breadcrumb">')
print('				<li class="breadcrumb-item"><a href="xtendweb.cgi"><i class="fas fa-redo"></i></a></li>')
print('				<li class="breadcrumb-item active">Backup Config</li>')
print('			</ol>')
print('		</nav>')

print('		<div class="row">')

print('			<div class="col-lg-6">')  # col left

print('				<div class="card">')  # card
print('					<div class="card-header">')
print('						<h5 class="card-title mb-0"><i class="fas fa-database float-right"></i> Backup Settings</h5>')
print('					</div>')
print('					<div class="card-body">')  # card-body

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
        backup_path = yaml_parsed_backupyaml.get('backup_path')
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

    print('					<form class="form" method="post" id="toastForm11" onsubmit="return false;">')

    # system_files
    system_files_hint = "Backup cPanel system files"
    print('						<div class="row align-items-center">')
    if system_files == 'enabled':
        commoninclude.print_green("system_files", system_files_hint)
        print('						<div class="col-md-6">')
        print('							<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('								<label class="btn btn-light active">')
        print('									<input type="radio" name="system_files" value="enabled" id="BuFilesOn" autocomplete="off" checked> Enabled')
        print('								</label>')
        print('								<label class="btn btn-light">')
        print('									<input type="radio" name="system_files" value="disabled" id="BuFilesOff" autocomplete="off"> Disabled')
        print('								</label>')
        print('							</div>')
        print('						</div>')
    else:
        commoninclude.print_red("system_files", system_files_hint)
        print('						<div class="col-md-6">')
        print('							<div class="btn-group btn-block btn-group-toggle mt-0" data-toggle="buttons">')
        print('								<label class="btn btn-light">')
        print('									<input type="radio" name="system_files" value="enabled" id="BuFilesOn" autocomplete="off"> Enabled')
        print('								</label>')
        print('								<label class="btn btn-light active">')
        print('									<input type="radio" name="system_files" value="disabled" id="BuFilesOff" autocomplete="off" checked> Disabled')
        print('								</label>')
        print('							</div>')
        print('						</div>')

    # mysql_backup
    mysql_backup_hint = "Use MariaBackup to backup full MySQL datadir"
    if mysql_backup == 'enabled':
        commoninclude.print_green("mariabackup", mysql_backup_hint)
        print('						<div class="col-md-6">')
        print('							<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('								<label class="btn btn-light active">')
        print('									<input type="radio" name="mysql_backup" value="enabled" id="BuDataOn" autocomplete="off" checked> Enabled')
        print('								</label>')
        print('								<label class="btn btn-light">')
        print('									<input type="radio" name="mysql_backup" value="disabled" id="BuDataOff" autocomplete="off"> Disabled')
        print('								</label>')
        print('							</div>')
        print('						</div>')
    else:
        commoninclude.print_red("mariabackup", mysql_backup_hint)
        print('						<div class="col-md-6">')
        print('							<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('								<label class="btn btn-light">')
        print('									<input type="radio" name="mysql_backup" value="enabled" id="BuDataOn" autocomplete="off"> Enabled')
        print('								</label>')
        print('								<label class="btn btn-light active">')
        print('									<input type="radio" name="mysql_backup" value="disabled" id="BuDataOff" autocomplete="off" checked> Disabled')
        print('								</label>')
        print('							</div>')
        print('						</div>')

    # backup_path
    backup_path_hint = "The directory where the cPanel pkgacct, MySQL backup and system files are stored"
    print('							<div class="col-md-12">')
    print('								<div class="input-group mt-2 mb-2">')
    print('									<div class="input-group-prepend">')
    print('										<span class="input-group-text">')
    commoninclude.print_multi_input("pkgacct backup path", backup_path_hint)
    print('										</span>')
    print('									</div>')
    print('									<input class="form-control" placeholder="'+backup_path+'" type="text" name="backup_path">')
    print('								</div>')
    print('							</div>')

    print('							<div class="col-md-12">')
    print('								<button class="btn btn-outline-primary btn-block mt-2" type="submit">Save Backup Settings</button>')
    print('							</div>')
    print('						</div>')

    print('					</form>')

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

    print('				</div>')  # card-body end
    print('			</div>')  # card end

    # list backup and allow restore
    if os.path.isfile('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE'):
        if not os.path.exists('/root/borg_restore_point'):
            os.makedirs('/root/borg_restore_point')
        print('			<div class="card">')  # card
        print('				<div class="card-header">')
        print('					<h5 class="card-title mb-0"><i class="fas fa-database float-right"></i>Restore points</h5>')
        print('				</div>')
        print('				<div class="card-body">')  # card-body
        if os.path.ismount('/root/borg_restore_point'):
            with open('/etc/borgmatic/BORG_SETUP_LOCK_DO_NOT_REMOVE', 'r') as restore_point_conf:
                yaml_parsed_restorepoint = yaml.safe_load(restore_point_conf)
            restore_point = yaml_parsed_restorepoint.get('restore_point', 'snapshot')
            commoninclude.print_success_alert(restore_point)
            print('				<form class="form mb-3" id="toastForm24" onsubmit="return false;">')
            print(('				<input class="hidden" name="action" value="umount">'))
            print('					<button type="submit" class="btn btn-outline-primary btn-block ">Umount Restore Point</button>')
            print('				</form>')
            mount_flag=True
        else:
            mount_flag=False
        proc = subprocess.Popen('borgmatic --list --json', shell=True, stdout=subprocess.PIPE)
        output = json.loads(proc.stdout.read())
        myarchives = output[0].get('archives')
        mykeypos = 1
        print('                 <div class="input-group">')
        print('                     <select name="myarchives" class="custom-select">')
        for backup in myarchives:
            print(('                    <option selected value="'+backup.get('archive')+'">'+backup.get('archive')+'</option>'))
        print('                     </select>')
        if not mount_flag:
            print('                 <div class="input-group-append">')
            print('                     <form class="m-0 toastForm25-wrap" id="toastForm25'+'-'+str(mykeypos)+'"  method="post" onsubmit="return false;">')
            print(('                        <input class="hidden" name="restorepoint" value="'+backup.get('archive')+'">'))
            print(('                        <input class="hidden" name="action" value="mount">'))
            print('                         <button class="btn btn-outline-primary btn-block" type="submit">Mount <i class="fas fa-upload"></i></button>')
            print('                     </form>')
            print('                 </div>')
            mykeypos = mykeypos + 1
        print('                 </div>')
        print('				</div>')  # card-body end
        print('				<div class="card-footer">')
        print('					<small>/root/borg_restore_point is the mount point.</small>')
        print('				</div>')
        print('			</div>')  # card end

    print('		</div>')  # end col left

    print('		<div class="col-lg-6">')  # col right

    print('			<div class="card">')  # card
    print('				<div class="card-header">')
    print('					<h5 class="card-title mb-0"><i class="fas fa-database float-right"></i> Borg Settings</h5>')
    print('				</div>')
    print('				<div class="card-body">')  # card-body

    print('					<form class="form input-group-prepend-min" method="post" id="toastForm12" onsubmit="return false;"> ')

    # repositories
    repositories_hint = "eg: user@backupserver:sourcehostname.borg"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    commoninclude.print_multi_input("repositories", repositories_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" value="'+yaml_parsed_borgmaticyaml['location']['repositories'][0]+'" type="text" name="repositories">')
    print('						</div>')

    # ssh_command
    ssh_command_hint = "options for ssh"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    commoninclude.print_multi_input("ssh_command", ssh_command_hint)
    print('								</span>')
    print('							</div>')
    print('								<input class="form-control" value="'+yaml_parsed_borgmaticyaml['storage']['ssh_command']+'" type="text" name="ssh_command">')
    print('						</div>')

    # encryption_passphrase
    encryption_passphrase_hint = "passphrase used to encrypt the backup"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    commoninclude.print_multi_input("passphrase", encryption_passphrase_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" value="'+yaml_parsed_borgmaticyaml['storage']['encryption_passphrase']+'" type="text" name="encryption_passphrase">')
    print('						</div>')

    # remote_rate_limit
    remote_rate_limit_hint = "network upload rate limit in kiBytes/second"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    commoninclude.print_multi_input("remote_rate_limit", remote_rate_limit_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['storage']['remote_rate_limit'])+'" type="text" name="remote_rate_limit">')
    print('						</div>')

    # retention
    print('<label class="label label-default mt-2 mb-2">Backup Retention</label>')
    # keep_hourly
    keep_hourly_hint = "number of hourly backups to keep"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    commoninclude.print_multi_input("keep_hourly", keep_hourly_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['retention']['keep_hourly'])+'" type="text" name="keep_hourly">')
    print('						</div>')

    # keep_daily
    keep_daily_hint = "number of daily backups to keep"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    commoninclude.print_multi_input("keep_daily", keep_daily_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['retention']['keep_daily'])+'" type="text" name="keep_daily">')
    print('						</div>')

    # keep_weekly
    keep_weekly_hint = "number of weekly backups to keep"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    commoninclude.print_multi_input("keep_weekly", keep_weekly_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['retention']['keep_weekly'])+'" type="text" name="keep_weekly">')
    print('						</div>')

    # keep_monthly
    keep_monthly_hint = "number of monthly backups to keep"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    commoninclude.print_multi_input("keep_monthly", keep_monthly_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" value="'+str(yaml_parsed_borgmaticyaml['retention']['keep_monthly'])+'" type="text" name="keep_monthly">')
    print('						</div>')

    print('						<button class="btn btn-outline-primary btn-block mt-3" type="submit">Save Borg Settings</button>')

    print('					</form>')
    print('					<form class="form" id="modalForm5" onsubmit="return false;">')
    print(('					 <input class="hidden" name="action" value="initrepo">'))
    print('						 <button class="btn btn-outline-primary btn-block mt-3" type="submit">Init Borg Repo</button>')
    print('	                </form>')

    print('				</div>')  # card-body end
    print('				<div class="card-footer">')
    print('					<small>Keep your encryption_passphrase in a safe place. Losing it would make data recovery impossible on a server crash.</small>')
    print('				</div>')
    print('			</div>')  # card end

    print('			<div class="card">')  # card
    print('				<div class="card-header">')
    print('					<h5 class="card-title mb-0"><i class="fas fa-database float-right"></i> Additional home directory to backup</h5>')
    print('				</div>')
    print('			<div class="card-body">')  # card-body

    # backup directories
    backup_dir_list = yaml_parsed_borgmaticyaml['location']['source_directories']

    if backup_dir_list:
        print('		<div class="label label-default mb-2">Currently backing up:</div>')
        print('			<div class="clearfix">')
        mykeypos=1
        for path in backup_dir_list:
            print('			<div class="input-group input-group-inline input-group-sm">')
            print('				<div class="input-group-prepend"><span class="input-group-text">')
            print(path)
            print('				</span></div>')
            if path not in ['/home', backup_path]:
                print('			<div class="input-group-append"><form class="form toastForm13-wrap" method="post" id="toastForm13'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                print(('			<input class="hidden" name="thehomedir" value="'+path+'">'))
                print(('			<input class="hidden" name="action" value="delete">'))
                print('				<button class="btn btn-outline-danger" type="submit"><span class="sr-only">Delete</span><i class="fas fa-times"></i></button>')
                print('			</form></div>')
            mykeypos = mykeypos + 1
            print('			</div>')
    print('				</div>')
    print('				<div class="label label-default mt-2 mb-2">Add new home directory to backup:</div>')
    print('					<form class="form" method="post" id="toastForm14" onsubmit="return false;">')

    print('						<div class="input-group mb-0">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">Enter Path</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="/home2" type="text" name="thehomedir">')
    print(('						<input class="hidden" name="action" value="add">'))
    print('							<div class="input-group-append"><button class="btn btn-outline-primary" type="submit"><span class="sr-only">Add</span><i class="fas fa-plus"></i></button></div>')
    print('						</div>')

    print('					</form>')
else:
    print('					<p>Install and setup Borg/Borgmatic</p>')
    print('					            <form class="form" id="modalForm4" onsubmit="return false;">')
    print(('					            <input class="hidden" name="action" value="installborg">'))
    print('					                <button class="btn btn-primary">Install</button>')
    print('								</form>')

print('					</div>')  # card-body end
print('				</div>')  # card end

print('			</div>')  # col right end
print('		</div>')  # row end

print('</div>')  # main-container end

commoninclude.print_modals()
commoninclude.print_loader()

print('</body>')
print('</html>')
