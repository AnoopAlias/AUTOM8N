#/bin/bash
#Author: Anoop P Alias

yum --enablerepo=epel -y install borgbackup python36 python36-pip MariaDB-backup
pip3.6 install borgmatic
mkdir /etc/borgmatic
chmod 750 /etc/borgmatic
touch /etc/borgmatic/excludes
echo 'Setup: Ok'
