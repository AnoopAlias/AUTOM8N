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


def branding_print_logo_name():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    else:
        brand_logo = "xtendweb.png"
    return brand_logo


def branding_print_banner():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_name = yaml_parsed_brand.get("brand", "AUTOM8N")
    else:
        brand_name = "AUTOM8N"
    return brand_name


def branding_print_support():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_support = yaml_parsed_brand.get("brand_support", '<div class="help float-right"><a class="btn btn-primary" target="_blank" href="https://autom8n.com"> docs <i class="fas fa-book-open"></i></a></div>')
    else:
        brand_support = '<div class="help float-right"><a class="btn btn-primary" target="_blank" href="https://autom8n.com"> docs <i class="fas fa-book-open"></i></a></div>'
    return brand_support


def print_green(theoption, hint):
    print(('<div class="col-md-6 align-self-center"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_red(theoption, hint):
    print(('<div class="col-md-6 align-self-center"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_multi_input(theoption, hint):
    print(('<div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'))


form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')

print('<title>')
print(branding_print_banner())
print('</title>')

print(('<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>'))
print(('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>'))
print(('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">'))
print(('<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>'))
print(('<link href="https://fonts.googleapis.com/css?family=Poppins&display=swap" rel="stylesheet">'))
print(('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css" rel="stylesheet">'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')

print('<body>')

print('<header id="main-header">')

print(branding_print_support())
print('		<div class="logo">')
print('			<h4>')
print('				<a href="xtendweb.cgi"><img border="0" src="')
print(					branding_print_logo_name())
print('					" width="48" height="48"></a>')
print(					branding_print_banner())
print('			</h4>')
print('		</div>')

print('</header>')

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
        pkgacct_backup = yaml_parsed_backupyaml.get('pkgacct_backup')
        system_files = yaml_parsed_backupyaml.get('system_files')
        mysql_backup = yaml_parsed_backupyaml.get('mysql_backup')
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

    print('					<form class="form" method="post" id="modalForm11" onsubmit="return false;">')

    # system_files
    system_files_hint = "Backup cPanel system files"
    print('						<div class="row text-right">')
    if system_files == 'enabled':
        print_green("system_files", system_files_hint)
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
        print_red("system_files", system_files_hint)
        print('						<div class="col-md-6">')
        print('							<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
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
        print_green("mariabackup", mysql_backup_hint)
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
        print_red("mariabackup", mysql_backup_hint)
        print('						<div class="col-md-6">')
        print('							<div class="btn-group btn-block btn-group-toggle" data-toggle="buttons">')
        print('								<label class="btn btn-light">')
        print('									<input type="radio" name="mysql_backup" value="enabled" id="BuDataOn" autocomplete="off"> Enabled')
        print('								</label>')
        print('								<label class="btn btn-light active">')
        print('									<input type="radio" name="mysql_backup" value="disabled" id="BuDataOff" autocomplete="off checked"> Disabled')
        print('								</label>')
        print('							</div>')
        print('						</div>')

    # backup_path
    backup_path_hint = "The directory where the cPanel pkgacct, MySQL backup and system files are stored"
    print('							<div class="col-md-12">')
    print('								<div class="input-group mt-2">')
    print('									<div class="input-group-prepend">')
    print('										<span class="input-group-text">')
    print_multi_input("pkgacct backup path", backup_path_hint)
    print('										</span>')
    print('									</div>')
    print('									<input class="form-control" placeholder="'+backup_path+'" type="text" name="backup_path">')
    print('								</div>')
    print('							</div>')

    print('							<div class="col-md-12">')
    print('								<button class="btn btn-outline-primary btn-block btn-ajax mt-2" type="submit">Save Backup Settings</button>')
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

    print('		</div>')  # end col left

    print('		<div class="col-lg-6">')  # col right

    print('			<div class="card">')  # card
    print('				<div class="card-header">')
    print('					<h5 class="card-title mb-0"><i class="fas fa-database float-right"></i> Borg Settings</h5>')
    print('				</div>')
    print('				<div class="card-body">')  # card-body

    print('					<form class="form input-group-prepend-min" method="post" id="modalForm12" onsubmit="return false;"> ')

    # repositories
    repositories_hint = "eg: user@backupserver:sourcehostname.borg"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    print_multi_input("repositories", repositories_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="'+yaml_parsed_borgmaticyaml['location']['repositories'][0]+'" type="text" name="repositories">')
    print('						</div>')

    # ssh_command
    ssh_command_hint = "options for ssh"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    print_multi_input("ssh_command", ssh_command_hint)
    print('								</span>')
    print('							</div>')
    print('								<input class="form-control" placeholder="'+yaml_parsed_borgmaticyaml['storage']['ssh_command']+'" type="text" name="ssh_command">')
    print('						</div>')

    # encryption_passphrase
    encryption_passphrase_hint = "passphrase used to encrypt the backup"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    print_multi_input("passphrase", encryption_passphrase_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="'+yaml_parsed_borgmaticyaml['storage']['encryption_passphrase']+'" type="text" name="encryption_passphrase">')
    print('						</div>')

    # remote_rate_limit
    remote_rate_limit_hint = "network upload rate limit in kiBytes/second"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    print_multi_input("remote_rate_limit", remote_rate_limit_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['storage']['remote_rate_limit'])+'" type="text" name="remote_rate_limit">')
    print('						</div>')

    # retention
    print('<label class="label label-default mt-2 mb-2">Backup Retention</label>')
    # keep_hourly
    keep_hourly_hint = "number of hourly backups to keep"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    print_multi_input("keep_hourly", keep_hourly_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['retention']['keep_hourly'])+'" type="text" name="keep_hourly">')
    print('						</div>')

    # keep_daily
    keep_daily_hint = "number of daily backups to keep"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    print_multi_input("keep_daily", keep_daily_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['retention']['keep_daily'])+'" type="text" name="keep_daily">')
    print('						</div>')

    # keep_weekly
    keep_weekly_hint = "number of weekly backups to keep"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    print_multi_input("keep_weekly", keep_weekly_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['retention']['keep_weekly'])+'" type="text" name="keep_weekly">')
    print('						</div>')

    # keep_monthly
    keep_monthly_hint = "number of monthly backups to keep"
    print('						<div class="input-group">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">')
    print_multi_input("keep_monthly", keep_monthly_hint)
    print('								</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="'+str(yaml_parsed_borgmaticyaml['retention']['keep_monthly'])+'" type="text" name="keep_monthly">')
    print('						</div>')

    print('						<button class="btn btn-outline-primary btn-block btn-ajax mt-4" type="submit">Save Borg Settings</button>')

    print('					</form>')

    print('				</div>')  # card-body end
    print('				<div class="card-footer">')
    print('					<small>Keep encryption_passphrase copied safely. Losing it would make data recovery impossible on a server crash</small>')
    print('				</div>')
    print('			</div>')  # card end

    print('			<div class="card">')  # card
    print('				<div class="card-header">')
    print('					<h5 class="card-title mb-0"><i class="fas fa-database float-right"></i> Additional Home directory to backup</h5>')
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
                print('			<form class="form modalForm13-wrap" method="post" id="modalForm13'+'-'+str(mykeypos)+'" onsubmit="return false;">')
                print('				<button class="btn btn-outline-danger" type="submit"><span class="sr-only">Delete</span><i class="fas fa-times"></i></button>')
                print(('			<input class="hidden" name="thehomedir" value="'+path+'">'))
                print(('			<input class="hidden" name="action" value="delete">'))
                print('			</form>')
            mykeypos = mykeypos + 1
            print('			</div>')
    print('				</div>')
    print('				<div class="label label-default mt-2 mb-2">Add new home directory to backup:</div>')
    print('					<form class="form" method="post" id="modalForm14" onsubmit="return false;">')

    print('						<div class="input-group mb-0">')
    print('							<div class="input-group-prepend">')
    print('								<span class="input-group-text">Enter Path</span>')
    print('							</div>')
    print('							<input class="form-control" placeholder="/home2" type="text" name="thehomedir">')
    print('							<button class="btn btn-outline-primary" type="submit"><span class="sr-only">Add</span><i class="fas fa-plus"></i></button>')
    print(('						<input class="hidden" name="action" value="add">'))
    print('						</div>')

    print('					</form>')
else:
    print('					<i class="fas fa-exclamation"></i>')
    print('					<p>Borg/Borgmatic not installed.</p>')
    print('					<small class="mb-1">To install run the following command</small>')
    print('					<kbd>/opt/nDeploy/scripts/easy_borg_setup.sh</kbd>')

print('					</div>')  # card-body end
print('				</div>')  # card end

print('			</div>')  # col right end
print('		</div>')  # row end

print('</div>')  # main-container end

# Modal
print('		<div class="modal fade" id="myModal" tabindex="-1" role="dialog"> ')
print('    		<div class="modal-dialog modal-dialog-centered" role="document">')
print('      		<div class="modal-content">')
print('        			<div class="modal-header">')
print('          			<h4 class="modal-title">Command Output</h4>')
print('						<button type="button" class="close" data-dismiss="modal" aria-label="Close">')
print('          				<span aria-hidden="true">&times;</span>')
print('        				</button>')
print('        			</div>')
print('        			<div class="modal-body">')
print('        			</div>')
print('					<div class="modal-footer">')
print('        				<button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>')
print('      			</div>')
print('      		</div>')
print('    		</div>')
print('     </div>')

print('</body>')
print('</html>')
