Setting up HHVM
================

HHVM manages new connections in threads of single process unlike PHP-FPM that handles new connections
by forking a new process . So unlike PHP-FPM there is no process pool in HHVM

nDeploy only supports HHVM running as a single user (nobody) using a single process .The recommended way
of running HHVM for multiple users is to create a process for each user which then require a third party process manager
to manage the process creation and shutdown

**HHVM install and setup on CentOS7**

#. Install HHVM as per https://github.com/facebook/hhvm/wiki/Prebuilt-Packages-on-Centos-7.x
#. Setup HHVM as an nDeploy backend app server

::

  cp /opt/nDeploy/conf/hhvm_nobody_server.ini /etc/hhvm/server.ini
  mkdir /var/log/hhvm/
  chown nobody:nobody /var/log/hhvm/
  mkdir /var/run/hhvm/
  chown nobody:nobody /var/run/hhvm/

  edit /usr/lib/systemd/system/hhvm.service and change --user hhvm to --user nobody

  systemctl enable hhvm
  systemctl start hhvm

  You can check hhvm status using
  systemctl status hhvm

  Register the HHVM backend in nDeploy
  /opt/nDeploy/scripts/update_backend.py HHVM_NOBODY hhvm /var/run/hhvm/hhvm.sock

.. disqus::
