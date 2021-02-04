#!/usr/bin/env bash
#Author: Anoop P Alias
maxctrl_fail=0

if [ -x /usr/bin/maxctrl ]; then
  maxctrl list servers --tsv > /tmp/maxctrl_status
  if [ $(cat /tmp/maxctrl_status|wc -l) -eq 3 ]; then
    cat /tmp/maxctrl_status |awk -F"\t" '{print $5}'|awk 'NR == 1'|grep -w "Master, Running" > /dev/null || maxctrl_fail=1
    cat /tmp/maxctrl_status |awk -F"\t" '{print $5}'|sed '2q;d'|grep -w "Relay Master, Slave, Running" > /dev/null || maxctrl_fail=1
    cat /tmp/maxctrl_status |awk -F"\t" '{print $5}'|awk 'NR == 3'|grep -w "Slave, Running" > /dev/null || maxctrl_fail=1
  else
    cat /tmp/maxctrl_status |awk -F"\t" '{print $5}'|awk 'NR == 1'|grep -w "Master, Running" > /dev/null || maxctrl_fail=1
    cat /tmp/maxctrl_status |awk -F"\t" '{print $5}'|sed '2q;d'|grep -w "Relay Master, Slave, Running" > /dev/null || maxctrl_fail=1
  fi

  if [ $maxctrl_fail -eq 1 ];then
    echo "maxctrl: FAIL" > /home/${hostname}_maxctrl
  else
    echo "maxctrl: OK" > /home/${hostname}_maxctrl
  fi
fi
