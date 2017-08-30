Tomcat Java backend
===========================

To setup a Tomcat web application server do
::

  # Install tomcat
  yum -y install tomcat

  #On CentOS6 edit file /etc/sysconfig/tomcat and change
  # What user should run tomcat
  TOMCAT_USER="root"

  # On CentOS7
  cp -p /usr/lib/systemd/system/tomcat.service /etc/systemd/system/tomcat.service
  vi /etc/systemd/system/tomcat.service
  # change under [Service]
  User=root
  Group=root

  systemctl daemon-reload
  systemctl restart tomcat


  # Register template
  /opt/nDeploy/scripts/update_profiles.py add root main PROXY 1007.j2 "A Java App"

  # Register backend
  /opt/nDeploy/scripts/update_backend.py add PROXY java_tomcat 8080


Users can select PROXY as backend and select "A Java App" as template to enable java support.
