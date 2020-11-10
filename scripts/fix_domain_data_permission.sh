#!/usr/bin/env bash

echo -e '\e[93m Attempting to fix domain-data file permission  \e[0m'

for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);
  do
    echo "FixPerm:: $CPANELUSER" && nice --adjustment=15 /opt/nDeploy/scripts/fix_domain_data_permission.py $CPANELUSER;
  done
