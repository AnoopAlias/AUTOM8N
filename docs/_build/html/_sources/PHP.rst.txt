Setting up PHP
================

On CentOS6/CentOS7
-------------------

XtendWeb can work with PHP installed from the following Software Collection( SCL)

1. cPanel EA-PHP repo
``/opt/nDeploy/scripts/easy_php_setup.sh``

Additional PHP modules from ea-php repo can be added similar to example below
::

  yum search ea-php
  yum install ea-php70-php-intl
  systemctl restart ndeploy_backends || service ndeploy_backends restart

2. REMI repo
``/opt/nDeploy/scripts/easy_php_setup.sh remi``

Additional PHP modules from remi repo can be added similar to example below
::

  yum --disableexcludes=all --enablerepo=remi search php
  yum --disableexcludes=all --enablerepo=remi install php56-php-pecl-memcached
  systemctl restart ndeploy_backends || service ndeploy_backends restart

On CloudLinux6/CloudLinux7
------------------------------

XtendWeb can work with ea-php packages installed from the CloudLinux cloudlinux-updates-testing repo
Note that remi repo may work but the php in remi is not compiled with the CloudLinux patches so it
may not adhere to limits setup in CloudLinux

1. CloudLinux EA-PHP repo
::

  yum --enablerepo=cloudlinux-updates-testing search ea-php
  yum --enablerepo=cloudlinux-updates-testing install ea-php70-php-intl
  systemctl restart ndeploy_backends || service ndeploy_backends restart


PHP-FPM user level master
---------------------------

The default PHP-FPM setup creates a single master process owned by root, which then spawns multiple pools
which run under the user credentials .The downside of this setup is that opcode caches like OpCache,APC etc share a single
cache .On the upside the root owned master process can chroot pools ensuring php scripts cannot access files (like /etc/named.conf for example )

The user level php-fpm master process can have resource limits set on a per user basis using SimpleR plugin supplied with Xtendweb

To use secure php-fpm
::

  #Works only on Centos7/CloudLinux7
  /opt/nDeploy/scripts/init_backends.py secure-php

To revert to single php-fpm master setup do
::

  /opt/nDeploy/scripts/init_backends.py disable-secure-php



Where are my php logs?
----------------------

XtendWeb creates php-fpm pool files for each user with the PHP error log file set to

``/home/CPANELUSER/logs/php_error_log``
Users can check the logs from their FileManager/FTP/SSH login


ZendOpcache and security considerations on php-fpm single master setup
-----------------------------------------------------------------------

. XtendWeb currently offers the following settings
that can mitigate the security risk of a shared OpCache memory to some extend

1. opcache.restrict_api
::

  opcache.restrict_api
  Allows calling OPcache API functions only from PHP scripts which path is started from specified string. The default "" means no restriction.
  This is set to /home/CPANELUSER/

2. opcache.blacklist_filename
::

  opcache.blacklist_filename
  The location of the OPcache blacklist file. A blacklist file is a text file containing the names of files that should not be accelerated, one per line. Wildcards are allowed, and prefixes can also be provided. Lines starting with a semi-colon are ignored as comments.
  This is set to /home/CPANELUSER/opcache-blacklist.txt
  User can upload the opcache-blacklist.txt to his homedir via FTP or ssh and paths in this file will not be cached.


Per user php.ini custom settings
---------------------------------

php-fpm lets users configure settings of type PHP_INI_PERDIR and PHP_INI_USER in .user.ini files

Ref: http://php.net/manual/en/configuration.file.per-user.php

the settings can be provided in ini format(same as php.ini) and the file must be named .user.ini



.. disqus::
