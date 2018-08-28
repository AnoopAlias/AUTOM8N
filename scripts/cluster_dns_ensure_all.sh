#!/bin/bash

echo -e '\e[93m Attempting to regenerate all gdnsd zones  \e[0m'
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);
do
  echo "DNSZoneGen:: $CPANELUSER" && nice --adjustment=15 /opt/nDeploy/scripts/cluster_gdnsd_ensure_user.py $CPANELUSER;
done
