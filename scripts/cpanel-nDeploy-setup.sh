#!/bin/bash

function enable {
#####

if [ ! -d /usr/local/rvm/gems/ruby-2.1.3/gems/passenger-4.0.53/ext/nginx ] ; then
	echo -e '\e[93m Setting up rvm ruby and gem required for Phusion Passenger \e[0m'
	sudo gpg2 --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3
	\curl -sSL https://get.rvm.io | sudo bash -s stable --ruby=2.1.3 --gems=passenger
	ln -s /usr/nginx/buildout /usr/local/rvm/gems/ruby-2.1.3/gems/passenger-4.0.53/
	/opt/nDeploy/scripts/update_backend.py RUBY ruby-2.1.3 /usr/local/rvm/wrappers/ruby-2.1.3/ruby
fi
#####

echo -e '\e[93m Modifying apache http and https port in cpanel \e[0m'
sed -i "s/apache_port.*/apache_port=0.0.0.0:9999/" /var/cpanel/cpanel.config
sed -i "s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:4430/" /var/cpanel/cpanel.config
sed -i "s/80/9999/" /etc/chkserv.d/httpd
/usr/local/cpanel/whostmgr/bin/whostmgr2 --updatetweaksettings > /dev/null
/usr/local/cpanel/libexec/tailwatchd --restart
#####

echo -e '\e[93m Adding cpanel stats processing hooks \e[0m'
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunAll --stage post --manual
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunUser --stage post --manual
#####

echo -e '\e[93m Setting up CSF firewall to ignore nginx and nDeploy-backends \e[0m'
if [ -f /etc/csf/csf.pignore ] ; then echo 'exe:/usr/sbin/nginx' >> /etc/csf/csf.pignore ; fi
#####

#Will not be undone
echo -e '\e[93m Setting up default vhost proxy in nginx \e[0m'
cpanelmainip=$(grep ADDR /etc/wwwacct.conf|awk '{print $2}')
sed -i "s/CPANELIP/$cpanelmainip/g" /etc/nginx/conf.d/default_server.conf
sed -i "s/CPANELIP/$cpanelmainip/g" /etc/nginx/conf.d/cpanel_services.conf
#####

echo -e '\e[93m Rebuilding Apache httpd backend configs and restarting daemons \e[0m'
/scripts/rebuildhttpdconf
/scripts/restartsrv http
service nginx restart
service incrond restart
service ndeploy_backends restart
chkconfig nginx on
chkconfig incrond on
chkconfig ndeploy_backends on
#####

echo -e '\e[93m Setting PHPBREW and NVM roots \e[0m'
export PHPBREW_ROOT=/usr/local/phpbrew
echo "export PHPBREW_ROOT=/usr/local/phpbrew" >> /root/.bashrc
export NVM_DIR="/usr/local/nvm"
echo "export NVM_DIR=/usr/local/nvm" >> /root/.bashrc
#####

}

function disable {

#####

echo -e '\e[93m Reverting apache http and https port in cpanel \e[0m'
sed -i "s/apache_port.*/apache_port=0.0.0.0:80/" /var/cpanel/cpanel.config
sed -i "s/apache_ssl_port.*/apache_ssl_port=0.0.0.0:443/" /var/cpanel/cpanel.config
sed -i "s/9999/80/" /etc/chkserv.d/httpd
/usr/local/cpanel/whostmgr/bin/whostmgr2 --updatetweaksettings > /dev/null
/usr/local/cpanel/libexec/tailwatchd --restart
#####

echo -e '\e[93m Deleting cpanel stats processing hooks \e[0m'
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunAll --stage post --manual
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunUser --stage post --manual
#####

echo -e '\e[93m Removing nginx from CSF pignore \e[0m'
if [ -f /etc/csf/csf.pignore ] ; then sed -i '/exe:\/usr\/sbin\/nginx/d' /etc/csf/csf.pignore ; fi
#####

echo -e '\e[93m Rebuilding Apache httpd backend configs.Apache will listen on default ports!  \e[0m'
/scripts/rebuildhttpdconf
/scripts/restartsrv http
service nginx stop
service incrond stop
service ndeploy_backends stop
chkconfig nginx off
chkconfig incrond off
chkconfig ndeploy_backends off
#####
}


case "$1" in
        enable)
            enable
            ;;
         
        disable)
            disable
            ;;
        *)
            echo $"Usage: $0 {enable|disable}"
            exit 1
 
esac
