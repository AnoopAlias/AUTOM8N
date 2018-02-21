#!/bin/bash

# Remove all .conf files if force argument is supplied
if [ "$#" -eq 1 ] && [ "$1" == "force" ] ; then
  rm -f /etc/nginx/sites-enabled/*.conf
fi

##Attempt to re-generate all nginx config
touch /opt/nDeploy/conf/skip_nginx_reload
touch /opt/nDeploy/conf/skip_php-fpm_reload
touch /opt/nDeploy/conf/skip_tomcat_reload

echo -e '\e[93m Attempting to regenerate all nginx conf  \e[0m'
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);
do
  echo "ConfGen:: $CPANELUSER" && nice --adjustment=15 /opt/nDeploy/scripts/generate_config.py $CPANELUSER;
done

if [ ! -f /opt/nDeploy/conf/secure-php-enabled -a -f /var/cpanel/feature_toggles/apachefpmjail ] ; then
  echo -e '\e[93m Attempting to fix PHP Chrooted environment  \e[0m'
  /opt/nDeploy/scripts/init_backends.py autofix
  echo -e '\e[93m Please set all users to JailShell for chrooted php-fpm \e[0m'
  echo -e '\e[93m Run "/opt/nDeploy/scripts/init_backends.py autofix" on slaves in XtendWeb cluster \e[0m'
fi

rm -f /opt/nDeploy/conf/skip_nginx_reload /opt/nDeploy/conf/skip_php-fpm_reload /opt/nDeploy/conf/skip_tomcat_reload

echo -e '\e[93m Attempting to regenerate  nginx default conf  \e[0m'
/opt/nDeploy/scripts/generate_default_vhost_config.py

# Reloading nginx
/usr/sbin/nginx -s reload

# Getting the OS release version
osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)

##Restart ndeploy_watcher
echo -e '\e[93m Attempting to restart ndeploy_watcher daemon \e[0m'
if [ ${osversion} -le 6 ];then
  service ndeploy_watcher stop
  rm -f /opt/nDeploy/watcher.pid
  service ndeploy_watcher start
else
  systemctl stop ndeploy_watcher
  rm -f /opt/nDeploy/watcher.pid
  systemctl start ndeploy_watcher
fi
