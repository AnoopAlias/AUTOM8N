#!/bin/bash
#Author : Anoop P Alias

##  nDeploy Cluster bootstrap script
##  nDeploy cluster syncs data over ssh and configs using csync2 over port 30865
##  Ensure The ssh ports and port 30865 are whitelisted in your firewall(csf etc). Else Setup will fail!
##  Ensure Mater <=> Slave can login via SSH key based authentication without a passphrase for user root
##  you can do this by running "ssh-copy-id the-other-host" on each server
##  Ensure both hostnames resolve via DNS or you must add both names in /etc/hosts file for local resolution
##  BEGIN settings to edit
#######################################################
MASTERHOST="server1.example.com:sshport"  #This is your master server having cPanel.
SLAVEHOST="slave1.example.com:sshport slave2.example.com:sshport" #This is a space seperated list of slaves including their sshport
SLAVELIST="slave1.example.com slave2.example.com" #This is a space seperated list of slave hostnames.
########################################################
## END settings to edit

#############
##Do not edit anything below this line
##Bootstrapping Python pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python
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
    echo "csync2          30865/tcp               #csync2" >> /etc/services
    ansible ndeploycluster -m shell -a "echo 'csync2          30865/tcp               #csync2' >> /etc/services"


    mastername=$(echo ${MASTERHOST}|cut -d":" -f1)
    masterport=$(echo ${MASTERHOST}|cut -d":" -f2)

    #Setting up csync2
    sed -i -e "s/MASTERSERVER/${mastername}/" -e "s/SLAVESERVERLIST/${SLAVELIST}/" /etc/csync2/csync2.cfg
    ansible ndeploycluster -m synchronize -a "src=/etc/csync2/ dest=/etc/csync2/ recursive=yes archive=yes"
    for slavemc in $(echo ${SLAVELIST})
    do
        slaveshort=$(echo ${slavemc}|cut -d"." -f1)
        mkdir /tmp/${slavemc}
        cp /etc/csync2/csync2.cfg /tmp/${slavemc}/
        sed -e "s/MASTERSERVER/${mastername}/" -e "s/SLAVESERVER/${slavemc}/g" -e "s/GROUPNAME/${slaveshort}/" /opt/nDeploy/conf/csync2.cfg.nginx >> /tmp/${slavemc}/csync2.cfg.nginx
        ansible ${slavemc} -m assemble -a "src=/tmp/${slavemc}/ dest=/etc/csync2/csync2.cfg remote_src=False"
        rm -rf /tmp/${slavemc}
        mkdir /etc/nginx/${slavemc}
    done
    for slavemc in $(echo ${SLAVELIST})
    do
        slaveshort=$(echo ${slavemc}|cut -d"." -f1)
        sed -e "s/MASTERSERVER/${mastername}/" -e "s/SLAVESERVER/${slavemc}/g" -e "s/GROUPNAME/${slaveshort}/" /opt/nDeploy/conf/csync2.cfg.nginx >> /etc/csync2/csync2.cfg
    done

    #Setting up unison and lsyncd
    mkdir /root/.unison
    cat /opt/nDeploy/conf/lsyncd_master.conf > /etc/lsyncd.conf
    n=1
    for slave in $(echo ${SLAVEHOST})
    do
        slavename=$(echo ${slave}|cut -d":" -f1)
        slaveport=$(echo ${slave}|cut -d":" -f2)
        slaveshrtname=$(echo ${slavename}|cut -d"." -f1)
        sed -e "s/SLAVESERVER/${slavename}/g" -e "s/SSHPORT/${slaveport}/g" /opt/nDeploy/conf/default.prf > /root/.unison/${slavename}.prf
        sed -e "s/GROUPNAME/runUnison${n}/" -e "s/SLAVESERVER/${slavename}/" /opt/nDeploy/conf/lsyncd_master.conf.unison >> /etc/lsyncd.conf
        sed -e "s/MASTERSSHPORT/${masterport}/" -e "s/MASTERSERVER/${mastername}/" -e "s/SLAVESERVER/${slavename}/" /opt/nDeploy/conf/lsyncd_slave.conf >> /tmp/${slavename}.lsyncd.conf
        ansible ${slavename} -m copy -a "src=/tmp/${slavename}.lsyncd.conf dest=/etc/lsyncd.conf"
        rm -f /tmp/${slavename}.lsyncd.conf
        n=$(($n+1))
    done

    service xinetd start
    chkconfig xinetd on
    chkconfig csync2 on
    systemctl enable csync2.socket
    systemctl start csync2.socket
    grep csync2 /etc/crontab || echo "* * * * * root /usr/sbin/csync2 -x" >> /etc/crontab
    systemctl restart crond || service crond restart
    /opt/nDeploy/scripts/cluster_home_ensure_all.py
    service lsyncd start
    chkconfig lsyncd on
    systemctl enable lsyncd
    systemctl start lsyncd
    ansible ndeploycluster -m service -a "name=xinetd enabled=yes state=started"
    ansible ndeploycluster -m service -a "name=csync2.socket enabled=yes state=started"
    ansible ndeploycluster -m service -a "name=lsyncd enabled=yes state=started"
    ansible ndeploycluster -m service -a "name=nginx enabled=yes state=started"

    /usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/accountcreate_hook_post.py --category Whostmgr --event Accounts::Create --stage post --manual
    /usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/accountremove_hook_post.py --category Whostmgr --event Accounts::Remove --stage post --manual
else
    echo "Something went wrong in setting up ansible. Aborting setup"
fi
