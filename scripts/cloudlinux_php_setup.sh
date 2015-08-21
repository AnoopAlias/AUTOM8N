#!/bin/bash
wget -O /tmp/phpversion.hint http://rpm.piserve.com/phpversion.hint

#Compile PHP54 
compile_php54(){

php54_ver=$(cat /tmp/phpversion.hint|grep "^5.4")
echo "Compiling .... ${php54_ver}"
wget -O /usr/local/src/php-${php54_ver}.tar.bz2 http://us2.php.net/distributions/php-${php54_ver}.tar.bz2
tar -xvjf /usr/local/src/php-${php54_ver}.tar.bz2 -C /usr/local/src/
wget -O /usr/local/src/cl-apache-patches.tar.gz http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz
cd /usr/local/src/php-${php54_ver}
tar -xvzf /usr/local/src/cl-apache-patches.tar.gz fpm-lve-php5.4_autoconf.patch 
patch -p1 --fuzz=10 < fpm-lve-php5.4_autoconf.patch
autoconf
config_args=$(php-config --configure-options|sed "s/--prefix=\/usr\/local //;s/--with-apxs2=\/usr\/local\/apache\/bin\/apxs//;s/--with-config-file-path=\/usr\/local\/lib//;s/--with-config-file-scan-dir=\/usr\/local\/lib\/php\.ini\.d//")
./configure ${config_args} --enable-fpm --prefix=/usr/local/php54_fpm
make
make install
cd -
rm -rf /usr/local/src/php-${php54_ver} /usr/local/src/php-${php54_ver}.tar.bz2 /usr/local/src/cl-apache-patches.tar.gz
/opt/nDeploy/scripts/update_backend.py PHP PHP54_LVE /usr/local/php54_fpm
}

#Compile PHP55
compile_php55(){

php55_ver=$(cat /tmp/phpversion.hint|grep "^5.5")
echo "Compiling .... ${php55_ver}"
wget -O /usr/local/src/php-${php55_ver}.tar.bz2 http://us2.php.net/distributions/php-${php55_ver}.tar.bz2
tar -xvjf /usr/local/src/php-${php55_ver}.tar.bz2 -C /usr/local/src/
wget -O /usr/local/src/cl-apache-patches.tar.gz http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz
cd /usr/local/src/php-${php55_ver}
tar -xvzf /usr/local/src/cl-apache-patches.tar.gz fpm-lve-php5.5_autoconf.patch
patch -p1 --fuzz=10 < fpm-lve-php5.5_autoconf.patch
autoconf
config_args=$(php-config --configure-options|sed "s/--prefix=\/usr\/local //;s/--with-apxs2=\/usr\/local\/apache\/bin\/apxs//;s/--with-config-file-path=\/usr\/local\/lib//;s/--with-config-file-scan-dir=\/usr\/local\/lib\/php\.ini\.d//")
./configure ${config_args} --enable-fpm --enable-opcache --prefix=/usr/local/php55_fpm
make
make install
cd -
rm -rf /usr/local/src/php-${php55_ver} /usr/local/src/php-${php55_ver}.tar.bz2 /usr/local/src/cl-apache-patches.tar.gz
/opt/nDeploy/scripts/update_backend.py PHP PHP55_LVE /usr/local/php55_fpm
}

#Compile PHP56
compile_php56(){

php56_ver=$(cat /tmp/phpversion.hint|grep "^5.6")
echo "Compiling .... ${php56_ver}"
wget -O /usr/local/src/php-${php56_ver}.tar.bz2 http://us2.php.net/distributions/php-${php56_ver}.tar.bz2
tar -xvjf /usr/local/src/php-${php56_ver}.tar.bz2 -C /usr/local/src/
wget -O /usr/local/src/cl-apache-patches.tar.gz http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz
cd /usr/local/src/php-${php56_ver}
tar -xvzf /usr/local/src/cl-apache-patches.tar.gz fpm-lve-php5.6_autoconf.patch
patch -p1 --fuzz=10 < fpm-lve-php5.6_autoconf.patch
autoconf
config_args=$(php-config --configure-options|sed "s/--prefix=\/usr\/local //;s/--with-apxs2=\/usr\/local\/apache\/bin\/apxs//;s/--with-config-file-path=\/usr\/local\/lib//;s/--with-config-file-scan-dir=\/usr\/local\/lib\/php\.ini\.d//")
./configure ${config_args} --enable-fpm --enable-opcache --prefix=/usr/local/php56_fpm
make
make install
cd -
rm -rf /usr/local/src/php-${php56_ver} /usr/local/src/php-${php56_ver}.tar.bz2 /usr/local/src/cl-apache-patches.tar.gz
/opt/nDeploy/scripts/update_backend.py PHP PHP56_LVE /usr/local/php56_fpm
}


#Uncomment any of the functions below to prevent that version from compiling
compile_php54
compile_php55
compile_php56


osversion=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
echo ${osversion}
if [ ${osversion} -eq 6 ];then
	/etc/init.d/ndeploy_backends stop
	/etc/init.d/ndeploy_backends start
	chkconfig ndeploy_backends on
elif [ ${osversion} -eq 7 ];then
	systemctl stop ndeploy_backends
	systemctl start ndeploy_backends
	systemctl enable ndeploy_backends
else
	echo "ndeploy_backends not restarted"
fi



	
