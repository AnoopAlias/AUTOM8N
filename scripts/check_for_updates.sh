#!/usr/bin/env bash

yum --enablerepo=ndeploy check-update nDeploy*

if [ $? == 100 ]; then
    echo "1" > /opt/nDeploy/conf/NDEPLOY_UPGRADE_STATUS
    echo "Upgrades available!"
else
    echo "0" > /opt/nDeploy/conf/NDEPLOY_UPGRADE_STATUS
    echo "You are up to date!"
fi
