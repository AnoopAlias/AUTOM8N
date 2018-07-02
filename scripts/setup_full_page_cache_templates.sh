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

if [ -f /opt/nDeploy/scripts/update_profiles.py ];then
  /opt/nDeploy/scripts/update_profiles.py add root main PHP wpredis_helper.j2 "Wordpress-FullPage-Cache+nginx-helper"
  /opt/nDeploy/scripts/update_profiles.py del root main PHP wpredis_helper_cluster.j2 "Wordpress-FullPage-Cache+nginx-helper(cluster)"
  /opt/nDeploy/scripts/update_profiles.py add root main HHVM wpredis_helper.j2 "Wordpress-FullPage-Cache+nginx-helper"
  /opt/nDeploy/scripts/update_profiles.py del root main HHVM wpredis_helper_cluster.j2 "Wordpress-FullPage-Cache+nginx-helper(cluster)"

  /opt/nDeploy/scripts/update_profiles.py add root main PHP wpredis_auto.j2 "Wordpress-FullPage-Cache"
  /opt/nDeploy/scripts/update_profiles.py add root main HHVM wpredis_auto.j2 "Wordpress-FullPage-Cache"
  /opt/nDeploy/scripts/update_profiles.py del root main PHP wpredis_auto_cluster.j2 "Wordpress-FullPage-Cache(cluster)"
  /opt/nDeploy/scripts/update_profiles.py del root main HHVM wpredis_auto_cluster.j2 "Wordpress-FullPage-Cache(cluster)"

  /opt/nDeploy/scripts/update_profiles.py add root main PHP drupalredis_auto.j2 "Drupal-FullPage-Cache"
  /opt/nDeploy/scripts/update_profiles.py add root main HHVM drupalredis_auto.j2 "Drupal-FullPage-Cache"
  /opt/nDeploy/scripts/update_profiles.py del root main PHP drupalredis_auto_cluster.j2 "Drupal-FullPage-Cache(cluster)"
  /opt/nDeploy/scripts/update_profiles.py del root main HHVM drupalredis_auto_cluster.j2 "Drupal-FullPage-Cache(cluster)"
fi

echo -e '\e[93m FullPage cache templates setup: OK \e[0m'
