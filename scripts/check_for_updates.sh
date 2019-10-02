#!/bin/bash

yum --enablerepo=ndeploy check-update *nDeploy*

if [ $? == 100 ]; then
    echo "1" > /opt/nDeploy/conf/NDEPLOY_UPGRADE_STATUS
    echo "You've got nDeploy updates available!"
else
    echo "0" > /opt/nDeploy/conf/NDEPLOY_UPGRADE_STATUS
    echo "No nDeploy updates detected..."
fi
