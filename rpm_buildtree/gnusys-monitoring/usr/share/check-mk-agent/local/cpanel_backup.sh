#!/bin/bash
#Author: Anoop P Alias

backup_fail=0
if [ -d /usr/local/cpanel/logs/cpbackup ];then
    grep -rl "Failure" /usr/local/cpanel/logs/cpbackup/ && backup_fail=1
fi

if [ backup_fail -eq 1 ];then
    status=$(grep -rl "Failure" /usr/local/cpanel/logs/cpbackup/)
    echo "2 cpbackup - ${status}"
else
    echo "0 cpbackup - OK"
fi

