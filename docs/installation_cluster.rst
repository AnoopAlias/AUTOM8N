XtendWeb Cluster Installation
=================================


XtendWeb Cluster Introduction
---------------------------------

XtendWeb cluster is the worlds easiest web application clustering solution featuring a fully automated deployment of a clustered DNS loadbalanced LAMP stack.
It is specifically designed for multi datacenter deployment and use encrypted communication between the server

XtendWeb cluster provide high availability , scalability and an inherent data backup (application files and database are replicated and normally reside on 2 servers at any time )
Coupled with the simplicity and intutiveness of cPanel control panel ,XtendWeb cluster is a must have for any modern enterprise web application deployment

Cluster Components:

1. cPanel DNS providing multiple A records for round robin DNS loadbalancing
2. Nginx servers running on all servers with server specific settings and serving files independandly
3. Application servers (php-fpm. Phusion passenger )running on all servers and serving app independandly
4. Csync2 - Syncing config across all servers
5. Unison - Syncing files across all servers
6. MaxScale router and mariaDB master-master replication - Database replication and query routing
7. Redis & stunnel - Secure sharing of PHP session
8. XtendWeb - generating and Syncing configuration for all servers


XtendWeb Cluster Requirements
--------------------------------

It is recommended that you setup XtendWeb cluster on CentOS7 with latest cPanel (v64 as of writing this).

We do support CentOS6, but it is less tested and has some disadvantages like stunnel startup script is lacking in CentOS6 .

XtendWeb cluster needs atleast 2 servers. Only one of the server need a valid cPanel license

Cluster provide horizontal scalability for web applications using DNS loadbalancing .

It is highly recommended that the servers be on different geographic regions ( eg: master in US , slave in UK ) and use different providers.
The golden rule is - Dont keep all your eggs in the same basket.

All communication between master and slave is TLS encrypted and is therefore safe .
The master and slave just need to be able to connect via internet.

The recommended way to upgrade to XtendWeb cluster from cPanel is setting up the cluster and migrating the websites over rather than setting up cluster
on the existing server.

Master server - Centos7 ,MariaDB 10.1

Slave Server's - Centos7 ( installed with cPanel DNS only which is licensed free ).Rest of the software is installed automatically at cluster setup.



XtendWeb cluster setup
--------------------------

.. tip:: Install CSF firewall on both servers and whitelist each others IP for access

.. tip:: The servers hostname must be valid and should resolve correctly(atleast from inside the master and slaves).
          It is recommended that they resolve correctly on the internet

.. note:: As of XtendWeb 4.3.20 you will need a license for all servers(master and slaves) on the cluster .Else Installation will fail
          Please visit https://autom8n.com/plans.html#plans for more info

1. Install cPanel and cPanel DNS only on master and slaves respectively
::

  # On Master
  cd /home && curl -o latest -L https://securedownloads.cpanel.net/latest && sh latest

  #On Slaves
  cd /home && curl -o latest-dnsonly -L https://securedownloads.cpanel.net/latest-dnsonly && sh latest-dnsonly


2. Install XtendWeb on master only
::

  # On Master only
  yum -y install epel-release
  yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-6.noarch.rpm

  # Purchase a license so the server can access xtendweb yum repo

  yum -y --enablerepo=ndeploy -y install nginx-nDeploy nDeploy # For nginx as webserver
     OR
  yum -y --enablerepo=ndeploy -y install openresty-nDeploy nDeploy # For openresty as webserver

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable

  /opt/nDeploy/scripts/setup_additional_templates.sh  # For installing Wordpress and Drupal full page cache template





3. On Master server Login to WHM and upgrade to MariaDB 10.1
::

  # On Master only
  Home »Software »MySQL/MariaDB Upgrade
  Select MariaDB 10.1 (General availability)
  and click "Next"
  Ensure Upgrade completes successfully

  Ensure password in /root/.my.cnf is enclosed in single quotes (eg password='mysecurepass')
  Unquoted and double-quoted password can sometimes cause issues



4. Setup password-less ssh login between master and slaves
::

  #On master
  ssh-keygen
  ssh-copy-id root@slaves-fqdn

  #On slaves
  ssh-keygen
  ssh-copy-id root@masters-fqdn

  #Ensure passwordless login works for root


5. Install Ansible on master
::

  # On master only
  yum -y install python-pip libffi-devel python-paramiko python-jinja2
  pip install ansible


6. Setup the hosts file on master
::

  # On a 2 server setup with default ssh port you just need to replace master and slave FQDN's in the sample file
  cd /opt/nDeploy/conf/nDeploy-cluster
  cp -p hosts.sample hosts

  # Edit the hosts file

  cat /opt/nDeploy/conf/nDeploy-cluster/hosts

  [ndeployslaves]  # section containing all your slaves
  slave1.example.com ansible_port=22 server_id=2 webserver=nginx
  # ansible_port is ssh port
  # server_id must be unique for each server
  # webserver can be nginx or openresty

  [ndeploymaster]  # section containing masters FQDN .Only one entry should be there
  master.example.com ansible_port=22 ansible_connection=local server_id=1 webserver=nginx

  [ndeploydbslave] # This section has the DB slave .Only one entry should be there
  slave1.example.com ansible_port=22 server_id=2 webserver=nginx
  # A slave can act as the DB slave too
  # In a 2 server setup use the same entry here as in [ndeployslaves]
  # In multi slave setups, use one of the slaves as DB slave.


7. Setup Cluster on master
::

  # It is recommended that you run the command below in screen as it may take time to complete
  ansible-playbook -i ./hosts cluster.yml


.. tip:: If you see "ERROR! Unexpected Exception: 'module' object has no attribute 'HAVE_DECL_MPZ_POWM_SEC'" on centos6 do
         yum remove python-crypto && pip install ansible ( Ref: https://github.com/ansible/ansible/issues/276 )



8. (optional) Add Additonal IP mapping if required
::

  # Cluster setup automatically maps servers main IP's
  # If you are using cloud by DigitalOcean ,Linode etc the automatic mapping is enough
  # If you have multiple IP on master and slave, map additional IP's using command below
  /opt/nDeploy/scripts/update_cluster_ipmap.py
  usage: update_cluster_ipmap.py [-h] slave_hostname ip_here remote_ip


9. Quirks for which we need a human intervention sometimes!
::

  # The machine sometimes act weired .
  # Here are some weired behaviour we notice that need manual intervention
  # We are still investigating reason for these and hopefully it will be fixed soon

  # Unison doesnt start automatically on master after cluster setup
  systemctl stop ndeploy_unison
  systemctl start ndeploy_unison

  #PostFix is not running on slave( see tip below and disable checksrvd and upcp cron)
  systemctl restart postfix


The cluster including PHP app server is fully setup now  and you can start adding accounts .Cluster automatically setus up DNS clustering
and you should use master and slaves as the nameservers for the domain to ensure DNS LoadBalancing.


.. tip:: Disable chkservd and all its drivers on slave dns only servers as chkservd can cause troubles in cluster operation.

         Disable all cronjobs including upcp cron in slaves crontab ( upcp sometimes removes non-cpanel componets setup by the cluster )
