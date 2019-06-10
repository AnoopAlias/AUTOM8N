#!/usr/bin/python

import cgi
import cgitb
import subprocess
import os
import yaml
import platform
import psutil
import signal
import sys
import re


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


def print_forbidden():
    print(('<i class="fas fa-exclamation"></i><p>Forbidden</p>'))


def print_error(themessage):
    print(('<i class="fas fa-exclamation"></i><p>'+themessage+'</p>'))


def print_success(themessage):
    print(('<i class="fas fa-thumbs-up"></i><p>'+themessage+'</p>'))


form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

with open(borgmatic_config_file, 'r') as borgmatic_conf:
    yaml_parsed_borgmaticyaml = yaml.safe_load(borgmatic_conf)
backup_dir_list = yaml_parsed_borgmaticyaml['location']['source_directories']

if form.getvalue('repositories'):
    yaml_parsed_borgmaticyaml['location']['repositories'][0] = form.getvalue('repositories')
if form.getvalue('remote_rate_limit'):
    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('remote_rate_limit')):
        print_error("Error: Positive integer value expected for remote_rate_limit")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['storage']['remote_rate_limit'] = int(form.getvalue('remote_rate_limit'))
if form.getvalue('ssh_command'):
    yaml_parsed_borgmaticyaml['storage']['ssh_command'] = form.getvalue('ssh_command')
if form.getvalue('encryption_passphrase'):
    # Input sanitation
    if not re.match("^[0-9a-zA-Z]+$", form.getvalue('encryption_passphrase')):
        print_error("Error: Do not use any symbols, use only numbers,small letters and capital letters in encryption passphrase")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['storage']['encryption_passphrase'] = form.getvalue('encryption_passphrase')
if form.getvalue('keep_hourly'):
    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('keep_hourly')):
        print_error("Error: Positive integer value expected for keep_hourly")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['retention']['keep_hourly'] = int(form.getvalue('keep_hourly'))
if form.getvalue('keep_daily'):
    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('keep_daily')):
        print_error("Error: Positive integer value expected for keep_daily")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['retention']['keep_daily'] = int(form.getvalue('keep_daily'))
if form.getvalue('keep_weekly'):
    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('keep_weekly')):
        print_error("Error: Positive integer value expected for keep_weekly")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['retention']['keep_weekly'] = int(form.getvalue('keep_weekly'))
if form.getvalue('keep_monthly'):
    # Input sanitation
    if not re.match("^[0-9]+$", form.getvalue('keep_monthly')):
        print_error("Error: Positive integer value expected for keep_monthly")
        sys.exit(0)
    else:
        yaml_parsed_borgmaticyaml['retention']['keep_monthly'] = int(form.getvalue('keep_monthly'))
if form.getvalue('thehomedir'):
    if not form.getvalue('thehomedir').startswith('/'):
        myhomedir_pass1 = '/'+form.getvalue('thehomedir')
    else:
        myhomedir_pass1 = form.getvalue('thehomedir')
    if myhomedir_pass1.endswith('/'):
        myhomedir = myhomedir_pass1[:-1]
    else:
        myhomedir = myhomedir_pass1
    if not myhomedir:
        print_error('Error: Invalid Homedir name')
        sys.exit(0)
    if not re.match("^[\.0-9a-zA-Z/_-]*$", myhomedir):
        print_error("Error: Invalid char in Homedir name")
        sys.exit(0)
    if form.getvalue('action'):
        if form.getvalue('action') == "add":
            if myhomedir not in backup_dir_list:
                backup_dir_list.append(myhomedir)
            yaml_parsed_borgmaticyaml['location']['source_directories'] = backup_dir_list
        elif form.getvalue('action') == "delete":
            backup_dir_list.remove(form.getvalue('thehomedir'))
            yaml_parsed_borgmaticyaml['location']['source_directories'] = backup_dir_list

with open(borgmatic_config_file, 'w') as borgmatic_conf:
    yaml.dump(yaml_parsed_borgmaticyaml, borgmatic_conf, default_flow_style=False)
os.chmod(borgmatic_config_file, 0o640)

print_success('Borgmatic Settings updated')

print('</body>')
print('</html>')
