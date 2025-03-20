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
    echo "maxctrl: FAIL" > /var/lib/maxscale/$(/bin/hostname)_maxctrl
  else
    echo "maxctrl: OK" > /var/lib/maxscale/$(/bin/hostname)_maxctrl
  fi
fi
# Check the status of slave nodes
if [ -f /opt/nDeploy/conf/nDeploy-cluster/hosts ] ; then
        ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m fetch -a "src=/var/lib/maxscale/{{ inventory_hostname }}_maxctrl dest=/var/lib/maxscale/{{ inventory_hostname }}_maxctrl flat=yes"
fi
