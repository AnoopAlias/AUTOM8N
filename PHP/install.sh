#!/bin/sh

yum install libmcrypt-devel openssl-devel -y

# Download cloudlinux patches
if [ ! -f "cl-apache-patches.tar.gz" ]; then
	wget http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz -O cl-apache-patches.tar.gz
fi

tar xvzf cl-apache-patches.tar.gz fpm-lve-php5.4_autoconf.patch fpm-lve-php5.4.patch

read

# --patch fpm-lve-php5.4_autoconf.patch --patch fpm-lve-php5.4.patch

patch -p1 < fpm-lve-php5.4.patch

php -n /usr/bin/phpbrew --debug install --jobs 4 5.4.42 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr

phpbrew ext install zendopcache
phpbrew ext install memcached
phpbrew ext install memcache
phpbrew ext install pdo_sqlite

/opt/nDeploy/scripts/update_backend.py PHP php-5.4.42 /usr/local/phpbrew/php/php-5.4.42


# ??? --enable-force-cgi-redirect