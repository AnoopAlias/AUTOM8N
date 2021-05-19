#!/usr/bin/env bash

if [ -f /opt/nDeploy/conf/ndeploy_cluster.yaml ];then
  for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);
  do
    HOMEDIR=$( getent passwd "${CPANELUSER}" | cut -d: -f6 )
    if [ -d ${HOMEDIR}/.ssh ]; then
      /usr/bin/ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m synchronize -a "src=${HOMEDIR}/.ssh/ dest=${HOMEDIR}/.ssh/ rsync_timeout=5"
    fi
  done
fi
