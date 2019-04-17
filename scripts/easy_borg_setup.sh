#/bin/bash
#Author: Anoop P Alias

echo -e '\e[93m Installing borg and borgmatic \e[0m'
yum --enablerepo=epel -y install borgmatic borgbackup python36-pip
pip3.6 install 'ruamel.yaml<=0.15'
pip3.6 install 'pykwalify>=1.6.0'
