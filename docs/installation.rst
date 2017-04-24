Installation
============
XtendWeb Requirements: cPanel 60.0+ server with CentOS6/CentOS7/CloudLinux6/CloudLinux7 64 bit OS installed

.. tip:: Ensure your cPanel version displayed in WHM is 60 or higher

.. tip:: CentOS7/CloudLinux7 is recommended

1. Install EPEL repo
::

  yum -y install epel-release

2. Install XtendWeb yum repo
::

  yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-5.noarch.rpm


3. Install XtendWeb plugin and nginx. Be patient as this may take several minutes to complete.
::

  yum --enablerepo=ndeploy install nginx-nDeploy nDeploy


4.1. Install PHP-FPM Application server
::

  #Install PHP-FPM Application server for PHP
  /opt/nDeploy/scripts/easy_php_setup.sh
  # php-fpm and a selected set of modules are installed from the EA4 php repo

4.2. Install Phusion Passenger ( only if you need support for RUBY/PYTHON/NODEJS )
::

  yum --enablerepo=ndeploy install nginx-nDeploy-module-passenger
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
  (brotli)      yum --enablerepo=ndeploy install nginx-nDeploy-module-brotli
  (geoip)       yum --enablerepo=ndeploy install nginx-nDeploy-module-geoip
  (naxsi)       yum --enablerepo=ndeploy install nginx-nDeploy-module-naxsi
  (redis)       yum --enablerepo=ndeploy install nginx-nDeploy-module-redis
  (redis2)      yum --enablerepo=ndeploy install nginx-nDeploy-module-redis2
  (set_misc)    yum --enablerepo=ndeploy install nginx-nDeploy-module-set_misc
  (srcache)     yum --enablerepo=ndeploy install nginx-nDeploy-module-srcache_filter
  (echo)        yum --enablerepo=ndeploy install nginx-nDeploy-module-echo
  # Following modules are installed and loaded by default but can be disabled
  (headers_more)
  (ndk) Nginx Development ToolKit

.. tip:: There are no additonal configurations required for the loadable modules. Users can control the functionality from XtendWeb UI


.. disqus::
