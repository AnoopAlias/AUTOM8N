http to https redirection
=========================

for domains having _SSL vhost one can easily redirect the non-SSL domain to SSL

1. Configure the non SSL domain with AUTO
::

  Backend : PROXY
  backend version: redirect
  Select a configuration template: nginX redirect http to https
  Enable/Disable Google PageSpeed Optimizations: DISABLE

2. Configure the SSL domain normally with whatever back-end you need.

.. disqus::
