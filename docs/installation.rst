Installation
============
Requirements: cPanel 11.48+ server with CentOS6/CentOS7/CloudLinux6/CloudLinux7 64 bit OS installed

* nDeploy 3.x is available via yum (Supports PHP-FPM from EasyApache4 or REMI repo)
* nDeploy 2.0.65 is available as an RPM package for manual install
* CentOS6/CloudLinux6 RPM - `https://rpm.piserve.com/CentOS/6/x86_64/ <https://rpm.piserve.com/CentOS/6/x86_64/>`_
* CentOS7/CloudLinux7 RPM - `https://rpm.piserve.com/CentOS/7/x86_64/ <https://rpm.piserve.com/CentOS/7/x86_64/>`_

1. Install EPEL repo
::

  yum -y install epel-release

#. Install nDeploy yum repo
::

  yum -y install https://github.com/AnoopAlias/nDeploy/raw/master/nDeploy-release-centos-1.0-3.noarch.rpm

#. Install nDeploy plugin and nginx. Be patient as this may take several minutes to complete.
::

  yum --enablerepo=ndeploy install nginx-nDeploy nDeploy

#. Install or enable Application servers. You can skip any step below based on your servers requirements.
::

  #Install PHP-FPM Application server for PHP
  /opt/nDeploy/scripts/easy_php_setup.sh

  #Enable Phusion Passenger Application Server backend. This is required for Ruby/Python/NodeJS.
  /usr/nginx/scripts/nginx-passenger-setup.sh

#. Enable the plugin. This will make nginx your frontend webserver.
::

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable

#. Step4(Optional) : Setup NAXSI learning .This is required to generate NAXSI whitelist rules
::

  #Note that this step will install JAVA and ElasticSearch daemon for NXAPI
  /usr/nginx/scripts/nxapi-setup.sh


.. disqus::
