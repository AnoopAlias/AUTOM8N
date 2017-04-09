#!/bin/bash
#Author: Anoop P Alias

yum --enablerepo=epel -y install redis
osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
if [ ${osversion} -ge 7 ];then
  systemctl enable redis.service && systemctl start redis.service
else
  service redis start && chkconfig redis on
fi

rpm -q openresty-nDeploy || yum --enablerepo=ndeploy -y install nginx-nDeploy-module-redis2 nginx-nDeploy-module-redis nginx-nDeploy-module-echo nginx-nDeploy-module-set_misc nginx-nDeploy-module-srcache_filter

/opt/nDeploy/scripts/update_profiles.py add root main PHP wpredis_helper.j2 "Wordpress+Redis+nginx-helper"
/opt/nDeploy/scripts/update_profiles.py add root main HHVM wpredis_helper.j2 "Wordpress+Redis+nginx-helper"

/opt/nDeploy/scripts/update_profiles.py add root main PHP wpredis_auto.j2 "Wordpress+Redis"
/opt/nDeploy/scripts/update_profiles.py add root main HHVM wpredis_auto.j2 "Wordpress+Redis"

/opt/nDeploy/scripts/update_profiles.py add root main PHP drupalredis_auto.j2 "Drupal+Redis"
/opt/nDeploy/scripts/update_profiles.py add root main HHVM drupalredis_auto.j2 "Drupal+Redis"

echo -e '\e[93m Additional templates setup: OK \e[0m'
