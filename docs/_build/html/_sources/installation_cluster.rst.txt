Cluster Installation
=======================

XtendWeb Cluster Requirements:
--------------------------------
.. note:: using CloudLinux will be counter productive on XtendWeb Cluster as cloudLinux is trying to solve server stability problem by limiting resources useable by a user
          XtendWeb on the other hand tries to achieve stability by using a fan-out infrastructure which is what an enterprise user would need.
          
It is recommended that you setup XtendWeb cluster on CentOS7 with latest cPanel (v64 as of writing this). XtendWeb cluster needs atleast 2 servers.

It is highly recommended that the servers be on different geographic regions ( eg: master in US , slave in UK ) and use different providers.
The golden rule is - Dont keep all your eggs in the same basket.

All communication between master and slave is TLS encrypted and is therefore safe .
The master and slave just need to be able to connect via internet.

The recommended way to upgrade to XtendWeb cluster from cPanel is setting up the cluster and migrating the websites over rather than setting up cluster
on the existing server.

Master server - Centos7 ,MariaDB 10.1

Slave Server's - Centos7 ( installed with cPanel DNS only which is licensed free ).Rest of the software is installed automatically at cluster setup.

.. tip:: The servers hostname must be valid and should resolve correctly(atleast from inside the master and slaves).
          It is recommended that they resolve correctly on the internet


.. tip:: CentOS7 is recommended


XtendWeb cluster setup:
--------------------------

.. tip:: If you are using CSF whitelist all server ip's in cluster and ensure TCP ports  30865 , 4430, 9999, 13306 are allowed

.. tip:: The servers hostname must be valid and should resolve correctly(atleast from inside the master and slaves).
          It is recommended that they resolve correctly on the internet


1. Install XtendWeb as normal on master and enable the plugin
::

  Follow https://xtendweb.gnusys.net/docs/installation_standalone.html  # On master


2. Install cPanel DNS only on all the slaves
::

  cd /home && curl -o latest-dnsonly -L https://securedownloads.cpanel.net/latest-dnsonly && sh latest-dnsonly
  # You do not need to install XtendWeb or make any other changes on the slave


3. On Master Login to WHM and upgrade to MariaDB 10.1
::

  Home »Software »MySQL/MariaDB Upgrade
  Select MariaDB 10.1 (General availability)
  and click "Next"
  Ensure Upgrade completes successfully


.. tip:: On master ensure the /root/.my.cnf has mysql password enclosed in single quotes .
         Unquoted password will fail the Ansible playbook run
         password='mypass' is good. password=mypass and password="mypass" may cause failure in setup scripts


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



8. Add Additonal IP mapping if required
::

  # Cluster setup automatically maps servers main IP's
  # If you are using cloud by DigitalOcean ,Linode etc the automatic mapping is enough
  # If you have multiple IP on master and slave, map additional IP's using command below
  /opt/nDeploy/scripts/update_cluster_ipmap.py
  usage: update_cluster_ipmap.py [-h] slave_hostname ip_here remote_ip

9. Setup MySQL profile on masters WHM
::

  WHM >> Home »SQL Services »Manage MySQL® Profiles
  Add a new profile:
    Profile Name : xtendweb
    [select] Manually enter an existing MySQL superuser’s credentials.Manually enter an existing MySQL superuser’s credentials.
    Host: 127.0.0.1  #Do not use localhost as this will fail
    Port: 13306
    Username: root
    Password: ****  #This is mysql root password and can be obtained from /root/.my.cnf

    Save and under actions click on : "Validate" and "Activate" the xtendweb pofile.


The cluster is fully setup now and you can start adding accounts .Cluster automatically setus up DNS clustering
and you should use master and slaves as the nameservers for the domain to ensure DNS LoadBalancing.

The slave works independently (thus the scalability!) ,so ensure the backends required are installed on all slaves using
::

   /opt/nDeploy/scripts/easy_php_setup.sh # For PHP
   /opt/nDeploy/scripts/easy_hhvm_setup.sh # For HHVM

   yum --enablerepo=ndeploy install nginx-nDeploy-module-passenger # Nginx
   OR
   yum --enablerepo=ndeploy install openresty-nDeploy-module-passenger # Openresty
   AND
   /opt/nDeploy/scripts/easy_passenger_setup.sh  #For Python/Ruby/NodeJS

.. tip:: Disable chkservd on slave dns only servers as chkservd can cause troubles in cluster operation.
