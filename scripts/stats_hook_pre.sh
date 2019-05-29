#!/bin/bash

if [ -f /opt/nDeploy/conf/CLUSTER_LOG ] && [ -f /opt/nDeploy/conf/ndeploy_cluster.yaml ]; then
  # Sync the domlogs from the slaves
  /usr/bin/ansible-playbook -i /opt/nDeploy/conf/nDeploy-cluster/hosts /opt/nDeploy/conf/nDeploy-cluster/hosts /opt/nDeploy/conf/nDeploy-cluster/stats_download.yml
  for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);
  do
    /opt/nDeploy/scripts/stats_hook_logmerge.py $CPANELUSER
  done
fi
