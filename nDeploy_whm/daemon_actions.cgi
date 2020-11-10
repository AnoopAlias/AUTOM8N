#!/usr/bin/env python3

import cgitb
import cgi
import psutil
import os
import platform
import yaml
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
php_secure_mode_file = installation_path+"/conf/secure-php-enabled"

cgitb.enable()
form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('action'):
    if form.getvalue('action') == 'nginxreload':
        if os.path.isfile(cluster_config_file):

            terminal_call('/usr/sbin/nginx -s reload && service nginx status && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"nginx -s reload && service nginx status\"', 'Reloading NGINX cluster-wide...', 'NGINX reload initialized cluster-wide!')
            print_success('NGINX reload initialized cluster-wide!')

        else:

            terminal_call('/usr/sbin/nginx -s reload && service nginx status', 'Reloading NGINX...', 'NGINX reload initialized!')
            print_success('Nginx reload initialized!')

    elif form.getvalue('action') == 'watcherrestart':

        terminal_call('service ndeploy_watcher stop && /bin/rm -f /opt/nDeploy/watcher.pid && service ndeploy_watcher start && service ndeploy_watcher status', 'Reloading Watcher...', 'Watcher reload initialized!')
        print_success('Watcher reload initialized!')

    elif form.getvalue('action') == 'redisflush':
        if os.path.isfile(cluster_config_file):

            terminal_call('/usr/bin/redis-cli FLUSHALL && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"/usr/bin/redis-cli FLUSHALL\" && service redis status', 'Flushing Redis Cache cluster-wide...', 'Redis cache flushed cluster-wide!')
            print_success('Redis cache flushed cluster-wide!')

        else:

            terminal_call('/usr/bin/redis-cli FLUSHALL && service redis status', 'Flushing Redis Cache...', 'Redis Cache flushed!')
            print_success('Redis Cache flushed!')

    elif form.getvalue('action') == 'restart_backends':

        # If not a multi-master PHP setup
        if not os.path.isfile(php_secure_mode_file):
            # This check only detects single master php processes and produces irrelavant data in multi-master mode
            backend_data_yaml = open(backend_config_file, 'r')
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
            backend_data_yaml.close()
            output = ""
            php_status_dict = {}
            if "PHP" in backend_data_yaml_parsed:
                php_backends_dict = backend_data_yaml_parsed["PHP"]
                for php,path in list(php_backends_dict.items()):
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

                for service,status in list(php_status_dict.items()):
                    if status == "NOT ACTIVE":
                        output = output + service+', '
                if output:
                    output = output[:-2] + ' detected down. '

            if os.path.isfile(cluster_config_file):

                terminal_call('service ndeploy_backends restart && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"service ndeploy_backends restart\"', 'Restarting single master PHP backends cluster-wide...', output+'Single master PHP backends restarted cluster-wide!')
                print_success(output+'Single master PHP backends restarted cluster-wide!')

            else:

                terminal_call('service ndeploy_backends restart && service ndeploy_backends status', 'Restarting single master application backends...', output+'Single master PHP backends restarted!')
                print_success(output+'Single master PHP backends restarted!')

        # If multi-master PHP setup
        else:

            if os.path.isfile(cluster_config_file):

                terminal_call('killall -9 php-fpm && /scripts/restartsrv apache_php_fpm && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"killall -9 php-fpm && /scripts/restartsrv apache_php_fpm\"', 'Restarting multi-master PHP backends cluster-wide...', 'Multi-master PHP backends restarted cluster-wide!')
                print_success('Multi-Master PHP backends restarted cluster-wide!')

            else:

                terminal_call('killall -9 php-fpm && /scripts/restartsrv apache_php_fpm', 'Restarting multi-master PHP backends...', 'Multi-master PHP backends restarted!')
                print_success('Multi-Master PHP backends restarted!')

    else:
        print_forbidden()

else:
    print_forbidden()

print_simple_footer()
