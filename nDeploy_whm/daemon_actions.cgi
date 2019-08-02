#!/usr/bin/env python

import commoninclude
import cgitb
import subprocess
import cgi
import psutil
import os
import platform
import signal

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
xtendweb_installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cgitb.enable()
form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('</head>')
print('<body>')

if form.getvalue('action'):
    if form.getvalue('action') == 'nginxreload':
        if os.path.isfile(cluster_config_file):
            the_raw_cmd = '/usr/sbin/nginx -s reload && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"nginx -s reload\"'
        else:
            the_raw_cmd = '/usr/sbin/nginx -s reload;systemctl is-active --quiet nginx && echo NGINX has been reloaded and is active.'
    elif form.getvalue('action') == 'watcherrestart':
        the_raw_cmd = 'service ndeploy_watcher stop && /bin/rm -f /opt/nDeploy/watcher.pid && service ndeploy_watcher start'
    elif form.getvalue('action') == 'redisflush':
        the_raw_cmd = 'redis-cli FLUSHALL'
    else:
        commoninclude.print_forbidden()
        the_raw_cmd = 'echo ""'
    run_cmd = subprocess.Popen(the_raw_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    print('<samp>')
    while True:
        line = run_cmd.stdout.readline()
        if not line:
            break
        print('<li class="mb-2"><samp>'+line+'</samp></li><hr>')
    print('</samp>')
else:
    commoninclude.print_forbidden()
print('</body>')
print('</html>')
