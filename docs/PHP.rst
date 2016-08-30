Setting up PHP
================

On CentOS6/CentOS7
-------------------

nDeploy can work with PHP installed from the following Software Collection( SCL)

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

nDeploy can work with ea-php packages installed from the CloudLinux cloudlinux-updates-testing repo
Note that remi repo may work but the php in remi is not compiled with the CloudLinux patches so it
may not adhere to limits setup in CloudLinux

1. CloudLinux EA-PHP repo
::

  yum --enablerepo=cloudlinux-updates-testing search ea-php
  yum --enablerepo=cloudlinux-updates-testing install ea-php70-php-intl
  systemctl restart ndeploy_backends || service ndeploy_backends restart


Where are my php logs?
----------------------

nDeploy creates php-fpm pool files for each user with the PHP error log file set to

``/home/CPANELUSER/logs/php_error_log``
Users can check the logs from their FileManager/FTP/SSH login

.. tip:: Note that this feature was added in nDeploy version 3.x. If you are upgrading from a prior release of nDeploy please see the commands below.

You must run
::

  find /opt/nDeploy/php-fpm.d/ -iname "*.conf" -not -name "nobody.conf" -exec rm -f {} \;

  /opt/nDeploy/scripts/attempt_autofix.sh

  systemctl restart ndeploy_backends || service ndeploy_backends restart

The above commands will recreate all php-fpm pool config with the logging setting in place.


ZendOpcache and security considerations
----------------------------------------

PHP-FPM shares the OpCache memory with all the user pools. On a shared hosting setup where users dont trust one another
this can be a security risk . The workaround is to run one PHP-FPM master process per user which need
more resource overhead and a process manager . nDeploy currently offers the following settings
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
