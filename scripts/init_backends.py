#!/usr/bin/env python


import yaml
import argparse
import subprocess
import os
import signal
import time
import pwd
import jinja2
import codecs
import sys


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
php_fpm_config = installation_path+"/conf/php-fpm.conf"


# Function defs


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def control_php_fpm(trigger):
    if "PHP" in backend_data_yaml_parsed:
        php_backends_dict = backend_data_yaml_parsed["PHP"]
        if trigger == "autofix":
            conf_list = os.listdir("/opt/nDeploy/php-fpm.d")
            for filename in conf_list:
                user, extension = filename.split('.')
                try:
                    pwd.getpwnam(user)
                except KeyError:
                    os.remove("/opt/nDeploy/php-fpm.d/"+filename)
                if user != 'nobody':
                    user_home = pwd.getpwnam(user).pw_dir
                    user_shell = pwd.getpwnam(user).pw_shell
                    if user_shell == '/usr/local/cpanel/bin/noshell':
                        print('Please set Jailed shell for user: '+user)
                    else:
                        print('VirtfsJailFix:: '+user)
                        subprocess.call('su - '+user+' -c "touch '+user_home+'/public_html"', shell=True)
        elif trigger == "start":
            subprocess.call("sysctl -q -w net.core.somaxconn=4096", shell=True)
            subprocess.call("sysctl -q -w vm.max_map_count=131070", shell=True)
            for path in list(php_backends_dict.values()):
                if os.path.isfile(path+"/sbin/php-fpm"):
                    php_fpm_bin = path+"/sbin/php-fpm"
                else:
                    php_fpm_bin = path+"/usr/sbin/php-fpm"
                subprocess.call(php_fpm_bin+" --prefix "+path+" --fpm-config "+php_fpm_config, shell=True)
        elif trigger == "stop":
            for path in list(php_backends_dict.values()):
                php_fpm_pid = path+"/var/run/php-fpm.pid"
                if os.path.isfile(php_fpm_pid):
                    with open(php_fpm_pid) as f:
                        mypid = f.read()
                    f.close()
                    try:
                        os.kill(int(mypid), signal.SIGQUIT)
                        time.sleep(3)  # Give enough time for all child process to exit
                    except OSError:
                        break
        elif trigger == "reload":
            for path in list(php_backends_dict.values()):
                php_fpm_pid = path+"/var/run/php-fpm.pid"
                if os.path.isfile(path+"/sbin/php-fpm"):
                    php_fpm_bin = path+"/sbin/php-fpm"
                else:
                    php_fpm_bin = path+"/usr/sbin/php-fpm"
                if os.path.isfile(php_fpm_pid):
                        with open(php_fpm_pid) as f:
                            mypid = f.read()
                        try:
                            os.kill(int(mypid), signal.SIGUSR2)
                        except OSError:
                            subprocess.call(php_fpm_bin+" --prefix "+path+" --fpm-config "+php_fpm_config, shell=True)
                        time.sleep(3)
                        try:
                            with open(path + "/var/run/php-fpm.pid") as f:
                                newpid = f.read()
                        except IOError:
                            subprocess.call(php_fpm_bin+" --prefix "+path+" --fpm-config "+php_fpm_config, shell=True)
                        try:
                            os.kill(int(newpid), 0)
                        except OSError:
                            subprocess.call(php_fpm_bin+" --prefix "+path+" --fpm-config "+php_fpm_config, shell=True)
                else:
                        subprocess.call(php_fpm_bin+" --prefix "+path+" --fpm-config "+php_fpm_config, shell=True)
        elif trigger == "secure-php":
            try:
                subprocess.call(['systemctl', '--version'])
            except OSError:
                print('secure-php needs systemd . upgrade your cPanel system to CentOS7 ')
                sys.exit(1)
            else:
                for backend_name in list(php_backends_dict.keys()):
                    systemd_socket_file = "/etc/systemd/system/"+backend_name+"@.socket"
                    systemd_service_file = "/etc/systemd/system/"+backend_name+"@.service"
                    templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
                    templateEnv = jinja2.Environment(loader=templateLoader)
                    socket_template = templateEnv.get_template('secure-php-fpm.socket.j2')
                    templateVars = {"PHP_ROOT_PATH": php_backends_dict.get(backend_name)}
                    socket_generated_config = socket_template.render(templateVars)
                    with codecs.open(systemd_socket_file, "w", 'utf-8') as confout:
                        confout.write(socket_generated_config)
                    service_template = templateEnv.get_template('secure-php-fpm.service.j2')
                    service_generated_config = service_template.render(templateVars)
                    with codecs.open(systemd_service_file, "w", 'utf-8') as confout:
                        confout.write(service_generated_config)
                subprocess.call(['systemctl', 'daemon-reload'])
                print('Disabling root owned php-fpm master process:')
                subprocess.call(['systemctl', 'stop', 'ndeploy_backends.service'])
                subprocess.call(['systemctl', 'disable', 'ndeploy_backends.service'])
                if not os.path.isfile(installation_path+"/conf/secure-php-enabled"):
                    os.mknod(installation_path+"/conf/secure-php-enabled")
        elif trigger == "disable-secure-php":
            conf_list = os.listdir("/opt/nDeploy/secure-php-fpm.d")
            for filename in conf_list:
                user, extension = filename.split('.')
                for backend_name in list(php_backends_dict.keys()):
                    subprocess.call(['systemctl', 'stop', backend_name+'@'+user+'.socket'])
                    subprocess.call(['systemctl', 'disable', backend_name+'@'+user+'.socket'])
                    subprocess.call(['killall', '-SIGKILL', 'php-fpm'])
            silentremove(installation_path+"/conf/secure-php-enabled")
            subprocess.call(['systemctl', 'enable', 'ndeploy_backends.service'])
            subprocess.call(['systemctl', 'restart', 'ndeploy_backends.service'])
        # Following is provided to remove legacy Apache PHPFPM selector plugin
        elif trigger == 'httpd-php-uninstall':
            silentremove('/var/cpanel/templates/apache2_4/vhost.local')
            silentremove('/var/cpanel/templates/apache2_4/ssl_vhost.local')
            silentremove(installation_path+'/conf/PHPFPM_SELECTOR_ENABLED')
            subprocess.call(['/scripts/rebuildhttpdconf'], shell=True)
            subprocess.call(['/scripts/restartsrv_httpd'], shell=True)
        elif trigger == 'jailphpfpm':
            if os.path.isfile('/opt/nDeploy/conf/secure-php-enabled'):
                print('php-fpm can be chrooted only if master process is run as root')
                print('Disable  secure-php to setup chrooted php-fpm')
            else:
                if os.path.isdir('/opt/nDeploy/conf/nDeploy-cluster'):
                    subprocess.call(['/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=jaildefaultshell value=1'], shell=True)
                subprocess.call(['/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=jailapache value=1'], shell=True)
                if not os.path.isdir('/var/cpanel/feature_toggles'):
                    os.mkdir('/var/cpanel/feature_toggles')
                subprocess.call(['touch /var/cpanel/feature_toggles/apachefpmjail'], shell=True)
        elif trigger == 'disable-jailphpfpm':
            silentremove('/var/cpanel/feature_toggles/apachefpmjail')
        else:
            return


backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()


parser = argparse.ArgumentParser(description="Start/Stop various nDeploy backends")
parser.add_argument("control_command")
args = parser.parse_args()
trigger = args.control_command
control_php_fpm(trigger)
