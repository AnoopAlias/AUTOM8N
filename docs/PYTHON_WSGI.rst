Setting up Python (WSGI app)
=============================

1. Enable the Phusion Passenger module
``/usr/nginx/scripts/nginx-passenger-setup.sh``

2. To setup python install https://github.com/saghul/pythonz
::

  root@cpanel1 [~]# pythonz install 3.4.2

  root@cpanel1 [~]# pythonz list
  # Installed Python versions
    CPython-2.7.8
    CPython-3.4.2

  root@cpanel1 [~]# pythonz locate 3.4.2
  /usr/local/pythonz/pythons/CPython-3.4.2/bin/python3

3. Register the python backend
::

  root@cpanel1 [~]# /opt/nDeploy/scripts/update_backend.py PYTHON CPython-3.4.2 /usr/local/pythonz/pythons/CPython-3.4.2/bin/python3

**Bootstrapping PIP**

PIP can be used to add additional python modules by cPanel user
::

  wget https://bootstrap.pypa.io/get-pip.py

  root@cpanel1 [~]# pythonz locate 3.4.2
  /usr/local/pythonz/pythons/CPython-3.4.2/bin/python3

  root@cpanel1 [~]# /usr/local/pythonz/pythons/CPython-3.4.2/bin/python3 get-pip.py

To install PIP packages as user add the --user flag
::

  gnusys@gnusys.net [~]# /usr/local/pythonz/pythons/CPython-2.7.8/bin/pip install --user PyYAML

Additional Reference
https://www.phusionpassenger.com/library/deploy/nginx/deploy/python/

Additonal Environment variables can be set per application by the cPanel user in MANUAL edit mode from nDeploy
https://www.phusionpassenger.com/library/config/nginx/reference/#passenger_env_var

.. disqus::
