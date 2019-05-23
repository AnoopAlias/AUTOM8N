#/bin/bash
#Author: Anoop P Alias

echo -e '\e[93m Installing borg and borgmatic \e[0m'
yum --enablerepo=epel -y install borgbackup python36 python36-pip MariaDB-backup
pip3.6 install borgmatic
mkdir /etc/borgmatic
chmod 750 /etc/borgmatic
echo -e '\e[93m Setup: Ok \e[0m'
