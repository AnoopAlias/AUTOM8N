#!/usr/bin/env python3

import cgi
import cgitb
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_warning, print_forbidden


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Production"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
update_status_file = installation_path+"/conf/NDEPLOY_UPGRADE_STATUS"

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('upgrade_control'):

    if form.getvalue('upgrade_control') == 'check':

        terminal_call(installation_path+'/scripts/check_for_updates.sh', 'Checking for updates...')

        # Get upgrade status of nDeploy
        update_status = ''
        if os.path.isfile(update_status_file):
            with open(update_status_file, 'r') as update_status_value:
                update_status = update_status_value.read(1)

        if update_status == '0':
            print_success('You are up to date!')

        elif update_status == '1':
            print_success('Upgrades Available!')

        else:
            print_warning('Issue checking for updates!')

    elif form.getvalue('upgrade_control') == 'reinstall':
        if os.path.isfile(cluster_config_file):

            terminal_call('yum -y --enablerepo=ndeploy reinstall *nDeploy*', 'Reinstalling application on Master...', 'Reinstalling application cluster-wide...')
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy reinstall *nDeploy*\"', '', 'Application has been reinstalled cluster-wide!')
            terminal_call(installation_path+'/scripts/check_for_updates.sh', '', 'Checking for updates...')
            print_success('Application has been reinstalled cluster-wide!')

        else:

            terminal_call('yum -y --enablerepo=ndeploy reinstall *nDeploy*', 'Reinstalling application...', 'Application has been reinstalled!')
            terminal_call(installation_path+'/scripts/check_for_updates.sh', '', 'Checking for updates...')
            print_success('Application has been reinstalled!')

    elif form.getvalue('upgrade_control') == 'upgrade':
        if os.path.isfile(cluster_config_file):

            terminal_call('yum -y --enablerepo=ndeploy upgrade *nDeploy*', 'Upgrading application on Master...', 'Upgrading application cluster-wide...')
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy upgrade *nDeploy*\"', '', 'Application has been upgraded cluster-wide!')
            terminal_call(installation_path+'/scripts/attempt_autofix.sh', '', 'Running AutoFix...')
            terminal_call(installation_path+'/scripts/check_for_updates.sh', '', 'Checking for updates...')
            print_success('Application has been upgraded cluster-wide!')

        else:

            terminal_call('yum -y --enablerepo=ndeploy upgrade *nDeploy*', 'Upgrading application...', 'Application has been upgraded!')
            terminal_call(installation_path+'/scripts/attempt_autofix.sh', '', 'Running AutoFix...')
            terminal_call('nginx -t && needs-restarting | grep nginx && service nginx restart', '', 'Reloading Nginx...')
            terminal_call(installation_path+'/scripts/check_for_updates.sh', '', 'Checking for updates...')
            print_success('Application has been upgraded!')

else:
    print_forbidden()

print_simple_footer()
