Setting up NodeJS
==================

1. Enable the Phusion Passenger module
``/usr/nginx/scripts/nginx-passenger-setup.sh``

2. To provide nodeJs backend you must install https://github.com/creationix/nvm

  Note that only nodeJs versions 0.10 and above will work!

3. Register the NodeJS backend in nDeploy
::

  root@cpanel1 [~]# nvm ls-remote

  root@cpanel1 [~]# nvm install v0.11.14

  root@cpanel1 [~]# nvm ls
  ->  v0.10.33
      v0.11.14
  stable -> 0.10 (-> v0.10.33) (default)
  unstable -> 0.11 (-> v0.11.14) (default)

  /opt/nDeploy/scripts/update_backend.py NODEJS v0.11.14 /usr/local/nvm/v0.11.14/bin/node


4. cPanel user can run npm install --production in the package directory
::

  npm install (in package directory, no arguments):

  Install the dependencies in the local node_modules folder.

Additional Reference
https://www.phusionpassenger.com/library/deploy/nginx/deploy/nodejs/

Additonal Environment variables can be set per application by the cPanel user in MANUAL edit mode from nDeploy
https://www.phusionpassenger.com/library/config/nginx/reference/#passenger_env_var

.. disqus::
