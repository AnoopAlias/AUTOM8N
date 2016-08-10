Setting up ColdFusion or Java
==============================

There are 2 ways to setup ColdFusion supported by nDeploy

￼
**Using Tomcat**

This is the simplest to setup. The downside is that this setup is
not suited for a shared environment as the app server will be restarted for domain
addition and removal etc.

1. Install the railo bundled with tomcat Railo Server with Tomcat 7 from http://www.getrailo.org/index.cfm/download/

2. Register the backend with backend_name railo_tomcat as type PROXY and path 8888 (this is default port for the above installer!)

  ``/opt/nDeploy/scripts/update_backend.py PROXY railo_tomcat 8888``

**Using Caucho resin**

This is perfect for shared coldfusion hosting providers

Resin or Resin Pro is supported . Resin has a watchdog that helps to dynamically add/remove webapps without restart

Install resin or resin pro and deploy railo war to the ROOT context and add it as a servelet loaded by default in all webapps

1. Setup JAVA
::

  root@cpanel1 [~]# yum install java-1.8.0-openjdk-javadoc.noarch java-1.8.0-openjdk-src.x86_64 java-1.8.0-openjdk-devel.x86_64 java-1.8.0-openjdk-headless.x86_64
  root@cpanel1 [~]# java -version
  openjdk version "1.8.0_25"
  OpenJDK Runtime Environment (build 1.8.0_25-b17)
  OpenJDK 64-Bit Server VM (build 25.20-b23, mixed mode)

2. Install Resin RPM

``root@cpanel1 [~]# rpm -ivh http://caucho.com/download/rpm-6.5/4.0.41/x86_64/resin-4.0.41-1.x86_64.rpm``

3. You will see resin running in ps output
::

  root      3656 45.4  4.1 2513972 85136 pts/0   Sl   03:41   0:06 /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.25-3.b17.el6_6.x86_64/bin/java -Dresin.watc
  resin     3708 67.8  6.5 2796608 135580 pts/0  Sl   03:41   0:06  \_ /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.25-3.b17.el6_6.x86_64/bin/java -Dresin.

4. Stop resin and edit /etc/resin/resin.properties
::

  # For security, Resin can switch to a non-root user after binding to port 80
  -- setuid_user : resin
  -- setuid_group : resin
  ++ setuid_user : nobody
  ++ setuid_group : nobody

  # Web-apps named with numeric suffixes, e.g. foo-10.0.war and can be browsed
  # as /foo. When a new version of the web-app is deployed, Resin continues
  # to route active session requests to the previous web-app version while
  # new sessions go to the new version, so users will not be aware of the
  # application upgrade.
  webapp_multiversion_routing : true

  # Arg passed directly to the JVM
  jvm_args  : -Xmx512m
  jvm_mode    : -server

  # disable the quercus *.php mapping when using Apache for PHP
  quercus_disable : true

  # Enable remote admin (for remote CLI and for EC2 ext: triad discovery)
  remote_admin_enable : true

  # Enable /resin-admin web administration console
  web_admin_enable : true
  web_admin_host   :

  # Permit access to /resin-admin from non-local network ip-addresses
  # web_admin_external : true

  # Require HTTPS to access /resin-admin
  # web_admin_ssl : true

  # Enable Resin REST Admin
  rest_admin_enable : true

5. Generate and setup the ADMINISTRATOR user login
::

  root@cpanel1 [~]# resinctl generate-password --user ADMINISTRATOR
  Enter password:
  Verify password:
  admin_user : ADMINISTRATOR
  admin_password : {SSHA}R4irpW6LJiUtnnW4PAebEYXHhZLgy7w4

6. Set up permissions for nobody user
::

  cd /var
  root@cpanel1 [/var]# chown -R nobody:nobody resin
  root@cpanel1 [/var]# chown -R root:root resin/watchdog-data

  cd /var/resin

  root@cpanel1 [/var/resin]# mkdir hosts
  root@cpanel1 [/var/resin]# chown -R nobody:nobody hosts

7. Download and install RAILO
::

  root@cpanel1 [/var/resin/webapp-jars]# ls
  ./  ../
  root@cpanel1 [/var/resin/webapp-jars]# wget http://www.getrailo.org/railo/remote/download42/4.2.1.008/custom/all/railo-4.2.1.008-jars.tar.gz
  --2014-12-05 04:09:29--  http://www.getrailo.org/railo/remote/download42/4.2.1.008/custom/all/railo-4.2.1.008-jars.tar.gz
  Resolving www.getrailo.org... 188.138.56.135
  Connecting to www.getrailo.org|188.138.56.135|:80... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: 61704841 (59M) [application/x-gzip]
  Saving to: `railo-4.2.1.008-jars.tar.gz'

  100%[========================================================================================================>] 6,17,04,841 11.2M/s   in 5.4s

  2014-12-05 04:09:35 (10.9 MB/s) - `railo-4.2.1.008-jars.tar.gz' saved [61704841/61704841]

  root@cpanel1 [/var/resin/webapp-jars]#

  root@cpanel1 [/var/resin/webapp-jars]# tar -xvzf railo-4.2.1.008-jars.tar.gz

  root@cpanel1 [/var/resin/webapp-jars]# mv railo-4.2.1.008-jars/* ./

  root@cpanel1 [/var/resin/webapp-jars]# rm -rf railo-4.2.1.008-jars railo-4.2.1.008-jars.tar.gz

8. Edit file /etc/resin/app-default.xml
::

  <servlet servlet-name="CFMLServlet" servlet-class="railo.loader.servlet.CFMLServlet">
      <init-param>
        <param-name>railo-web-directory</param-name>
        <param-value>{web-root-directory}/WEB-INF/railo/</param-value>
        <description>Railo Web Directory directory</description>
      </init-param>
      <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet servlet-name="AMFServlet" servlet-class="railo.loader.servlet.AMFServlet">
      <load-on-startup>2</load-on-startup>
    </servlet>

    <servlet-mapping url-pattern="*.cfm" servlet-name="CFMLServlet"/>
    <servlet-mapping url-pattern="*.cfml" servlet-name="CFMLServlet"/>
    <servlet-mapping url-pattern="*.cfc" servlet-name="CFMLServlet"/>

    <welcome-file-list>
      <welcome-file>index.cfm</welcome-file>
      <welcome-file>index.cfml</welcome-file>
      <welcome-file>index.jsp</welcome-file>
      <welcome-file>index.php</welcome-file>
      <welcome-file>index.html</welcome-file>
    </welcome-file-list>

9. Set railo server-context and web-context password
::

  http://cpanel1.sysally.net:8080/railo-context/admin/server.cfm
  http://cpanel1.sysally.net:8080/railo-context/admin/web.cfm

10. Register the railo server as a PROXY backend
::

  root@cpanel1 [~]# /opt/nDeploy/scripts/update_backend.py PROXY railo_resin 8080

.. disqus::
