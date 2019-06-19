#!/bin/bash

if [ -f /opt/nDeploy/conf/ndeploy_cluster.yaml ]; then
  # We proceed further only if its a zone files
  echo $1 | egrep ".db$" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    DOMAIN=$(echo $1| awk -F"/" '{print $5}'|sed 's/.db$//')
    if (/scripts/whoowns ${DOMAIN} > /dev/null); then
      USER=$(/scripts/whoowns ${DOMAIN})
      /opt/nDeploy/scripts/cluster_gdnsd_ensure_user.py ${USER}
    else
      rsync -a /var/named/${DOMAIN}.db /etc/gdnsd/zones/${DOMAIN}
      chown nobody:nobody /etc/gdnsd/zones/${DOMAIN}
    fi
  fi
fi
