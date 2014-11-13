#!/bin/bash

#Change cPanel apache default ports to 80 and 443
sed -i "s/apache_port.*/apache_port=0.0.0.0:80/" /var/cpanel/cpanel.config
sed -i "s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:443/" /var/cpanel/cpanel.config
sed -i "s/9999/80/" /etc/chkserv.d/httpd

#Remove nginx reload hooks
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunAll --stage post --manual
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunUser --stage post --manual

#Remove nginx from  csf pignore
if [ -f /etc/csf/csf.pignore ] ; then
	sed -i '/exe:\/usr\/sbin\/nginx/d' /etc/csf/csf.pignore
fi

#Rebuild apache httpd config and restart the service
/usr/local/cpanel/whostmgr/bin/whostmgr2 --updatetweaksettings > /dev/null
/scripts/rebuildhttpdconf
/usr/local/cpanel/libexec/tailwatchd --restart

