#!/bin/bash

echo -e '\e[93m ########################################################################### \e[0m'
echo -e '\e[93m #                     !!! Warning !!!                                     # \e[0m'
echo -e '\e[93m #     Switching template is done on a best effort basis                   # \e[0m'
echo -e '\e[93m #               100% accuracy not guarenteed                              # \e[0m'
echo -e '\e[93m ########################################################################### \e[0m'


service ndeploy_watcher stop
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1)
do
  echo "Auto ConfGen:: $CPANELUSER" && /opt/nDeploy/scripts/auto_config.py $CPANELUSER
done
kill -USR1 $(cat /var/run/nginx.pid)
/opt/nDeploy/scripts/attempt_autofix.sh
