#!/bin/bash
yum install scl-utils
osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
echo ${osversion}
if [ ${osversion} -eq 6 ];then
	yum -y install http://rpms.remirepo.net/enterprise/remi-release-6.rpm
	for ver in 54 55 56
	do
		yum -y --disableexcludes=main --enablerepo=remi install php$ver php$ver-php-fpm php$ver-php-opcache php$ver-php-mysqlnd php$ver-php-gd php$ver-php-imap php$ver-php-intl php$ver-php-ioncube-loader php$ver-php-xmlrpc php$ver-php-xml php$ver-php-mcrypt php$ver-php-mbstring php$ver-php-ioncube-loader php$ver-php-intl php$ver-php-imap php$ver-php-gd
		sed "s/CPANELUSER/nobody/g" /opt/nDeploy/conf/php-fpm.pool.tmpl > /opt/remi/php$ver/root/etc/php-fpm.d/www.conf
		ln -s /opt/remi/php$ver/root/usr/sbin/php-fpm /opt/remi/php$ver/root/sbin/php-fpm
		ln -s /opt/remi/php$ver/root/etc/php-fpm.d /opt/remi/php$ver/root/usr/etc/php-fpm.d
		ln -s /opt/remi/php$ver/root/var /opt/remi/php$ver/root/usr/var
		/opt/nDeploy/scripts/update_backend.py PHP PHP$ver /opt/remi/php$ver/root
		/etc/init.d/ndeploy_backends stop
		/etc/init.d/ndeploy_backends start
		chkconfig ndeploy_backends on
	done
elif [ ${osversion} -eq 7 ];then
	yum -y install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
	for ver in 54 55 56
	do
		yum -y --disableexcludes=main --enablerepo=remi install php$ver php$ver-php-fpm php$ver-php-opcache php$ver-php-mysqlnd php$ver-php-gd php$ver-php-imap php$ver-php-intl php$ver-php-ioncube-loader php$ver-php-xmlrpc php$ver-php-xml php$ver-php-mcrypt php$ver-php-mbstring php$ver-php-ioncube-loader php$ver-php-intl php$ver-php-imap php$ver-php-gd
		sed "s/CPANELUSER/nobody/g" /opt/nDeploy/conf/php-fpm.pool.tmpl > /opt/remi/php$ver/root/etc/php-fpm.d/www.conf
		ln -s /opt/remi/php$ver/root/usr/sbin/php-fpm /opt/remi/php$ver/root/sbin/php-fpm
		ln -s /opt/remi/php$ver/root/etc/php-fpm.d /opt/remi/php$ver/root/usr/etc/php-fpm.d
		ln -s /opt/remi/php$ver/root/var /opt/remi/php$ver/root/usr/var
		/opt/nDeploy/scripts/update_backend.py PHP PHP$ver /opt/remi/php$ver/root
		systemctl stop ndeploy_backends
		systemctl start ndeploy_backends
		systemctl enable ndeploy_backends
	done
else
	echo "ERROR: Unknown OS Version detected. Aborting Install "
fi
