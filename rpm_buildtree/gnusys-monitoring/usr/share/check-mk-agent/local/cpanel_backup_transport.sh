#!/bin/bash
#Author: Anoop P Alias


transport_fail=0
if [ -d /usr/local/cpanel/logs/cpbackup_transporter ];then
    grep -rl "failed" /usr/local/cpanel/logs/cpbackup_transporter/ > /dev/null && transport_fail=1
fi

if [ $transport_fail -eq 1 ];then
    status=$(grep -rl "failed" /usr/local/cpanel/logs/cpbackup_transporter/|tr '\n' ' ')
    echo "2 cpbackup_transport - ${status}"
else
    echo "0 cpbackup_transport - OK"
fi
