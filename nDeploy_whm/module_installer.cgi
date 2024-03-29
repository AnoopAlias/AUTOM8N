#!/usr/bin/env python3

import cgi
import cgitb
import yaml
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

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('test_cookie') and form.getvalue('geoip2') and form.getvalue('passenger') and form.getvalue('waf'):
    cmd_install = ""
    cmd_uninstall = ""
    if form.getvalue('test_cookie') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):
        cmd_install += "nginx-nDeploy-module-testcookie_access "
    elif form.getvalue('test_cookie') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):
        cmd_uninstall += "nginx-nDeploy-module-testcookie_access "
    if form.getvalue('geoip2') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/geoip2.load'):
        cmd_install += "nginx-nDeploy-module-geoip2 "
    elif form.getvalue('geoip2') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/geoip2.load'):
        cmd_uninstall += "nginx-nDeploy-module-geoip2 "
    if form.getvalue('passenger') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/passenger.load'):
        cmd_install += "nginx-nDeploy-module-passenger "
    elif form.getvalue('passenger') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/passenger.load'):
        cmd_uninstall += "nginx-nDeploy-module-passenger "
    if form.getvalue('waf') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/nemesida.load'):
        cmd_install += "nginx-nDeploy-module-nemesida "
    elif form.getvalue('waf') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/nemesida.load'):
        cmd_uninstall += "nginx-nDeploy-module-nemesida "
    if cmd_install != "" or cmd_uninstall != "":
        if cmd_install == "" and cmd_uninstall != "":
            if os.path.isfile(cluster_config_file):
                terminal_call('yum -y remove '+cmd_uninstall+' && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y remove '+cmd_uninstall+'\"', 'Uninstalling the following modules cluster-wide: '+cmd_uninstall+'...', 'The following modules have been uninstalled cluster-wide: '+cmd_uninstall+'!')
            else:
                terminal_call('yum -y remove '+cmd_uninstall, 'Uninstalling the following modules: '+cmd_uninstall+'...', 'The following modules have been uninstalled cluster-wide: '+cmd_uninstall+'!')
            print_success('Modules uninstalled!')
        elif cmd_install != "" and cmd_uninstall == "":
            if os.path.isfile(cluster_config_file):
                terminal_call('yum -y --enablerepo=ndeploy install '+cmd_install+' && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy install '+cmd_install+'\"', 'Installing the following modules cluster-wide: '+cmd_install+'...', 'The following modules have been installed cluster-wide: '+cmd_install+'!')
            else:
                terminal_call('yum -y --enablerepo=ndeploy install '+cmd_install, 'Installing the following modules: '+cmd_install+'...', 'The following modules have been installed: '+cmd_install+'!')
            print_success('Modules installed!')
        else:
            if os.path.isfile(cluster_config_file):
                terminal_call('yum -y remove '+cmd_uninstall+' && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y remove '+cmd_uninstall+'\"', 'Uninstalling the following modules cluster-wide: '+cmd_uninstall+'...')
                terminal_call('yum -y --enablerepo=ndeploy install '+cmd_install+' && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy install '+cmd_install+'\"', 'Installing the following modules cluster-wide: '+cmd_install+'...', 'Modules installed/uninstalled!')
            else:
                terminal_call('yum -y remove '+cmd_uninstall, 'Uninstalling the following modules: '+cmd_uninstall+'...')
                terminal_call('yum -y --enablerepo=ndeploy install '+cmd_install, 'Installing the following modules cluster-wide: '+cmd_install+'...', 'Modules installed/uninstalled!')
            print_success('Modules installed/uninstalled!')
    else:
        print_warning('Nothing to do.')
else:
    print_forbidden()
print_simple_footer()
