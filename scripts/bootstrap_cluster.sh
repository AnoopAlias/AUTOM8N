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
MASTERHOSTNAME="server1.example.com"  #This is your master server having cPanel. This server must have CentOS7 or higher OS
MASTERIP="192.168.1.1"   #you can use your servers mainIP here or LAN-IP if you are clustering over a LAN
MASTERSSHPORT="22"  #Cannot be Blank. Use 22 if its default

SLAVEHOSTNAME="slave.example.com"   #This is your slave server preferably running a cPanel DNS only . This server must have CentOS7 or higher OS
SLAVEIP="192.168.1.2"  #you can use your servers mainIP here or LAN-IP if you are clustering over a LAN
SLAVESSHPORT="22"   #Cannot be Blank. Use 22 if its default
########################################################
## END settings to edit

#############
##Do not edit anything below this line
##Bootstrapping Python pip
curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python
pip install --upgrade pipcurl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python
pip install --upgrade pip

##Installing https://github.com/sebastien/cuisine
pip install cuisine
if [ $? -eq 0 ];then
    /opt/nDeploy/scripts/ndeploy_cluster_setup.py ${MASTERHOSTNAME}::${MASTERIP}:${MASTERSSHPORT} ${SLAVEHOSTNAME}::${SLAVEIP}:${SLAVESSHPORT}
else
    echo "Something went wrong in setting up python cuisine!. Aborting setup"
fi
