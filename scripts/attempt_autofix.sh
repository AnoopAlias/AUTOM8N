#!/bin/bash

# Remove all .conf files if force argument is supplied
if [ "$#" -eq 1 ] && [ "$1" == "force" ] ; then
  rm -f /etc/nginx/sites-enabled/*.conf
fi

##Attempt to re-generate all nginx config
touch /opt/nDeploy/conf/skip_nginx_reload
touch /opt/nDeploy/conf/skip_php-fpm_reload

echo -e '\e[93m Attempting to regenerate all nginx conf  \e[0m'
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);do echo "ConfGen:: $CPANELUSER" && nice --adjustment=15 /opt/nDeploy/scripts/generate_config.py $CPANELUSER;done

rm -f /opt/nDeploy/conf/skip_nginx_reload /opt/nDeploy/conf/skip_php-fpm_reload

echo -e '\e[93m Attempting to regenerate  nginx default conf  \e[0m'
/opt/nDeploy/scripts/generate_default_vhost_config.py

# Reloading nginx
/usr/sbin/nginx -s reload

# Getting the OS release version
osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)

if [ ! -f /opt/nDeploy/conf/secure-php-enabled ] ; then
  ##Attempt to fix backends issue
  echo -e '\e[93m Attempting to restart all backend Application servers \e[0m'
  if [ ${osversion} -le 6 ];then
  	service ndeploy_backends restart
  else
  	systemctl restart ndeploy_backends
  fi
else
  kill -9 $(ps aux|grep php-fpm|grep secure-php-fpm.d|grep -v grep|awk '{print $2}')
fi

echo -e '\e[93m The following PHP-FPM master process has started \e[0m'

for pid in $(pidof php-fpm)
do
    lsof -p $pid | grep txt | awk '{print $1,$2,$3,$9}'
done


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
