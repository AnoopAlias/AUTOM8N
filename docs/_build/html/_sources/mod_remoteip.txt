mod_remoteip
============

One of the backend nDeploy support is PROXY to httpd .
You must setup mod_remoteip to provide httpd with the correct IP of clients and modify apache logging settings
``yum -y install ea-apache24-mod_remoteip``

1. Navigate to WHM Home »Service Configuration »Apache Configuration »Include Editor > Scroll down to "Pre VirtualHost Include"

2. Select the version of Apache you wish to customize and add the following
::

  <IfModule remoteip_module>
    RemoteIPHeader X-Forwarded-For
    RemoteIPTrustedProxy x.x.x.x/32   #substitute x.x.x.x with your IP address
    RemoteIPTrustedProxy y.y.y.y/32   #substitute y.y.y.y with your IP address
  </IfModule>
  <IfModule log_config_module>
    LogFormat "%{Referer}i -> %U" referer
    LogFormat "%{User-agent}i" agent
    LogFormat "%a %l %u %t \"%r\" %>s %b" common
    LogFormat "%a %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    CustomLog logs/access_log combined
  </IfModule>

3. Click Update , which will then make the above settings active

.. disqus::
