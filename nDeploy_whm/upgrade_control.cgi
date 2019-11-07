#!/bin/python

import commoninclude
import cgi
import cgitb
import os
import subprocess
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"
update_status_file = installation_path+"/conf/NDEPLOY_UPGRADE_STATUS"

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('upgrade_control'):

    if form.getvalue('upgrade_control') == 'check':

        procExe = subprocess.Popen('echo -e "Checking for updates..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()
        procExe = subprocess.Popen(installation_path+'/scripts/check_for_updates.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procExe.wait()

        # Get upgrade status of nDeploy
        update_status = ''
        if os.path.isfile(update_status_file):
            with open(update_status_file, 'r') as update_status_value:
                update_status = update_status_value.read(1)

        if update_status == '0':
            commoninclude.print_success('You are up to date!')

        elif update_status == '1':
            commoninclude.print_success('Upgrades Available!')

        else:
            commoninclude.print_warning('Issue checking for updates!')

    elif form.getvalue('upgrade_control') == 'reinstall':
        if os.path.isfile(cluster_config_file):

            procExe = subprocess.Popen('echo -e "Reinstalling application cluster-wide..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('yum -y --enablerepo=ndeploy reinstall *nDeploy* && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy reinstall *nDeploy*\" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success('Application has been reinstalled cluster-wide!')

        else:

            procExe = subprocess.Popen('echo -e "Reinstalling application..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('yum -y --enablerepo=ndeploy reinstall *nDeploy* >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success('Application has been reinstalled!')

    elif form.getvalue('upgrade_control') == 'upgrade':
        if os.path.isfile(cluster_config_file):

            procExe = subprocess.Popen('echo -e "Upgrading application cluster-wide..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('yum -y --enablerepo=ndeploy upgrade *nDeploy* && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy upgrade *nDeploy*\" && '+installation_path+'/scripts/attempt_autofix.sh && '+installation_path+'/scripts/check_for_updates.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success('Application has been upgraded cluster-wide!')

        else:

            procExe = subprocess.Popen('echo -e "Upgrading application..." > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()
            procExe = subprocess.Popen('yum -y --enablerepo=ndeploy upgrade *nDeploy* && '+installation_path+'/scripts/attempt_autofix.sh && nginx -t && needs-restarting | grep nginx && service nginx restart && '+installation_path+'/scripts/check_for_updates.sh >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            procExe.wait()

            commoninclude.print_success('Application has been upgraded!')

else:
    commoninclude.print_forbidden()

print_simple_footer()
