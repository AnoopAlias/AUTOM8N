Naxsi
=======

.. note:: NAXSI will only be enabled if ModSecurity is in the disabled state

NAXSI is Nginx Anti XSS and SQL Injection . https://github.com/nbs-system/naxsi

Currently XtendWeb support enabling/disabling NAXSI WAF and loading community contributed whitelists for Drupal and Wordpress CMS .
Extending NAXSI using whitelists need root level access to the server .

Root user can add Whitelists to the file
::

  /etc/nginx/sites-enabled/{ cpaneldomain }.naxsi.wl # Where cpaneldomain is the actual cPanel configured domainname
  nginx -s reload  # to load the whitelists into the server
