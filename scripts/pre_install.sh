#!/bin/bash

#Change cPanel apache default ports to what nDeploy expects
sed -i "s/apache_port.*/apache_port=0.0.0.0:9999/" /var/cpanel/cpanel.config
sed -i "s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:4430/" /var/cpanel/cpanel.config
sed -i "s/80/9999/" /etc/chkserv.d/httpd

#Add nginx reload hooks
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunAll --stage post --manual
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunUser --stage post --manual

#Add nginx to csf pignore
if [ -f /etc/csf/csf.pignore ] ; then
	echo 'exe:/usr/sbin/nginx' >> /etc/csf/csf.pignore
fi

#Rebuild apache httpd config and restart the service
/usr/local/cpanel/whostmgr/bin/whostmgr2 --updatetweaksettings > /dev/null
/scripts/rebuildhttpdconf
/usr/local/cpanel/libexec/tailwatchd --restart

