#!/bin/bash

##Attempt to re-generate all nginx config
/bin/touch /opt/nDeploy/conf/skip_nginx_reload
/bin/touch /opt/nDeploy/conf/skip_php-fpm_reload
/bin/touch /opt/nDeploy/conf/skip_tomcat_reload

# Try removing any stale config
for vhost in $(find /etc/nginx/sites-enabled/ -iname "*.conf" -exec basename {} .conf \;)
do
  cpvhost=$(echo ${vhost}|sed 's/_wildcard_/\*/')
  grep -w "^${cpvhost}:" /etc/userdatadomains > /dev/null
  if [ $? -ne 0 ] ; then
    rm -f /etc/nginx/sites-enabled/${vhost}.*
    if [ -f /opt/nDeploy/conf/ndeploy_cluster.yaml ]; then
      for slavehost in $(cat /opt/nDeploy/conf/ndeploy_cluster.yaml |grep -v "^ "|cut -d: -f1)
      do
        rm -f /etc/nginx/${slavehost}/${vhost}.*
      done
    fi
  fi
done

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

/bin/rm -f /opt/nDeploy/conf/skip_nginx_reload /opt/nDeploy/conf/skip_php-fpm_reload /opt/nDeploy/conf/skip_tomcat_reload

echo -e '\e[93m Attempting to regenerate  nginx default conf  \e[0m'
/opt/nDeploy/scripts/generate_default_vhost_config.py
if [ -f /opt/nDeploy/conf/ndeploy_cluster.yaml ]; then
  /opt/nDeploy/scripts/update_nginx_status_allow.py
fi

# Fixing RPM state
if [ -f /etc/cpanel/ea4/is_ea4 ];then
	echo -e '\e[93m !!! Removing conflicting mod_evasive ea-apache24-mod_evasive ea-apache24-mod_ruid2 ea-apache24-mod_http2 rpm \e[0m'
	yum -y remove ea-apache24-mod_ruid2 ea-apache24-mod_http2 ea-apache24-mod_evasive mod_evasive
	yum -y install ea-apache24-mod_remoteip
fi

# Reloading nginx
service nginx reload

# Getting the OS release version
osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)

##Restart ndeploy_watcher
echo -e '\e[93m Attempting to restart ndeploy_watcher daemon \e[0m'
if [ ${osversion} -le 6 ];then
  service ndeploy_watcher stop
  /bin/rm -f /opt/nDeploy/watcher.pid
  service ndeploy_watcher start
else
  systemctl stop ndeploy_watcher
  /bin/rm -f /opt/nDeploy/watcher.pid
  systemctl start ndeploy_watcher
fi
