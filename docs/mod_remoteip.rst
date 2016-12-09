mod_remoteip
============

One of the backend XtendWeb support is PROXY to httpd .
You must setup mod_remoteip to provide httpd with the correct IP of clients and modify apache logging settings
``yum -y install ea-apache24-mod_remoteip``


XtendWeb automatically generates the remoteIP configuration when the plugin is enabled
You just need to include the file in Apache httpd as below


1. Navigate to WHM Home »Service Configuration »Apache Configuration »Include Editor > Scroll down to "Pre VirtualHost Include"

2. Select the version of Apache you wish to customize and add the following
::

  Include "/etc/nginx/conf.d/httpd_mod_remoteip.include"

3. Click Update , which will then make the above settings active

.. disqus::
