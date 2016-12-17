Monitoring nginx and app servers
=================================

**Monitoring nginX**

The server is already configured on localhost to send the nginx status at nginx_status URL

lynx http://localhost/nginx_status

on the server cli will show the status .
Local checks (for example the check_mk nginx status module) should just report
the details fine to remote monitoring servers.

Monit configuration for nginx
Below example is for init .For systemd replace "/etc/init.d/nginx start/stop"
with "/usr/bin/systemctl start/stop nginx.service"
::

  check process nginx with pidfile /var/run/nginx.pid
  start program = "/etc/init.d/nginx start"
  stop program  = "/etc/init.d/nginx stop"



**Monitoring php-fpm**

php-fpm can be configured to provide detailed status info per pool.
But since this has its own data confidentiality risks
this is not enabled by default on the php-fpm pool config file.
But all php-based templated include a location block to give a ping signal to php-fpm
and the fpm pool is setup to respond with a pong

http://domain.com/pingphpfpm

will return with a pong output if php-fpm pool is working fine .

This can be easily configured for status checking

Monit configuration useful to restart php-fpm in case of issues
Below example is for systemd .For init replace "/usr/bin/systemctl start/stop ndeploy_backends.service"
with "/etc/init.d/ndeploy_backends start/stop"
::

  check host mydomain.com with address mydomain.com
  start program = "/usr/bin/systemctl start ndeploy_backends.service"
  stop program = "/usr/bin/systemctl stop ndeploy_backends.service"
    if failed url https:/mydomain.com/pingphpfpm
        and content = "pong"
        with timeout 60 seconds
    then restart



.. disqus::
