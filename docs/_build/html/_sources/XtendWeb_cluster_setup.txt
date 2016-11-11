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

  #Copy rpm repos on master to slave for php and mysql
  cd /etc/yum.repos.d
  rsync -av EA4.repo MariaDB101.repo root@slave:/etc/yum.repos.d/


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

8. There are 3 ways to setup MySQL to be used with nDeploy cluster.

Dedicated MySQL server(recommended):

*This setup is recommeded for its simplicity .The downside is that the MySQL server is a*
*single point of failure and Sites will show database error on the database server outage.But*
*since the dedicated mysql server runs only mysql it can be fine tuned and downtime can be limited*
*to cases where there is a planned downtime by the host itself (which are very few in modern cloud)*

In each server the /var/lib/mysql/mysql.sock and 127.0.0.1:3306 sockets are bound by nginx stream proxy.

MySQL master-master replication with nginx as proxy:

::

  yum install MariaDB-server MariaDB-client MariaDB-shared MariaDB-common MariaDB-devel

  On master and slave setup the my.cnf file ( sample my.cnf file is provided as /opt/nDeploy/conf/cluster_mysql.ini.sample)
  server-id and auto_increment_offset must be different on both servers .Dump and restore all data on master on the slave.

  On Master:

  MariaDB [(none)]> grant replication slave on *.* to replicator@'slaves-ip' identified by 'thesecretpass';
  Query OK, 0 rows affected (0.00 sec)

  MariaDB [(none)]> flush privileges;

  On Slave:
  MariaDB [(none)]> grant replication slave on *.* to replicator@'masters-ip' identified by 'thesecretpass';
  Query OK, 0 rows affected (0.00 sec)

  MariaDB [(none)]> flush privileges;

  Verify the master log file and position on both servers and configure each other to be a slave

  On Master:
  MariaDB [(none)]> show master status;
  +-------------------+----------+--------------+------------------+
  | File              | Position | Binlog_Do_DB | Binlog_Ignore_DB |
  +-------------------+----------+--------------+------------------+
  | master-bin.000002 |      641 |              |                  |
  +-------------------+----------+--------------+------------------+

  On Slave:

  MariaDB [(none)]> CHANGE MASTER TO master_host='masters-ip', master_port=13306, master_user='replicator', master_password='thesecretpass', master_log_file='master-bin.000002', master_log_pos=641;
  Query OK, 0 rows affected (0.03 sec)

  MariaDB [(none)]> start slave;

  Do the same by reversing the server roles thus making each server master to and slave of the other.

Setup nginX as a proxy to the MySQL service and serve the port and socket where PHP expects it to be

Sample config files /etc/nginx/conf.d/mysql_stream_master.conf and /etc/nginx/conf.d/mysql_stream_slave.conf is already supplied by the RPM
Copy and adjust it according to your setup and include it in nginx.conf from the file /etc/nginx/conf.d/main_custom_include.conf

::

  On Master:

  cp -p /etc/nginx/conf.d/mysql_stream_master.conf /etc/nginx/conf.d/mysql_stream_master.conf.local
  [root@master ~]# cat /etc/nginx/conf.d/main_custom_include.conf
  include /etc/nginx/conf.d/mysql_stream_master.conf.local;
  [root@master ~]# cat /etc/nginx/conf.d/mysql_stream_master.conf.local
  stream {
      upstream mysql_backend {
          server unix:/var/lib/mysql/mysql_original.sock;
          server slaves-ip:13306 backup;  # Use Slaves IP here
      }

      server {
          listen     127.0.0.1:3306;
          listen     unix:/var/lib/mysql/mysql.sock;
          proxy_pass mysql_backend;
      }
  }

  On Slave:
  cp -p /etc/nginx/conf.d/mysql_stream_slave.conf /etc/nginx/conf.d/mysql_stream_slave.conf.local

  root@slave [~]# cat /etc/nginx/conf.d/main_custom_include.conf
  include /etc/nginx/conf.d/mysql_stream_slave.conf.local;
  root@slave [~]# cat /etc/nginx/conf.d/mysql_stream_slave.conf.local
  stream {
      upstream mysql_backend {
          server masters-ip:13306; # Use Masters IP here
          server unix:/var/lib/mysql/mysql_original.sock backup;
      }

      server {
          listen     127.0.0.1:3306;
          listen     unix:/var/lib/mysql/mysql.sock;
          proxy_pass mysql_backend;
      }
  }

  restart Nginx on both master and slave

9. Ensure database access work from both servers.

WHM >> Home »SQL Services »Additional MySQL Access Hosts

Add both master and slave servers IP address here


**APPLICATION SERVERS**

10. Setup PHP-FPM backends (for PHP) and Phusion Passenger ( RUBY , PYTHON , NODEJS) on all servers in the cluster
::

  For PHP support
  ================

  On Master:
  /opt/nDeploy/scripts/easy_php_setup.sh

  On Slave:
  /opt/nDeploy/scripts/easy_php_setup.sh

  For RUBY, PYTHON and NODEJS support
  ======================
  On Master:
  /usr/nginx/scripts/nginx-passenger-setup.sh

  On Slave:
  /usr/nginx/scripts/nginx-passenger-setup.sh


Start the cluster
------------------
As a last step you must provide nDeploy with a ipmap file that maps IP address on master to IP address on
slave server for configuration generation

11. Make the ipmap file that maps each IP on the master to an ip on the slave

::

  /opt/nDeploy/scripts/update_cluster_ipmap.py
  usage: update_cluster_ipmap.py [-h] slave_hostname ip_here remote_ip
  update_cluster_ipmap.py: error: too few arguments

  /opt/nDeploy/scripts/update_cluster_ipmap.py slavehostname ip-on-master corresponding-ip-on-slave

  The above step creates the /opt/nDeploy/conf/ndeploy_cluster.yaml

  Example:

  /opt/nDeploy/scripts/update_cluster_ipmap.py slave.sysally.net 162.243.56.192 162.243.54.157

  [root@master ~]# cat /opt/nDeploy/conf/ndeploy_cluster.yaml
  slave.sysally.net:
    ipmap:
      162.243.56.192: 162.243.54.157


.. disqus::
