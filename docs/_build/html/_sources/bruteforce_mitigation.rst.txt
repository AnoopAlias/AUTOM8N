Brute Force Mitigation
===========================

The default proxy template on XtendWeb rate limits access to the following URL entry points

::

  /admin
  /administrator
  /login
  /wp-admin
  /search
  /wp-login.php
  /xmlrpc.php


Administrators can extend this list to include more URL's by adding a custom template.

This prevents a brute force attack on the above URL's , but allows access to genuine users.
