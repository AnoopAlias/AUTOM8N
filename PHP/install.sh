#!/bin/sh

yum install libmcrypt-devel openssl-devel gmp-devel curl-devel libcurl-devel libcurlssl-devel -y
yum install firebird-devel -y
yum install ImageMagick-devel sqlite-devel freetds-devel

curl -L -O https://github.com/phpbrew/phpbrew/raw/master/phpbrew
chmod +x phpbrew
sudo mv phpbrew /usr/bin/phpbrew

phpbrew init

# Download cloudlinux patches
if [ ! -f "cl-apache-patches.tar.gz" ]; then
	wget http://repo.cloudlinux.com/cloudlinux/sources/da/cl-apache-patches.tar.gz -O cl-apache-patches.tar.gz
fi

read

# patch -p1 < fpm-lve-php5.4.patch

source ~/.phpbrew/bashrc

export PHPBREW_ROOT=/usr/local/phpbrew
mkdir $PHPBREW_ROOT -v

# default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap +iconv +sqlite +gettext
php -n /usr/bin/phpbrew --debug install --jobs 12 --patch fpm-lve-php5.4_fixed.patch 5.6.15 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap +iconv +sqlite +gettext -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr
php -n /usr/bin/phpbrew --debug install --jobs 12 --patch fpm-lve-php5.4_fixed.patch 5.5.30 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap +iconv +sqlite +gettext -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr
php -n /usr/bin/phpbrew --debug install --jobs 12 --patch fpm-lve-php5.4_fixed.patch 5.4.45 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap +iconv +sqlite +gettext -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr
php -n /usr/bin/phpbrew --debug install --jobs 12 --patch fpm-lve-php5.4_fixed.patch 5.3.29 +default +fpm +mysql +exif +ftp +gd +intl +soap +pdo +curl +gmp +imap +iconv +sqlite +gettext -- --with-libdir=lib64 --with-gd=shared --enable-gd-natf --with-jpeg-dir=/usr --with-png-dir=/usr


phpbrew use php-5.4.45

EXTENSIONS="imagick pdo_firebird memcache uploadprogress"
for i in $EXTENSIONS; do
  phpbrew ext install $i
  if [ $? -ne 0 ]; then
    exit $?
  fi
  phpbrew ext enable $i
done

phpbrew ext install imagick
phpbrew ext install pdo_dblib -- --with-libdir=lib64
phpbrew ext install pdo_firebird
phpbrew ext install memcache /memcached
phpbrew ext install uploadprogress

# devel
phpbrew ext install xhprof 0.9.4
phpbrew ext disable xhprof

# gd installed by main php compile
mkdir /usr/local/phpbrew/php/$PHPBREW_PHP/var/db/ -p
echo extension=gd.so >> /usr/local/phpbrew/php/$PHPBREW_PHP/var/db/gd.ini
phpbrew ext enable gd
phpbrew ext install gd -- --with-freetype-dir=/usr/include/freetype ???? not work

http://www.directadmin.com/imap.txt
https://github.com/phpbrew/phpbrew/issues/227
yum install libc-client-devel uw-imap.x86_64
phpbrew ext install imap


/opt/nDeploy/scripts/update_backend.py PHP php-5.4.45 /usr/local/phpbrew/php/php-5.4.45