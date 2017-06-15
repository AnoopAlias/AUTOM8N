Installation
============
XtendWeb Requirements: cPanel 60.0+ server with CentOS6/CentOS7/CloudLinux6/CloudLinux7 64 bit OS installed

.. tip:: XtendWeb can use either Nginx or OpenResty as the webserver

.. tip:: CentOS7/CloudLinux7 is recommended


1. Install EPEL repo
::

  yum -y install epel-release

2. Install XtendWeb yum repo
::

  yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-5.noarch.rpm


3. Install XtendWeb plugin and nginx or openresty . Be patient as this may take several minutes to complete.
::

  yum --enablerepo=ndeploy install nginx-nDeploy nDeploy # For nginx as webserver
     OR
  yum --enablerepo=ndeploy install openresty-nDeploy nDeploy # For openresty as webserver
  # OpenResty support embedding lua code.Openresty does not include mod_security and naxsi modules (use OpenSSL)
  # Nginx include naxsi and mod_security waf ( use LibreSSL instead of OpenSSL )
  # You can use any of the webserver in an interchangeable way and swap anytime


4.1. Install PHP-FPM Application server
::

  #Install PHP-FPM Application server for PHP
  /opt/nDeploy/scripts/easy_php_setup.sh
  # php-fpm and a selected set of modules are installed from the EA4 php repo

.. tip:: Default PHP-FPM setup above use chroot of PHP-FPM pools to /home/virtfs . This is an alternative to CageFS.
         PHP process will not be able to view files not in /home/virtfs like /etc/named.conf for example.
         Ref: https://documentation.cpanel.net/display/ALD/PHP-FPM+User+Pools#PHP-FPMUserPools-Jailshell

4.1.1. (Optional) Setup per user php-fpm master process for complete user level isolation
::

    #Works only on Centos7/CloudLinux7
    /opt/nDeploy/scripts/init_backends.py secure-php
    # This setup does not support chroot to virtfs as user level process cannot be chrooted!
    # PHP pocess is user owned but will be able to read files the user has access to


4.1.2. Enable PHP-FPM selector plugin(to make php-fpm default in httpd)
::

  /opt/nDeploy/scripts/init_backends.py httpd-php-install
  # Note that this will add new apache vhost templates in /var/cpanel/templates/apache2_4/
  # This will make php-fpm the default backend for all accounts in Apache httpd
  # Users can switch PHP version on a per domain basis using PHP-FPM selector plugin in cPanel

4.2. Install Phusion Passenger ( only if you need support for RUBY/PYTHON/NODEJS )
::

  yum --enablerepo=ndeploy install nginx-nDeploy-module-passenger # Nginx
  OR
  yum --enablerepo=ndeploy install openresty-nDeploy-module-passenger # Openresty
  #Enable Phusion Passenger Application Server backend. This is required for Ruby/Python/NodeJS.
  /opt/nDeploy/scripts/easy_passenger_setup.sh
  # Ruby will be compiled and installed to /usr/local/rvm
  # Python will be compiled and installed to /usr/local/pythonz
  # NodeJS will be installed to /usr/local/nvm
  # The easy_passenger script installs only one version of Ruby/Python and NodeJS
  # Additional versions can be installed and managed using rvm,pythonz and nvm respectively

4.3. Install HHVM Hack/PHP Application server
::

  /opt/nDeploy/scripts/easy_hhvm_setup.sh


5. Enable the plugin. This will make nginx your frontend webserver.
::

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable


.. tip:: If you modify WHM service certificate run /opt/nDeploy/scripts/generate_default_vhost_config.py && nginx -s reload

6. Enable Extra templates that require redis and additional nginx modules
::

  /opt/nDeploy/scripts/setup_additional_templates.sh


7. Install Optional additional modules
::

  #Note that each module increases the nginx size and processing requirements
  #So install only required functionality .
  (pagespeed)   yum --enablerepo=ndeploy install nginx-nDeploy-module-pagespeed
  (pagespeed)   yum --enablerepo=ndeploy install openresty-nDeploy-module-pagespeed  # OpenResty
  (brotli)      yum --enablerepo=ndeploy install nginx-nDeploy-module-brotli
  (brotli)      yum --enablerepo=ndeploy install openresty-nDeploy-module-brotli  # OpenResty
  (geoip)       yum --enablerepo=ndeploy install nginx-nDeploy-module-geoip
  (geoip)       yum --enablerepo=ndeploy install openresty-nDeploy-module-geoip # OpenResty
  (naxsi)       yum --enablerepo=ndeploy install nginx-nDeploy-module-naxsi
  (modsecurityv3) yum --enablerepo=ndeploy install nginx-nDeploy-module-modsecurity
  (redis)       yum --enablerepo=ndeploy install nginx-nDeploy-module-redis
  (redis2)      yum --enablerepo=ndeploy install nginx-nDeploy-module-redis2
  (set_misc)    yum --enablerepo=ndeploy install nginx-nDeploy-module-set_misc
  (srcache)     yum --enablerepo=ndeploy install nginx-nDeploy-module-srcache_filter
  (echo)        yum --enablerepo=ndeploy install nginx-nDeploy-module-echo
  # Following modules are installed and loaded by default in nginx but can be disabled
  (headers_more)
  (ndk) Nginx Development ToolKit
  # Following modules are installed and loaded by default in openresty
  https://openresty.org/en/components.html

.. tip:: There are no additonal configurations required for the loadable modules. Users can control the functionality from XtendWeb UI


.. disqus::
