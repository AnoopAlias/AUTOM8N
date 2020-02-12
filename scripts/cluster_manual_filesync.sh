#!/usr/bin/env bash

SSHPORT="22"   #script assumes all slaves have same SSH port settings
SLAVEHOST="slave1.example.com slave2.example.com"

for MYHOST in ${SLAVEHOST}
do
  for dir in $(cat /etc/userdatadomains|awk -F"==" '{print $5}'); do rsync -av -e "ssh -p ${SSHPORT}" ${dir}/ root@${MYHOST}:${dir}/; done
done
