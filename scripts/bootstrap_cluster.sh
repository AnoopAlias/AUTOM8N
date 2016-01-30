#!/bin/bash
#Author : Anoop P Alias

##  nDeploy Cluster bootstrap script
##  nDeploy cluster syncs data over ssh and configs using csync2 over port 30865
##  Ensure The ssh ports and port 30865 are whitelisted in your firewall(csf etc). Else Setup will fail!
##  Ensure Mater <=> Slave can login via SSH key based authentication without a passphrase for user root
##  you can do this by running "ssh-copy-id the-other-host" on each server
##  Ensure both hostnames resolve via DNS or you must add both names in /etc/hosts file for local resolution
## This script will work only for a single Master<=>Slave setup. Refer https://support.sysally.net/projects/ndeploy/wiki for
## instructions on setting up on Single Master and multiple slaves
##  BEGIN settings to edit
#######################################################
MASTERHOST="server1.example.com:sshport"  #This is your master server having cPanel.
SLAVEHOST="slave1.example.com:sshport slave2.example.com:sshport" #This is a space seperated list of slaves
########################################################
## END settings to edit

#############
##Do not edit anything below this line
##Bootstrapping Python pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python
pip install --upgrade pipcurl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python
pip install --upgrade pip

##Installing https://github.com/sebastien/cuisine
pip install ansible
pip install --upgrade ansible
if [ $? -eq 0 ];then

    if [ ! -d /etc/ansible ];then mkdir /etc/ansible;fi
    touch /etc/ansible/hosts
    echo "[ndeploycluster]" >> /etc/ansible/hosts
    for slave in $(echo ${SLAVEHOST})
    do
        echo "$slave" >> /etc/ansible/hosts
    done

    yum --enablerepo=ndeploy -y install lsyncd csync2-nDeploy unison-nDeploy
    csync2 -k /etc/csync2/csync2.key

    ansible ndeploycluster -m yum -a "name=epel-release state=present"
    ansible ndeploycluster -m yum -a "name=http://rpm.piserve.com/nDeploy-release-centos-1.0-1.noarch.rpm state=present"
    ansible ndeploycluster -m yum -a "name=lsyncd enablerepo=ndeploy state=present"
    ansible ndeploycluster -m yum -a "name=csync2-nDeploy enablerepo=ndeploy state=present"
    ansible ndeploycluster -m yum -a "name=unison-nDeploy enablerepo=ndeploy state=present"
    ansible ndeploycluster -m yum -a "name=nginx-nDeploy enablerepo=ndeploy state=present"
    ansible ndeploycluster -m yum -a "name=nDeploy-cluster-slave enablerepo=ndeploy state=present"
    ansible ndeploycluster -m shell -a 'sed -i "s/^UMASK/#UMASK/" /etc/login.defs'

    mkdir /root/.unison
    for slave in $(echo ${SLAVEHOST})
    do
        slavename=$(echo ${slave}|cut -d":" -f1)
        slaveport=$(echo ${slave}|cut -d":" -f2)
        mkdir /etc/nginx/${slavename}
        sed -e "s/SLAVESERVER/${slavename}/g" -e "s/SSHPORT/${slaveport}/g" /opt/nDeploy/conf/default.prf > /root/.unison/${slavename}.prf
    done
    ansible ndeploycluster -m copy -a "src=/opt/nDeploy/conf/lsyncd_slave.conf dest=/etc/lsyncd.conf"
    ansible ndeploycluster -m synchronize -a "src=/etc/csync2/ dest=/etc/csync2/ recursive=yes archive=yes"
    rsync -av /opt/nDeploy/conf/lsyncd_master.conf /etc/lsyncd.conf

    /usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/accountcreate_hook_post.py --category Whostmgr --event Accounts::Create --stage post --manual
    /usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/accountremove_hook_post.py --category Whostmgr --event Accounts::Remove --stage post --manual
else
    echo "Something went wrong in setting up ansible. Aborting setup"
fi
