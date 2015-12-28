#!/usr/bin/env python

import yaml
import os
import sys
import argparse
import subprocess
import re
import cuisine
import pwd


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup nDeploy cluster")
    parser.add_argument("MASTERDATA")
    parser.add_argument("SLAVEDATA")
    args = parser.parse_args()
    slavedata = args.SLAVEDATA
    masterdata = args.MASTERDATA
    masterserver, masterip = masterdata.split(":")
    slaveserver, slaveip = slavedata.split(":")
    if is_valid_hostname(masterserver):
        pass
    else:
        print("The hostname of master: "+masterserver+" is invalid")
        sys.exit(1)
    if is_valid_hostname(slaveserver):
        pass
    else:
        print("The hostname of slave: "+slaveserver+" is invalid ")
        sys.exit(1)
    print("Installing csync2,unison and lsyncd")
    subprocess.call('yum --enablerepo=ndeploy -y install lsyncd csync2-nDeploy unison-nDeploy', shell=True)
    sed_cmd1 = 'sed -i "s/MASTERSERVER/'+masterserver+'/g" /etc/csync2/csync2.cfg'
    sed_cmd2 = 'sed -i "s/SLAVESERVER/'+slaveserver+'/g" /etc/csync2/csync2.cfg'
    subprocess.call(sed_cmd1, shell=True)
    subprocess.call(sed_cmd2, shell=True)
    cuisine.connect(slaveserver)
    cuisine.run("yum --enablerepo=ndeploy -y install lsyncd csync2-nDeploy unison-nDeploy nginx-nDeploy")
    subprocess.call('csync2 -k /etc/csync2/csync2.key', shell=True)
    cuisine.rsync("/etc/csync2/", "/etc/csync2/")
    if not os.path.isdir("/root/.unison"):
        os.mkdir("/root/.unison")
    sed_cmd3 = 'sed "s/SLAVESERVER/'+slaveserver+'/g" '+installation_path+'/conf/default.prf > /root/.unison/default.prf'
    subprocess.call(sed_cmd3, shell=True)
    rsync_cmd1 = 'rsync -av '+installation_path+'/conf/lsyncd_master.conf /etc/lsyncd.conf'
    subprocess.call(rsync_cmd1, shell=True)
    sed_cmd4 = 'sed "s/MASTERSERVER/'+masterserver+'/g" '+installation_path+'/conf/lsyncd_slave.conf > /tmp/nDeploy_lsyncd.conf'
    subprocess.call(sed_cmd4, shell=True)
    cuisine.rsync("/tmp/nDeploy_lsyncd.conf", "/etc/lsyncd.conf")
    os.remove("/tmp/nDeploy_lsyncd.conf")
    with open("/etc/domainusers", 'r') as domainusers:
        for line in domainusers:
            cpaneluser, domain = line.split(":")
            user_info = pwd.getpwnam(cpaneluser)
            cpaneluserhome = user_info.pw_dir
            cuisine.user_ensure_linux(cpaneluser, home=cpaneluserhome)
    if not os.path.isdir("/etc/nginx/"+slaveserver):
        os.mkdir("/etc/nginx/"+slaveserver)
    cuisine.dir_ensure("/etc/nginx/"+slaveserver)
    filecontent = cuisine.file_read('/etc/nginx/conf.d/custom_include.conf')
    if not re.search('include /etc/nginx/'+slaveserver+'/\*.conf;', filecontent, re.MULTILINE):
        cuisine.file_append("/etc/nginx/conf.d/custom_include.conf", "include /etc/nginx/"+slaveserver+"/*.conf;\n")
    subprocess.call('systemctl enable  csync2.socket', shell=True)
    subprocess.call('systemctl start csync2.socket', shell=True)
    cuisine.run('systemctl enable  csync2.socket')
    cuisine.run('systemctl start csync2.socket')
    # Do a Manual csync2 sync
    subprocess.call("/usr/sbin/csync2 -xv", shell=True)
    subprocess.call('grep "/usr/sbin/csync2" /etc/crontab || echo "* * * * * root /usr/sbin/csync2 -x" >> /etc/crontab', shell=True)
    subprocess.call('systemctl restart crond.service', shell=True)
    subprocess.call('systemctl enable  lsyncd.service', shell=True)
    subprocess.call('systemctl start lsyncd.service', shell=True)
    cuisine.run('systemctl enable  lsyncd.service')
    cuisine.run('systemctl start lsyncd.service')
    cuisine.run('systemctl enable nginx.service')
    cuisine.run('systemctl start nginx.service')
    # Creating the cluster config file
    mydict = {slaveserver: {'connect': slaveip, 'ipmap': {masterip: slaveip}}}
    with open(installation_path+'/conf/ndeploy_cluster.yaml', 'w') as cluster_conf:
        cluster_conf.write(yaml.dump(mydict, default_flow_style=True))
    # Doing the initial unison sync of /home
    subprocess.Popen('/usr/bin/unison', shell=True)
