nDeploy cluster setup
=====================

Your business is critical - Never Lose an email . Never Show a "WebSite Down!" message to a client .

Never worry how your server will handle the next high profile product launch

DuET cPanel provides a horizontally scalable high-performance web stack on a cPanel server that makes 3 critical infrastructure high available

1. High Available web stack using Round Robin DNS

2. High Available MySQL/MariaDB using master-master replication

3. PostFix backup MX that will accept and queue up emails in case the master goes down and deliver it to master once master is online

DuET cPanel needs at least 2 servers ( thus the name! ) .It is best that they be identical , but except for the drives, it is not mandatory.

1. cPanel Licenced server (master)

2. cPanel DNS only server (slave)

You can add more cPanel DNS only installed slave servers at any time and scale your infrastructure horizontally

The recommended method to switch to DuET cPanel is set up the DuET cpanel in a cloud ( Why Cloud?) and migrate your domains over. You can Also migrate your existing cPanel server setup to DuET cPanel , but this is not discussed here.


Basic 2 server setup
---------------------

1. Setup cPanel
::

  master.sysally.net  ==> CentOS7 ,cPanel ,MariaDB 10.1
  Install cPanel - cd /home && curl -o latest -L https://securedownloads.cpanel.net/latest && sh latest

  slave.sysally.net ==> CentOS7 ,cPanel DNS only
  Install DNS Only - cd /home && curl -o latest-dnsonly -L https://securedownloads.cpanel.net/latest-dnsonly && sh latest-dnsonly

2. Install nDeploy on the master . Follow http://ndeploy.readthedocs.io/en/latest/#installation

3. Install ansible
::

  yum -y install python-pip libffi-devel python-paramiko python-jinja2
  pip install ansible

4. Ensure master and slave can communicate via SSH without password (SSH key based login must work from both ends)

Login at least once from both ends and ensure the SSH key signatures are accepted and SSH login works without any prompt
::

  On Slave:
  ssh root@masters-FQDN -p port

  On Master:
  ssh root@slaves-FQDN -p port

5. Setup the cluster

On the dnsonly slave remove the cpanel installed MySQL* rpms as these prevent the postfix server to be installed
::

  eg:
  root@slave [~]# rpm -qa|grep MySQL
  MySQL55-test-5.5.48-1.cp1148.x86_64
  MySQL55-server-5.5.48-1.cp1148.x86_64
  MySQL55-devel-5.5.48-1.cp1148.x86_64
  MySQL55-shared-5.5.48-1.cp1148.x86_64

  yum remove MySQL55-*

On Master
::

  cd /opt/nDeploy/conf/nDeploy-cluster
  cp -p hosts.sample hosts

  #Modify the hosts file created above as required .Use FQDN's for hostnames

  ansible-playbook -i ./hosts cluster.yml

  #If any of the tasks fail; you will need to check it and rerun the playbook


Configuring the rest of the system to work as a cluster
-------------------------------------------------------

**EMAIL**

6. Setup the BackupMX
::

  WHM >> Home »DNS Functions »Edit Zone Templates
  Modify the DNS zone template on master and set slave as a second MX entry with lower priority
  %domain%. IN A %ip%
  %domain%. IN AAAA %ipv6%

  %domain%. IN MX 0 %domain%.
  %domain%. IN MX 5 slave.sysally.net.

  WHM >> Home »Service Configuration »Exim Configuration Manager
  Access Lists
  Backup MX hosts => Edit

  and add the hostname of the slave to this list

**DNS**

7. WHM >> Home »Clusters »DNS Cluster

Setup DNS clustering between master and slave with DNS role as "Synchronize Changes"

**MYSQL**

There are 2 ways to setup MySQL to be used with nDeploy cluster.

Dedicated MySQL server(recommended):

*This setup is recommeded for its simplicity .The downside is that the MySQL server is a*
*single point of failure and Sites will show database error on the database server outage.But*
*since the dedicated mysql server runs only mysql it can be fine tuned and downtime can be limited*
*to cases where there is a planned downtime by the host itself (which are very few in modern cloud)*
