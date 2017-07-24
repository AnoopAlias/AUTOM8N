#!/bin/bash
#Author: Anoop P Alias

# Settings to change
# Use the remote servers IP in the variable below
REMOTE_SERVER='ip.ip.ip.ip'
# End Settings to change

rsync -av root@${REMOTE_SERVER}:/opt/nDeploy/domain-data/ /opt/nDeploy/domain-data/
rsync -av --exclude=backends.yaml --exclude=nDeploy-cluster --exclude=ndeploy_cluster.yaml root@${REMOTE_SERVER}:/opt/nDeploy/conf/ /opt/nDeploy/conf/
rsync -av root@${REMOTE_SERVER}:/opt/nDeploy/php-fpm.d/ /opt/nDeploy/php-fpm.d/
rsync -av root@${REMOTE_SERVER}:/opt/nDeploy/secure-php-fpm.d/ /opt/nDeploy/secure-php-fpm.d/
rsync -av root@${REMOTE_SERVER}:/opt/nDeploy/hhvm.d/ /opt/nDeploy/hhvm.d/
rsync -av root@${REMOTE_SERVER}:/opt/nDeploy/hhvm.slave.d/ /opt/nDeploy/hhvm.slave.d/
rsync -av --exclude=*.conf --exclude=*.include root@${REMOTE_SERVER}:/etc/nginx/sites-enabled/ /etc/nginx/sites-enabled/
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);do /opt/nDeploy/scripts/fix_domain_data_permission.py $CPANELUSER;done
/opt/nDeploy/scripts/attempt_autofix.sh
echo -e '\e[93m Migration of settings : OK \e[0m'
