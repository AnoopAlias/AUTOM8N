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


Monitoring Xtendweb cPanel cluster
======================================

XtendWeb cPanel web cluster require monitoring of File syncing and database replication. This is provided 24x7 with our Proactive cluster administration
plan. AUTOM8N use check_mk+nagios for monitoring the infrastructure .


If you have a Proactive cluster support plan do
::

  yum --enablerepo=ndeploy install gnusys-monitoring

Database Replication
----------------------

Database replication health should be monitored . Since XtendWeb cPanel web cluster use MySQL Master-Master replication ,the 'seconds behind master' field in
cPanel master server and DB slave server must be monitored . This is automatically done if you enable MySQL monitoring via local check in check_mk


Unison File Sync status
----------------------------

The Following check_mk local check can monitor unison file sync
::

  #!/usr/bin/env python


  import os
  import psutil
  import yaml


  __author__ = "Anoop P Alias"
  __copyright__ = "Copyright Anoop P Alias"
  __license__ = "GPL"
  __email__ = "anoopalias01@gmail.com"


  installation_path = "/opt/nDeploy"  # Absolute Installation Path
  cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"


  if os.path.isfile(cluster_config_file):
      filesync_fail_count = 0
      status = []
      with open(cluster_config_file, 'r') as cluster_data_yaml:
          cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
      for servername in cluster_data_yaml_parsed.keys():
          filesync_ok = False
          for myprocess in psutil.process_iter():
              mycmdline = myprocess.cmdline()
              if '/usr/bin/unison' in mycmdline and servername in mycmdline:
                  filesync_ok = True
              else:
                  pass
          if not filesync_ok:
              filesync_fail_count = filesync_fail_count+1
              status.append(servername+":FAIL")
      if filesync_fail_count > 0:
          print("2 unison - "+str(status))
      else:
          print("0 unison - OK")




Health of websites and application servers must be monitored in all master and slave cPanel servers in a cluster setup.
