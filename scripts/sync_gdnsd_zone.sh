#!/bin/bash

if [ -f /opt/nDeploy/conf/ndeploy_cluster.yaml ]; then
  # We proceed further only if its a zone files
  echo $1 | egrep ".db$" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    DOMAIN=$(echo $1| awk -F"/" '{print $5}'|sed 's/.db$//')
    USER=$(/scripts/whoowns ${DOMAIN})
    /opt/nDeploy/scripts/cluster_gdnsd_ensure_user.py ${USER}
  fi
fi
