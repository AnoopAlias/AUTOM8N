#!/usr/bin/python

import cgi
import cgitb
import subprocess
import os
import platform
import psutil
import signal

__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

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

if form.getvalue('ddos'):
    try:
        with open(os.devnull, 'w') as FNULL:
            subprocess.call(['systemctl', '--version'], stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError:
        print_error('iptables not compatible')
    else:
        if form.getvalue('ddos') == 'enable':
            if os.path.isfile('/opt/nDeploy/conf/XTENDWEB_FIREHOL_SETUP_LOCK_DO_NOT_REMOVE'):
                subprocess.call('sysctl -w net/ipv4/tcp_syncookies=1', shell=True)
                subprocess.call('sysctl -w net/ipv4/tcp_timestamps=1', shell=True)
                subprocess.call('sysctl -w net/netfilter/nf_conntrack_tcp_loose=0', shell=True)
                subprocess.call('sysctl -w net/netfilter/nf_conntrack_max=2000000', shell=True)
                subprocess.call('echo 2000000 > /sys/module/nf_conntrack/parameters/hashsize', shell=True)
                subprocess.call(['systemctl', 'restart', 'firehol.service'])
                print('<i class="fas fa-thumbs-up"></i> SYNPROXY DDOS Mitigation is now enabled')
            else:
                print_error('FireHol firewall not installed')
                print('					<small class="mb-1">To install run the following command with ansible_port set to sshd port</small><br>')
                print('					<kbd>cd /opt/nDeploy/conf/nDeploy-firewall/</kbd><br>')
                print('					<kbd>ansible-playbook -i ./hosts firewall.yml --extra-vars "ansible_port=22"</kbd><br>')
        elif form.getvalue('ddos') == 'disable':
            if os.path.isfile('/opt/nDeploy/conf/XTENDWEB_FIREHOL_SETUP_LOCK_DO_NOT_REMOVE'):
                subprocess.call(['systemctl', 'stop', 'firehol.service'])
                print_success('SYNPROXY DDOS Mitigation is now disabled')
            else:
                print_error('FireHol firewall not installed')
                print('					<small class="mb-1">To install run the following command with ansible_port set to sshd port</small><br>')
                print('					<kbd>cd /opt/nDeploy/conf/nDeploy-firewall/</kbd><br>')
                print('					<kbd>ansible-playbook -i ./hosts firewall.yml --extra-vars "ansible_port=22"</kbd><br>')
else:
    print_forbidden()

print('</body>')
print('</html>')
