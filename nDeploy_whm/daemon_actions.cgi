#!/usr/bin/env python

import commoninclude
import cgitb
import subprocess
import cgi
import psutil
import os
import platform
import signal
import yaml
from commoninclude import print_simple_header, print_simple_footer



__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cgitb.enable()
form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('action'):
    if form.getvalue('action') == 'nginxreload':
        if os.path.isfile(cluster_config_file):

            procExe = subprocess.Popen('echo -e "Reloading NGINX cluster-wide..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('/usr/sbin/nginx -s reload && service nginx status && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"nginx -s reload && service nginx status\" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('echo -e "NGINX reload initialized cluster-wide..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success('NGINX reload initialized cluster-wide!')

        else:

            procExe = subprocess.Popen('echo -e "Reloading NGINX..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('/usr/sbin/nginx -s reload && service nginx status >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('echo -e "NGINX reload initialized..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success('Nginx reload initialized!')

    elif form.getvalue('action') == 'watcherrestart':

        procExe = subprocess.Popen('echo -e "Reloading Watcher..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('service ndeploy_watcher stop && /bin/rm -f /opt/nDeploy/watcher.pid && service ndeploy_watcher start && service ndeploy_watcher status >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen('echo -e "Watcher reload initialized..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        commoninclude.print_success('Watcher reload initialized!')

    elif form.getvalue('action') == 'redisflush':
        if os.path.isfile(cluster_config_file):

            procExe = subprocess.Popen('echo -e "Flushing Redis cache cluster-wide..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('/usr/bin/redis-cli FLUSHALL && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"/usr/bin/redis-cli FLUSHALL\" && service redis status >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('echo -e "Redis cache flushed cluster-wide..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success('Redis cache flushed cluster-wide!')

        else:

            procExe = subprocess.Popen('echo -e "Flushing Redis cache..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('/usr/bin/redis-cli FLUSHALL && service redis status >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('echo -e "Redis cache flushed..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success('Redis Cache flushed!')

    elif form.getvalue('action') == 'restart_backends':

        backend_data_yaml = open(backend_config_file, 'r')
        backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
        backend_data_yaml.close()

        # This check only detects single master php processes and produces irrelavant data in multi-master mode
        output = ""
        if not os.path.isfile(cluster_config_file):
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

            procExe = subprocess.Popen('echo -e "Restarting application backends..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('service ndeploy_backends restart && service ndeploy_backends status >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('echo -e "'+output+'Application backends restarted..." >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success(output+'Application backends restarted!')

        else: 
            commoninclude.print_warning('Cannot restart PHP Backends in socket mode.')

    else:
        commoninclude.print_forbidden()

else:
    commoninclude.print_forbidden()

print_simple_footer()
