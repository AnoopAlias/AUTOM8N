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
            the_raw_cmd = '/usr/sbin/nginx -s reload'
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
