#!/bin/bash
#Author : Anoop P Alias

if [ -s /opt/nDeploy/lock/config_generation_queue ]
then
  cat /dev/null > /opt/nDeploy/lock/config_generation_queue_tmp
  cp -p /opt/nDeploy/lock/config_generation_queue /opt/nDeploy/lock/config_generation_queue_tmp
  cat /dev/null > /opt/nDeploy/lock/config_generation_queue
  for CPANELUSER in $(cat /opt/nDeploy/lock/config_generation_queue_tmp|sort|uniq)
  do
	   /opt/nDeploy/scripts/generate_config.py ${CPANELUSER}
  done
fi
