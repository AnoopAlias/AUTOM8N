XtendWeb Cluster Installation
=================================


XtendWeb Cluster Introduction
---------------------------------

XtendWeb cluster is the world's easiest web application clustering solution featuring a fully automated deployment of a clustered DNS load balanced LAMP stack.
It is specifically designed for multi-datacenter deployment and use encrypted communication between the server

XtendWeb cluster provides high availability, scalability and an inherent data backup (application files and database are replicated and normally reside on 2 servers at any time )
Coupled with the simplicity and intuitiveness of cPanel control panel , XtendWeb cluster is a must have for any modern enterprise web application deployment

Cluster Components:

1. cPanel DNS providing multiple A records for round-robin DNS load balancing
2. Nginx servers running on all servers with server specific settings and serving files independently
3. Application servers (php-fpm, HHVM, Phusion Passenger)running on all servers and serving app independently
4. Csync2 - Syncing config across all servers
5. Unison - Syncing files across all servers
6. MaxScale router and MariaDB master-master replication - Database replication and query routing
7. Redis & stunnel - Secure sharing of PHP session
8. XtendWeb - generating and Syncing configuration for all servers


XtendWeb Cluster Requirements
--------------------------------

Master Server :
::

  CentOS7+cPanel
  On your normal RAM requirement add 1 GB Ram extra per slave for Unison file sync running for every 100GB Disk
  Also add enough for httpd service and mysql service which will be running from master
  That is on a cluster with 200GB disk for example
  1 slave with 200GB disk  :  1 GB for 100GB per slave = 2 GB
  2 slave with 200GB disk  :  2( 1 GB for 100GB per slave ) = 4 GB
  3 slaves with 200GB disk :  3( 1 GB for 100GB per slave ) = 6 GB

Slave server:
::

  Add 1 GB RAM for every 100GB disk for unison filesync
  That is for a slave with 200GB disk add 2 GB ram extra to your ram requirement calculation

Example resource calculations
--------------------------------

A typical single slave cluster setup with 200 GB disk and 8GB usable RAM would be
::

  Master : 200GB Disk and 8 + 2 GB(unison)+ 2 GB (extra for httpd and mysql) = 12 GB Ram
  Slave :  200GB Disk and 8 + 2 GB (unison) = 10 GB ram

A typical 2 slave cluster setup with 200 GB disk and 8GB usable RAM would be
  ::

    Master : 200GB Disk and 8 + (2+2) = 4GB(unison)+ 2 GB (extra for httpd and mysql) = 14 GB Ram
    Slave1 :  200GB Disk and 8 + 2 GB (unison) = 10 GB ram
    Slave2 :  200GB Disk and 8 + 2 GB (unison) = 10 GB ram

A typical 3 slave cluster setup with 200 GB disk and 8GB usable RAM would be
  ::

    Master : 200GB Disk and 8 + (2+2+2) = 6GB(unison)+ 2 GB (extra for httpd and mysql) = 16 GB Ram
    Slave1 :  200GB Disk and 8 + 2 GB (unison) = 10 GB ram
    Slave2 :  200GB Disk and 8 + 2 GB (unison) = 10 GB ram
    Slave3 :  200GB Disk and 8 + 2 GB (unison) = 10 GB ram

Notice how the slave RAM requirement remain same,while master need 2 GB(for the 200GB disk sync) ram extra for each slave being added

XtendWeb cluster setup
--------------------------

.. note:: Install CSF firewall on both servers and whitelist each others IP for access . The server's hostname must be valid and should resolve correctly as many cluster components reply on hostname to connect

.. note:: As of XtendWeb 4.3.20, you will need a license for all servers(master and slaves) on the cluster.Else Installation will fail
          Please visit https://autom8n.com/plans.html#plans for more info

The Slaves
----------
::

  # Prepare any number of servers and install cPanel DNS only on it. The slave server is auto setup by the master
  # So do nothing on it except install cPanel DNS only
  cd /home && curl -o latest-dnsonly -L https://securedownloads.cpanel.net/latest-dnsonly && sh latest-dnsonly
  ssh-keygen
  ssh-copy-id root@masters-fqdn
  # Login to WHM
  # Home »Service Configuration »Service Manager
  # Disable tailwatchd and all its drivers

  # Home »Server Configuration »Update Preferences
  # Set cPanel & WHM Updates to Never Update




The Master
------------
::

  #Install cPanel
  cd /home && curl -o latest -L https://securedownloads.cpanel.net/latest && sh latest
  ssh-keygen
  ssh-copy-id root@slaves-fqdn


  # Login to WHM
  # Home »Software »MySQL/MariaDB Upgrade
  # Upgrade to MariaDB 10.1 (General availability)

  yum -y install epel-release
  yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-6.noarch.rpm

  yum -y --enablerepo=ndeploy -y install nginx-nDeploy nDeploy # For nginx as webserver
     OR
  yum -y --enablerepo=ndeploy -y install openresty-nDeploy nDeploy # For openresty as webserver

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable

  yum -y install python-pip libffi-devel python-paramiko python-jinja2
  pip install ansible



  cd /opt/nDeploy/conf/nDeploy-cluster
  cp -p hosts.sample hosts

  # Edit the hosts file

  cat /opt/nDeploy/conf/nDeploy-cluster/hosts
  ############################################################
  [ndeployslaves]  # section containing all your slaves
  slave1.example.com ansible_port=22 server_id=2 webserver=nginx mainip=y.y.y.y
  # ansible_port is ssh port
  # server_id must be unique for each server
  # webserver can be nginx or openresty
  # mainip = the servers main ip address(external IP in a NAT-ed environment)

  [ndeploymaster]  # section containing masters FQDN .Only one entry should be there
  master.example.com ansible_port=22 ansible_connection=local server_id=1 webserver=nginx mainip=x.x.x.x

  [ndeploydbslave] # This section has the DB slave. Only one entry should be there
  slave1.example.com ansible_port=22 server_id=2 webserver=nginx mainip=y.y.y.y
  # A slave can act as the DB slave too
  # In a 2 server setup use the same entry here as in [ndeployslaves]
  # In multi-slave setups, use any one of the slaves as DB slave.
  #############################################################

  # It is recommended that you run the command below in screen as it may take time to complete
  ansible-playbook -i ./hosts cluster.yml

  # Once the Ansible play completes.The cluster is fully setup



.. note:: If you see "ERROR! Unexpected Exception: 'module' object has no attribute 'HAVE_DECL_MPZ_POWM_SEC'" on centos6 do
         yum remove python-crypto && pip install ansible ( Ref: https://github.com/ansible/ansible/issues/276 )



(optional) Add Additonal IP mapping if required
::

  # Cluster setup automatically maps servers main IP's
  # If you are using cloud by DigitalOcean ,Linode etc the automatic mapping is enough
  # If you have multiple IP on master and slave, map additional IP's using command below
  /opt/nDeploy/scripts/update_cluster_ipmap.py
  usage: update_cluster_ipmap.py [-h] slave_hostname service ip_here remote_ip
  service can have value web|dns
  In a NAT-ed system service web should have the internal ip(lan ip) mapping
  while service dns should have the external ip mapping


Quirks for which we need a human intervention sometimes!
::

  # The machine sometimes acts weird.
  # Here are some weird behavior we notice that need manual intervention Just once after cluster setup
  # We are still investigating reason for these and hopefully it will be fixed soon

  # Unison doesn't start automatically on master after cluster setup
  systemctl stop ndeploy_unison
  systemctl start ndeploy_unison

  #PostFix is not running on slave
  systemctl restart postfix



cPanel Horizontal scaling . Adding more web servers
----------------------------------------------------------

XtendWeb cluster's important feature is horizontal scalability. Horizontal scalability helps a web application to scale up and down horizontally .

This is useful when a website has a termendous amount of traffic that one web server cannot handle. With Xtendweb all you need to add a new full processing

capable webserver is as below

The new Slave
::

  # Prepare a fresh server and install cPanel DNS only on it
  cd /home && curl -o latest-dnsonly -L https://securedownloads.cpanel.net/latest-dnsonly && sh latest-dnsonly
  ssh-keygen
  ssh-copy-id root@masters-fqdn
  # Login to WHM
  # Home »Service Configuration »Service Manager
  # Disable tailwatchd and all its drivers

  # Home »Server Configuration »Update Preferences
  # Set cPanel & WHM Updates to Never Update


The Master
::

  cd /opt/nDeploy/conf/nDeploy-cluster
  vim /opt/nDeploy/conf/nDeploy-cluster/hosts

  # Ensure the new servers hostname is added under [ndeployslaves]

  ssh-copy-id root@new-slaves-fqdn

  cd /opt/nDeploy/conf/nDeploy-cluster
  ansible-playbook -i ./hosts cluster.yml


  On master server login to WHM
  Home »SQL Services »Additional MySQL Access Hosts

  # Click on the "click here" link towards the end of the below message
  Important: Users must log into cPanel and use the Remote MySQL feature to set up access from these hosts. After you have done this, if you would like to configure access from all users’ accounts click here.


Thats it. Your new host will start serving the website once the /home data is replicated.You can shutdown nginx on this host until data is replicated

Adding more webservers to horizontally scale a webapp will roughly take 10 minutes ( assuming a server with cPanel DNS only installed is used)
