#!/bin/bash

echo -e '\e[93m Attempting to redo DNS updates  \e[0m'

if [ ! -f /opt/nDeploy/conf/skip_geodns ]; then
  for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);
    do
      echo "DNSZoneGen:: $CPANELUSER" && nice --adjustment=15 /opt/nDeploy/scripts/cluster_gdnsd_ensure_user.py $CPANELUSER;
    done
else
  for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);
    do
      echo "DNSZoneGen:: $CPANELUSER" && nice --adjustment=15 /opt/nDeploy/scripts/cluster_dns_ensure_user.py $CPANELUSER;
    done
fi
