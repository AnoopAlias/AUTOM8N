#!/usr/bin/env bash
#Author: Anoop P Alias

yum --enablerepo=epel -y install borgbackup python3 python3-pip
yum --enablerepo=epel -y install MariaDB-backup
pip3 install borgmatic
mkdir /etc/borgmatic
chmod 750 /etc/borgmatic
touch /etc/borgmatic/excludes
echo 'Setup: Ok'
