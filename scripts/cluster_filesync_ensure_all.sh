#!/bin/bash

echo -e '\e[93m Attempting to sync document roots  \e[0m'

for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);
  do
    echo "FileSync:: $CPANELUSER" && nice --adjustment=15 /opt/nDeploy/scripts/cluster_filesync_ensure_user.py $CPANELUSER;
  done
