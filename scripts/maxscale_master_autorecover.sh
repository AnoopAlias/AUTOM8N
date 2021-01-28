#!/usr/bin/env bash
#Author: Anoop P Alias
maxctrl_fail=0

if [ -x /usr/bin/maxctrl ]; then
  maxctrl list servers --tsv > /tmp/maxctrl_status_master
  cat /tmp/maxctrl_status_master |awk -F"\t" '{print $5}'|awk 'NR == 1'|grep -w "Master, Running" > /dev/null || maxctrl_fail=1
fi
if [ $maxctrl_fail -eq 1 ];then
  mysql --defaults-file=/root/.my.cnf -e "STOP SLAVE;"
fi
